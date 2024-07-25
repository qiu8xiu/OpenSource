import networkx as nx
from company import DebtNetwork

class LSMOptimizer:
    def __init__(self, network):
        self.network = network
        self.optimization_records = []

    def optimize(self):
        G = nx.DiGraph()

        # Build the directed graph
        for company in self.network.companies.values():
            G.add_node(company.id, name=company.name)
            for debtor_id, amount in company.debtors.items():
                G.add_edge(company.id, debtor_id, weight=amount)

        while True:
            # Find all cycles in the graph
            cycles = list(nx.simple_cycles(G))
            if not cycles:
                break

            # Prioritize cycles by the minimum debt amount in each cycle
            cycles.sort(key=lambda cycle: min(G[u][v]['weight'] for u, v in zip(cycle, cycle[1:] + [cycle[0]])))

            # Optimize the first cycle in the sorted list
            self._optimize_cycle(G, cycles[0])

        # Update the original network
        self._update_network(G)

    def _optimize_cycle(self, G, cycle):
        edges_in_cycle = [(u, v) for u, v in zip(cycle, cycle[1:] + [cycle[0]]) if G.has_edge(u, v)]
        min_debt = min(G[u][v]['weight'] for u, v in edges_in_cycle)

        # Record the optimization details
        self.optimization_records.append({
            'cycle': [self.network.get_company_name_by_id(node) for node in cycle],
            'edges': [(self.network.get_company_name_by_id(u), self.network.get_company_name_by_id(v)) for u, v in edges_in_cycle],
            'min_debt': min_debt,
        })

        # Reduce all debts in the cycle by the minimum debt
        for u, v in edges_in_cycle:
            G[u][v]['weight'] -= min_debt

        # Remove edges with weight zero
        edges_to_remove = [(u, v) for u, v in edges_in_cycle if G[u][v]['weight'] == 0]
        G.remove_edges_from(edges_to_remove)

    def _update_network(self, G):
        # Clear original network's debtors and creditors
        for company in self.network.companies.values():
            company.debtors.clear()
            company.creditors.clear()

        # Update original network with optimized values
        for u, v, data in G.edges(data=True):
            amount = data['weight']
            if amount > 0:
                from_company = self.network.companies[u]
                to_company = self.network.companies[v]
                from_company.add_debt(v, amount)
                to_company.add_credit(u, amount)

    def get_optimization_records(self):
        return self.optimization_records

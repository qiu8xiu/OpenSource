import networkx as nx
import logging
from company import DebtNetwork

class LSMOptimizer:
    def __init__(self, network):
        self.network = network
        self.logger = logging.getLogger('LSMOptimizer')
        handler = logging.FileHandler('optimization.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def optimize(self):
        G = nx.DiGraph()

        # Build the directed graph
        for company in self.network.companies.values():
            G.add_node(company.id, name=company.name)
            for debtor_id, amount in company.debtors.items():
                G.add_edge(company.id, debtor_id, weight=amount)

        # Find all cycles in the graph
        cycles = list(nx.simple_cycles(G))

        # Log initial cycles
        self.logger.info(f"Initial cycles found: {cycles}")

        # Remove cycles and optimize
        for cycle in cycles:
            self._optimize_cycle(G, cycle)

        # Update the original network
        self._update_network(G)

    def _optimize_cycle(self, G, cycle):
        # Find the minimum debt in the cycle
        edges_in_cycle = [(u, v) for u, v in zip(cycle, cycle[1:] + [cycle[0]]) if G.has_edge(u, v)]
        min_debt = min(G[u][v]['weight'] for u, v in edges_in_cycle)

        # Log the optimization details
        self.logger.info(f"Optimizing cycle: {cycle}")
        self.logger.info(f"Edges in cycle: {edges_in_cycle}")
        self.logger.info(f"Minimum debt in cycle: {min_debt}")

        # Reduce all debts in the cycle by the minimum debt
        for u, v in edges_in_cycle:
            G[u][v]['weight'] -= min_debt

        # Remove edges with weight zero
        edges_to_remove = [(u, v) for u, v in edges_in_cycle if G[u][v]['weight'] == 0]
        self.logger.info(f"Removing edges with zero weight: {edges_to_remove}")
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

        # Log the updated network
        self.logger.info("Updated network:")
        for company in self.network.companies.values():
            self.logger.info(f"Company: {company.name} (ID: {company.id})")
            self.logger.info(f"  Debtors: {company.debtors}")
            self.logger.info(f"  Creditors: {company.creditors}")
            self.logger.info(f"  Total Debt: {sum(company.debtors.values())}")
            self.logger.info(f"  Total Credit: {sum(company.creditors.values())}")
            self.logger.info(f"  Net Position: {sum(company.creditors.values()) - sum(company.debtors.values())}")

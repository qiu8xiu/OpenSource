import matplotlib.pyplot as plt
import networkx as nx

def visualize_network(network):
    G = nx.DiGraph()

    for company in network.companies.values():
        G.add_node(company.name)
        for debtor_id, amount in company.debtors.items():
            debtor_name = network.companies[debtor_id].name
            G.add_edge(company.name, debtor_name, weight=amount)

    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color="lightblue", font_size=10, font_weight="bold", arrowsize=20)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    
    plt.title("Debt Network")
    plt.axis('off')  # Hide axis
    plt.show()

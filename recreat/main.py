from scenario import SimpleCycleScenario, ChainScenario, MixedScenario
from visualize import visualize_network
from calculations import NetworkCalculations
from optimizer import LSMOptimizer


def run_scenario(scenario):
    print(f"Running scenario: {scenario.name}")
    network = scenario.initialize()
    calculations = NetworkCalculations(network)

    # Display initial network
    network.display_network()
    visualize_network(network)
    
    # Print initial nominal liabilities matrix
    print("Initial Nominal Liabilities Matrix:")
    calculations.print_nominal_liabilities_matrix()

    # Print total debt and credit
    calculations.print_total_debt_and_credit()

    # Print net positions
    calculations.print_net_positions()

    # Print net internal debt
    calculations.print_net_internal_debt()

    # Print efficiency matrix
    calculations.print_efficiency_matrix()

    # Print stability coefficient
    calculations.print_stability_coefficient()


    # Visualize network
    visualize_network(network)

    # Print optimization records
    optimizer = LSMOptimizer(network)
    optimizer.optimize() 
    calculations.print_optimization_results()
    print_optimization_records(optimizer) 

def print_optimization_records(optimizer):
    records = optimizer.get_optimization_records()
    print("\nOptimization Records:")
    for record in records:
        print(f"Cycle: {record['cycle']}")
        print(f"Edges: {record['edges']}")
        print(f"Minimum debt in cycle: {record['min_debt']}")
        print("")




def main():
    scenarios = [
#        SimpleCycleScenario("Simple Cycle"),
#        ChainScenario("Chain Scenario"),
        MixedScenario("Mixed Scenario")
    ]
    
    for scenario in scenarios:
        run_scenario(scenario)


if __name__ == "__main__":
    main()

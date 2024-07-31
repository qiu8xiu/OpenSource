from scenario import SimpleCycleScenario, ChainScenario, MixedScenario, ComplexScenario
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


    # Print optimization records
    optimizer = LSMOptimizer(network)
    optimizer.optimize() 
    calculations.print_optimization_results()
    print_optimization_records(optimizer) 

    # Visualize network
    visualize_network(network)

def print_optimization_records(optimizer):
    records = optimizer.get_optimization_records()
    print("\nRecords:")
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
        ComplexScenario("Complex Scenario")  # Add the complex scenario here
    ]
    
    for scenario in scenarios:
        run_scenario(scenario)


if __name__ == "__main__":
    main()

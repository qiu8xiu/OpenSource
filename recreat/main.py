from scenario import SimpleCycleScenario, ChainScenario, MixedScenario
from visualize import visualize_network
from calculations import NetworkCalculations

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
    total_debt, total_credit = calculations.get_total_debt_and_credit()
    print("Total Debt:", total_debt)
    print("Total Credit:", total_credit)

    # Print net positions
    net_positions = calculations.get_net_positions()
    print("Net Positions:", net_positions)

    # Print net internal debt
    net_internal_debt = calculations.get_net_internal_debt()
    print("Net Internal Debt:", net_internal_debt)

    # Print efficiency matrix
    efficiency_matrix, _ = calculations.get_efficiency_matrix()
    print("Efficiency Matrix:")
    print(efficiency_matrix)

    # Print stability coefficient
    stability_coefficient, _ = calculations.get_stability_coefficient()
    print("Stability Coefficient:", stability_coefficient)

    # Optimize and print optimization results
    calculations.print_optimization_results()

    # Visualize network
    visualize_network(network)

def main():
    scenarios = [
        SimpleCycleScenario("Simple Cycle"),
        ChainScenario("Chain Scenario"),
        MixedScenario("Mixed Scenario")
    ]
    
    for scenario in scenarios:
        run_scenario(scenario)

if __name__ == "__main__":
    main()

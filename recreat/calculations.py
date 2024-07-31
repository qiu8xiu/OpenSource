import numpy as np
from company import DebtNetwork
from optimizer import LSMOptimizer

class NetworkCalculations:
    def __init__(self, network: DebtNetwork):
        self.network = network
        self.pre_optimization_network = None  # To store the state before optimization

    def get_nominal_liabilities_matrix(self):
        n = len(self.network.companies)
        ids = list(self.network.companies.keys())
        id_to_index = {id_: index for index, id_ in enumerate(ids)}
        L = np.zeros((n, n))
        for i, company in enumerate(self.network.companies.values()):
            for debtor_id, amount in company.debtors.items():
                j = id_to_index[debtor_id]
                L[i, j] = amount
        return L, ids

    def get_total_debt_and_credit(self):
        total_debt = {company.id: sum(company.debtors.values()) for company in self.network.companies.values()}
        total_credit = {company.id: sum(company.creditors.values()) for company in self.network.companies.values()}
        return total_debt, total_credit

    def get_net_positions(self):
        total_debt, total_credit = self.get_total_debt_and_credit()
        net_positions = {id_: total_credit[id_] - total_debt[id_] for id_ in total_debt.keys()}
        return net_positions

    def get_net_internal_debt(self):
        net_positions = self.get_net_positions()
        net_internal_debt = sum(max(-pos, 0) for pos in net_positions.values())
        return net_internal_debt

    def get_efficiency_matrix(self):
        L, ids = self.get_nominal_liabilities_matrix()
        n = len(ids)
        E = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                if L[i, j] > 0:
                    E[i, j] = L[i, j] / np.sum(L[i, :])
        return E, ids

    def get_stability_coefficient(self):
        L, ids = self.get_nominal_liabilities_matrix()
        n = len(ids)
        stability_coefficient = np.zeros(n)
        for i in range(n):
            in_sum = np.sum(L[:, i])
            out_sum = np.sum(L[i, :])
            stability_coefficient[i] = in_sum / out_sum if out_sum > 0 else 0
        return stability_coefficient, ids

    def print_nominal_liabilities_matrix(self, L=None, ids=None):
        if L is None or ids is None:
            L, ids = self.get_nominal_liabilities_matrix()
        names = [self.network.get_company_name_by_id(id_) for id_ in ids]
        n = len(ids)
        print("Nominal Liabilities Matrix L:")
        print("       " + " ".join(f"{name:>10}" for name in names))
        for i in range(n):
            row = " ".join(f"{int(L[i, j]):>10}" for j in range(n))
            total_debt = int(np.sum(L[i, :]))
            print(f"{names[i]:>10}: {row} | {total_debt}")
        print("-" * (12 * (n + 1)))
        col_totals = " ".join(f"{int(np.sum(L[:, j])):>10}" for j in range(n))
        print(f"{'Total':>10}: {col_totals}")

    def print_total_debt_and_credit(self):
        total_debt, total_credit = self.get_total_debt_and_credit()
        print("Total Debt and Credit:")
        for company_id in total_debt.keys():
            company_name = self.network.get_company_name_by_id(company_id)
            print(f"{company_name}: Debt = {total_debt[company_id]}, Credit = {total_credit[company_id]}")

    def print_net_positions(self, net_positions=None):
        if net_positions is None:
            net_positions = self.get_net_positions()
        net_positions_with_names = self.network.convert_ids_to_names(net_positions)
        print("Net Positions:")
        for company_name, net_position in net_positions_with_names.items():
            print(f"{company_name}: Net Position = {net_position}")

    def print_net_internal_debt(self):
        net_internal_debt = self.get_net_internal_debt()
        print(f"Net Internal Debt: {net_internal_debt}")

    def print_efficiency_matrix(self):
        E, ids = self.get_efficiency_matrix()
        names = [self.network.get_company_name_by_id(id_) for id_ in ids]
        n = len(ids)
        print("Efficiency Matrix E:")
        print("       " + " ".join(f"{name:>10}" for name in names))
        for i in range(n):
            row = " ".join(f"{E[i, j]:>10.2f}" for j in range(n))
            print(f"{names[i]:>10}: {row}")

    def print_stability_coefficient(self):
        stability_coefficient, ids = self.get_stability_coefficient()
        print("Stability Coefficient:")
        for i, company_id in enumerate(ids):
            company_name = self.network.get_company_name_by_id(company_id)
            print(f"{company_name}: Stability Coefficient = {stability_coefficient[i]}")

    def save_pre_optimization_state(self):
        """ Save the current state of the network before optimization. """
        self.pre_optimization_network = {
            "nominal_liabilities_matrix": self.get_nominal_liabilities_matrix(),
            "net_positions": self.get_net_positions(),
        }

    def print_pre_optimization_results(self):
        """ Print results saved before optimization. """
        if self.pre_optimization_network:
            print("Before Optimization:")
            L, ids = self.pre_optimization_network["nominal_liabilities_matrix"]
            self.print_nominal_liabilities_matrix(L, ids)
            self.print_net_positions(self.pre_optimization_network["net_positions"])
        else:
            print("Pre-optimization data not available.")

    def print_optimization_results(self):
        print("After Optimization:")
        self.print_nominal_liabilities_matrix()
        self.print_net_positions()

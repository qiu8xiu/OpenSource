import numpy as np
from company import DebtNetwork
from optimizer import LSMOptimizer

class NetworkCalculations:
    def __init__(self, network: DebtNetwork):
        self.network = network

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

    def print_nominal_liabilities_matrix(self):
        L, ids = self.get_nominal_liabilities_matrix()
        n = len(ids)
        print("Nominal Liabilities Matrix L:")
        for i in range(n):
            row = " ".join(f"{int(L[i, j])}" for j in range(n))
            total_debt = int(np.sum(L[i, :]))
            print(f"{row} | {total_debt}")
        print("-" * (2 * n + 3))
        col_totals = " ".join(f"{int(np.sum(L[:, j]))}" for j in range(n))
        print(f"{col_totals}")
        print()

    def print_optimization_results(self):
        print("Before Optimization:")
        self.print_nominal_liabilities_matrix()

        optimizer = LSMOptimizer(self.network)
        optimizer.optimize()

        print("After Optimization:")
        self.print_nominal_liabilities_matrix()

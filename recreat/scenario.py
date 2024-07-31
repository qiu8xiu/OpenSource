from company import DebtNetwork

class Scenario:
    def __init__(self, name):
        self.name = name
        self.network = DebtNetwork()

    def initialize(self):
        raise NotImplementedError("Subclasses should implement this method")

    def print_company_info(self, company_name):
        info = self.network.get_company_info(company_name)
        if info:
            print(f"Company: {info['name']}")
            print(f"  Debtors: {info['debtors']}")
            print(f"  Creditors: {info['creditors']}")
            print(f"  Total Debt: {info['total_debt']}")
            print(f"  Total Credit: {info['total_credit']}")
            print(f"  Net Position: {info['net_position']}")
        else:
            print(f"Company {company_name} not found in scenario {self.name}.")

class SimpleCycleScenario(Scenario):
    def initialize(self):
        self.network.add_debt("Company A", "Company B", 100)
        self.network.add_debt("Company B", "Company C", 150)
        self.network.add_debt("Company A", "Company C", 200)
        self.network.add_debt("Company C", "Company A", 50)
        return self.network

class ChainScenario(Scenario):
    def initialize(self):
        self.network.add_debt("Company A", "Company B", 100)
        self.network.add_debt("Company B", "Company C", 150)
        self.network.add_debt("Company C", "Company D", 200)
        self.network.add_debt("Company D", "Company E", 250)
        return self.network

class MixedScenario(Scenario):
    def initialize(self):
        self.network.add_debt("Company A", "Company B", 100)
        self.network.add_debt("Company B", "Company C", 150)
        self.network.add_debt("Company A", "Company D", 200)
        self.network.add_debt("Company D", "Company E", 250)
        self.network.add_debt("Company E", "Company A", 300)
        self.network.add_debt("Company C", "Company F", 350)
        self.network.add_debt("Company F", "Company B", 400)
        return self.network

class ComplexScenario:
    def __init__(self, name):
        self.name = name

    def initialize(self):
        network = DebtNetwork()


        # Adding debts
        network.add_debt("Company A", "Company B", 200)
        network.add_debt("Company A", "Company C", 300)
        network.add_debt("Company B", "Company C", 150)
        network.add_debt("Company B", "Company D", 100)
        network.add_debt("Company C", "Company A", 250)
        network.add_debt("Company C", "Company E", 400)
        network.add_debt("Company D", "Company B", 100)
        network.add_debt("Company D", "Company E", 150)
        network.add_debt("Company E", "Company A", 350)

        return network

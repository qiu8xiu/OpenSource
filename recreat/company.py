import uuid

class Company:
    def __init__(self, name):
        self.id = uuid.uuid4()
        self.name = name
        self.debtors = {}
        self.creditors = {}

    def add_debt(self, to, amount):
        if to in self.debtors:
            self.debtors[to] += amount
        else:
            self.debtors[to] = amount

    def add_credit(self, from_, amount):
        if from_ in self.creditors:
            self.creditors[from_] += amount
        else:
            self.creditors[from_] = amount

class DebtNetwork:
    def __init__(self):
        self.companies = {}

    def add_company(self, company):
        if company.id not in self.companies:
            self.companies[company.id] = company

    def get_or_create_company(self, name):
        for company in self.companies.values():
            if company.name == name:
                return company

        new_company = Company(name)
        self.add_company(new_company)
        return new_company

    def add_debt(self, from_name, to_name, amount):
        from_company = self.get_or_create_company(from_name)
        to_company = self.get_or_create_company(to_name)

        from_company.add_debt(to_company.id, amount)
        to_company.add_credit(from_company.id, amount)

    def remove_company(self, name):
        company = self.get_or_create_company(name)
        if company:
            del self.companies[company.id]

    def update_company(self, old_name, new_name):
        company = self.get_or_create_company(old_name)
        if company:
            company.name = new_name

    def display_network(self):
        for company in self.companies.values():
            print(f"Company: {company.name} (ID: {company.id})")
            print(f"  Debtors: {self.convert_ids_to_names(company.debtors)}")
            print(f"  Creditors: {self.convert_ids_to_names(company.creditors)}")
            print(f"  Total Debt: {sum(company.debtors.values())}")
            print(f"  Total Credit: {sum(company.creditors.values())}")
            print(f"  Net Position: {sum(company.creditors.values()) - sum(company.debtors.values())}")
            print()

    def get_company_info(self, name):
        for company in self.companies.values():
            if company.name == name:
                return {
                    'name': company.name,
                    'debtors': company.debtors,
                    'creditors': company.creditors,
                    'total_debt': sum(company.debtors.values()),
                    'total_credit': sum(company.creditors.values()),
                    'net_position': sum(company.creditors.values()) - sum(company.debtors.values())
                }
        return None

    def get_company_name_by_id(self, company_id):
        return self.companies[company_id].name if company_id in self.companies else None
    
    def convert_ids_to_names(self, id_dict):
        return {self.get_company_name_by_id(k): v for k, v in id_dict.items()}

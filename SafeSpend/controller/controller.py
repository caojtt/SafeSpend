from SafeSpend.abstract.abstract import IDataManager, IFinancialAdvisor

# ---------------------------
# ViewModel / Controller
# ---------------------------
class SafeSpendController:
    def __init__(self, data_manager: IDataManager, advisor: IFinancialAdvisor):
        self.data_manager = data_manager
        self.advisor = advisor
        self.data = self.data_manager.load_data()

    def save_data(self, month, income, expenses, savings, debt):
        new_entry = pd.DataFrame({
            "Month": [month],
            "Income": [income],
            "Expenses": [expenses],
            "Savings": [savings],
            "Debt Repayment": [debt]
        })
        if not ((self.data["Month"] == month).any()):
            self.data = pd.concat([self.data, new_entry], ignore_index=True)
            self.data_manager.save_data(self.data)
            return True
        return False

    def reset_data(self):
        self.data = self.data_manager.reset_data()

    def get_advice(self, income, expenses, savings, debt, goal):
        return self.advisor.get_advice(income, expenses, savings, debt, goal)

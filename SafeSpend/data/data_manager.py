# ---------------------------
# Data Layer
# ---------------------------
class CSVDataManager(IDataManager):
    def __init__(self, file_path="financial_data.csv"):
        self.file_path = file_path

    def load_data(self):
        if os.path.exists(self.file_path):
            return pd.read_csv(self.file_path, parse_dates=["Month"])
        return pd.DataFrame(columns=["Month", "Income", "Expenses", "Savings", "Debt Repayment"])

    def save_data(self, df):
        df.to_csv(self.file_path, index=False)

    def reset_data(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
        return self.load_data()

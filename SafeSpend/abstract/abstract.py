from abc import ABC, abstractmethod

# ---------------------------
# Interfaces and Abstract Classes
# ---------------------------
class IDataManager(ABC):
    @abstractmethod
    def load_data(self): pass

    @abstractmethod
    def save_data(self, df): pass

    @abstractmethod
    def reset_data(self): pass


class IFinancialAdvisor(ABC):
    @abstractmethod
    def get_advice(self, income, expenses, savings, debt, goal): pass

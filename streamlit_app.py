# Redesigned SafeSpend App Using Robust OOD Principles

from abc import ABC, abstractmethod
import pandas as pd
import os
import re
import streamlit as st
from datetime import datetime
from openai import OpenAI

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


# ---------------------------
# AI Financial Advisor
# ---------------------------
class OpenAIFinancialAdvisor(IFinancialAdvisor):
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def get_advice(self, income, expenses, savings, debt, goal):
        prompt = (
            f"As of {datetime.now().strftime('%B %d, %Y')}, I earn ${income}/mo and spend ${expenses}.\n"
            f"I have ${savings} in savings and owe ${debt}. My financial goal is: {goal}.\n"
            "You are a financial coach providing simple, actionable, and encouraging financial guidance."
        )
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a financial advisor."},
                {"role": "user", "content": prompt},
            ]
        )
        return response.choices[0].message.content


# ---------------------------
# Utility
# ---------------------------
class ResponseCleaner:
    @staticmethod
    def clean(text):
        text = re.sub(r"[*_`#~]", "", text)
        text = re.sub(r"(?<=[a-zA-Z0-9])\n(?=[a-zA-Z0-9])", "", text)
        text = re.sub(r"\n{2,}", "\n\n", text)
        return text.strip()


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


# ---------------------------
# Streamlit GUI (View Layer)
# ---------------------------
def main():
    st.set_page_config(page_title="SafeSpend", layout="wide")
    st.title("SafeSpend AI Money Coach")

    data_manager = CSVDataManager()
    advisor = OpenAIFinancialAdvisor()
    controller = SafeSpendController(data_manager, advisor)

# -------------------------------
# Unified Save Section (Current or Prior Month)
# -------------------------------
    with st.sidebar.expander("Enter or Save Monthly Data"):
        # Default: current month
        selected_date = datetime.now().replace(day=1)
    
        # Toggle for prior month entry
        if st.checkbox("Use Prior Month"):
            months = [
                "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"
            ]
            current_year = datetime.today().year
            years = list(range(2020, current_year + 1))
    
            selected_month = st.selectbox("Month", months)
            selected_year = st.selectbox("Year", years[::-1])
            selected_date = datetime(selected_year, months.index(selected_month) + 1, 1)
    
        # Single set of input fields used for both current and prior
        income_val = st.number_input("Monthly Income ($)", min_value=0.0, step=100.0)
        expenses_val = st.number_input("Monthly Expenses ($)", min_value=0.0, step=100.0)
        savings_val = st.number_input("Savings ($)", min_value=0.0, step=100.0)
        debt_val = st.number_input("Debt ($)", min_value=0.0, step=100.0)
    
        if st.button("Save Data"):
            if controller.save_data(selected_date, income_val, expenses_val, savings_val, debt_val):
                st.success(f"Data for {selected_date.strftime('%B %Y')} saved successfully!")
            else:
                st.warning(f"Data for {selected_date.strftime('%B %Y')} already exists.")


    # income = st.sidebar.number_input("Monthly Income ($)", min_value=0.0, step=100.0)
    # expenses = st.sidebar.number_input("Monthly Expenses ($)", min_value=0.0, step=100.0)
    # savings = st.sidebar.number_input("Savings ($)", min_value=0.0, step=100.0)
    # debt = st.sidebar.number_input("Debt ($)", min_value=0.0, step=100.0)
    # goal = st.sidebar.text_area("Financial Goal", placeholder="e.g., Save for a house")

    # if st.sidebar.button("Save This Month"):
    #     month = datetime.now().replace(day=1)
    #     if controller.save_data(month, income, expenses, savings, debt):
    #         st.success("Data saved.")
    #     else:
    #         st.warning("Data for this month already exists.")

    if st.sidebar.button("Reset Data"):
        controller.reset_data()
        st.success("Data reset.")

    if st.sidebar.button("Get Financial Advice"):
        if goal.strip():
            with st.spinner("Getting your financial plan..."):
                advice = controller.get_advice(income, expenses, savings, debt, goal)
                clean = ResponseCleaner.clean(advice)
                st.subheader("AI-Powered Financial Plan")
                st.text_area("Advice", clean, height=300)
        else:
            st.warning("Please enter a goal.")

    if not controller.data.empty:
        st.subheader("Financial History")
        st.dataframe(controller.data.set_index("Month"))
        st.line_chart(controller.data[["Income", "Expenses", "Savings"]])
        st.line_chart(controller.data[["Debt Repayment"]])


if __name__ == "__main__":
    main()

# -------------------------------
# Import Required Libraries
# -------------------------------
import streamlit as st
import pandas as pd
import os
import re
from openai import OpenAI
from datetime import datetime

# -------------------------------
# Financial Data Manager Class
# -------------------------------
class FinancialDataManager:
    DATA_FILE = "financial_data.csv"

    def load_data(self):
        if os.path.exists(self.DATA_FILE):
            return pd.read_csv(self.DATA_FILE, parse_dates=["Month"])
        else:
            return pd.DataFrame(columns=["Month", "Income", "Expenses", "Savings", "Debt Repayment"])

    def save_data(self, df):
        df.to_csv(self.DATA_FILE, index=False)

    def reset_data(self):
        if os.path.exists(self.DATA_FILE):
            os.remove(self.DATA_FILE)
        return self.load_data()

# -------------------------------
# Financial Advisor Class
# -------------------------------
class FinancialAdvisor:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def get_financial_advice(self, income, expenses, savings, debt, goal):
        current_date = datetime.now().strftime("%B %d, %Y")
        prompt = (
            f"As of {current_date}, I earn ${income} per month and spend ${expenses}. "
            f"I have ${savings} in savings and owe ${debt} in debt. "
            f"My financial goal is: {goal}. "
            "You are a financial coach that gives helpful, non-judgmental, beginner-friendly advice."
            " Based on this, provide a financial plan including budgeting strategies, savings tips, and investment recommendations."
            " Please format your response in clear paragraphs with correct spacing and punctuation."
            " Avoid markdown formatting."
        )
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a financial advisor providing actionable advice."},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content

# -------------------------------
# Data Cleaner Utility Class
# -------------------------------
class DataCleaner:
    @staticmethod
    def clean_response(text):
        text = re.sub(r"[*_`#~]", "", text)
        text = re.sub(r"(?<=[a-zA-Z0-9])\n(?=[a-zA-Z0-9])", "", text)
        text = re.sub(r"\n{2,}", "\n\n", text)
        text = re.sub(r"\s{3,}", "  ", text)
        return text.strip()

# -------------------------------
# SafeSpend Main Application Class
# -------------------------------

# --------------
# Controller
# --------------
class SafeSpendApp:
    def __init__(self):
        self.data_manager = FinancialDataManager()
        self.advisor = FinancialAdvisor()
        self.cleaner = DataCleaner()
        self.data = self.data_manager.load_data()
# --------------
# GUI 
# --------------
    def run(self):
        st.set_page_config(page_title="SafeSpend", layout="wide")
        st.title("SafeSpend AI Money Coach: Smarter Finance Management")
        st.subheader("Get AI-powered financial insights for budgeting, savings, and investments.")

        self.sidebar_inputs()
        self.display_data_and_charts()

    def sidebar_inputs(self):
        st.sidebar.header("Enter Your Monthly Financial Details")

        # Input fields
        income = st.sidebar.number_input("Monthly Income ($)", min_value=0.0, step=100.0, value=0.0)
        expenses = st.sidebar.number_input("Total Monthly Expenses ($)", min_value=0.0, step=100.0, value=0.0)
        savings = st.sidebar.number_input("Current Savings ($)", min_value=0.0, step=100.0, value=0.0)
        debt = st.sidebar.number_input("Total Debt ($)", min_value=0.0, step=100.0, value=0.0)

        # Save Current Month Button
        if st.sidebar.button("Save This Month's Data"):
            self.save_current_month_data(income, expenses, savings, debt)

        # Spacer
        st.sidebar.markdown("---")

        # Prior Month Data Entry
        with st.sidebar.expander("Enter Data for a Prior Month"):
            self.save_prior_month_data()

        # Spacer
        st.sidebar.markdown("---")

        # Investment goal input
        investment_goal = st.sidebar.text_area(
            "What are your financial goals?",
            placeholder="e.g., Save for a down payment on a house"
        )

        # Reset and Get Advice buttons
        if st.sidebar.button("Reset Data"):
            self.data = self.data_manager.reset_data()
            st.success("Data has been reset.")

        if st.sidebar.button("Get AI Financial Advice"):
            if investment_goal.strip() != "":
                with st.spinner("Analyzing your finances…"):
                    try:
                        advice = self.advisor.get_financial_advice(income, expenses, savings, debt, investment_goal)
                        cleaned_advice = self.cleaner.clean_response(advice)
                        st.subheader("AI-Powered Financial Plan")
                        st.text_area("Your SafeSpend Financial Plan:", cleaned_advice, height=300)
                    except Exception as e:
                        st.error(f"Something went wrong with the AI service:\n\n{e}")
            else:
                st.warning("Please enter your financial goal to receive advice.")

    def save_current_month_data(self, income, expenses, savings, debt):
        current_month = datetime.now().replace(day=1)
        if not ((self.data["Month"] == current_month).any()):
            new_entry = pd.DataFrame({
                "Month": [current_month],
                "Income": [income],
                "Expenses": [expenses],
                "Savings": [savings],
                "Debt Repayment": [debt]
            })
            self.data = pd.concat([self.data, new_entry], ignore_index=True)
            self.data_manager.save_data(self.data)
            st.success("Data saved successfully!")
        else:
            st.warning("Data for the current month already exists.")

    def save_prior_month_data(self):
        months = ["January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November", "December"]
        current_date = datetime.today()
        years = list(range(2020, current_date.year + 1))

        selected_month_name = st.selectbox("Select Month", months)
        selected_year = st.selectbox("Select Year", years[::-1])

        selected_month_index = months.index(selected_month_name) + 1
        prior_month = datetime(selected_year, selected_month_index, 1)

        prior_income = st.number_input("Monthly Income ($)", min_value=0.0, step=100.0, value=0.0, key="prior_income")
        prior_expenses = st.number_input("Total Monthly Expenses ($)", min_value=0.0, step=100.0, value=0.0, key="prior_expenses")
        prior_savings = st.number_input("Current Savings ($)", min_value=0.0, step=100.0, value=0.0, key="prior_savings")
        prior_debt = st.number_input("Total Debt ($)", min_value=0.0, step=100.0, value=0.0, key="prior_debt")

        if st.button("Save Prior Month's Data"):
            if not ((self.data["Month"] == prior_month).any()):
                new_entry = pd.DataFrame({
                    "Month": [prior_month],
                    "Income": [prior_income],
                    "Expenses": [prior_expenses],
                    "Savings": [prior_savings],
                    "Debt Repayment": [prior_debt]
                })
                self.data = pd.concat([self.data, new_entry], ignore_index=True)
                self.data_manager.save_data(self.data)
                st.success(f"Data for {prior_month.strftime('%B %Y')} saved successfully!")
            else:
                st.warning(f"Data for {prior_month.strftime('%B %Y')} already exists.")

    def display_data_and_charts(self):
        if not self.data.empty:
            self.data["Month"] = pd.to_datetime(self.data["Month"])
            self.data.sort_values("Month", inplace=True)

            st.subheader("All Financial Data")
            st.dataframe(self.data.set_index("Month"))

            st.subheader("Monthly Financial Trends")
            st.line_chart(self.data[["Income", "Expenses", "Savings"]])

            st.subheader("Debt Repayment Over Time")
            st.line_chart(self.data[["Debt Repayment"]])
        else:
            st.info("No financial data available. Please enter and save your financial details.")

# -------------------------------
# Launch the SafeSpend App
# -------------------------------
if __name__ == "__main__":
    app = SafeSpendApp()
    app.run()



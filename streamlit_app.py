# -------------------------------
# Import Required Libraries
# -------------------------------
import streamlit as st
import pandas as pd
import os
import re
from openai import OpenAI
from datetime import datetime
from PIL import Image

# -------------------------------
# Initialize OpenAI Client
# -------------------------------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -------------------------------
# Configure Streamlit Page
# -------------------------------

st.set_page_config(page_title="SafeSpend", layout="wide")
logo = Image.open("SafeSpendFinalLogo.png")
st.image(logo, width=150)

# -------------------------------
# Define Data File Path
# -------------------------------
DATA_FILE = "financial_data.csv"

# -------------------------------
# Function to Load Data
# -------------------------------
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE, parse_dates=["Month"])
    else:
        # Initialize with an empty DataFrame
        return pd.DataFrame(columns=["Month", "Income", "Expenses", "Savings", "Debt Repayment"])

# -------------------------------
# Function to Save Data
# -------------------------------
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# -------------------------------
# Function to Get Financial Advice
# -------------------------------

def get_financial_advice(income, expenses, savings, debt, goal):
    # Get the current date
    current_date = datetime.now().strftime("%B %d, %Y")
    
    # Construct the prompt with the current date
    prompt = (
        f"As of {current_date}, I earn ${income} per month and spend ${expenses}. "
        f"I have ${savings} in savings and owe ${debt} in debt. "
        f"My financial goal is: {goal}. "
        "You are a financial coach that gives helpful, non-judgmental, beginner-friendly advice."
        "Based on this, provide a financial plan including budgeting strategies, savings tips, and investment recommendations in order to best reach this goal."
        "Please format your response in clear paragraphs with correct spacing and punctuation."
        "Avoid markdown formatting."
    )
    
    # Generate the AI response
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a financial advisor providing actionable advice."},
            {"role": "user", "content": prompt},
        ],
    )
    
    return response.choices[0].message.content


# -------------------------------
# Application Title and Description
# -------------------------------
st.title("SafeSpend AI Money Coach: Smarter Finance Management")
st.subheader("Get AI-powered financial insights for budgeting, savings, and investments.")

# -------------------------------
# Sidebar Inputs for Financial Details
# -------------------------------
st.sidebar.header("Enter Your Monthly Financial Details")

# Input fields for financial data with placeholders
income = st.sidebar.number_input("Monthly Income ($)", min_value=0.0, step=100.0, value=0.0)
expenses = st.sidebar.number_input("Total Monthly Expenses ($)", min_value=0.0, step=100.0, value=0.0)
savings = st.sidebar.number_input("Current Savings ($)", min_value=0.0, step=100.0, value=0.0)
debt = st.sidebar.number_input("Total Debt ($)", min_value=0.0, step=100.0, value=0.0)

# -------------------------------
# Save Current Month's Data
# -------------------------------
# Load existing data
data = load_data()

# Button to save current month's data
if st.sidebar.button("Save This Month's Data"):
    current_month = datetime.now().replace(day=1)
    # Check if current month data already exists
    if not ((data["Month"] == current_month).any()):
        new_entry = pd.DataFrame({
            "Month": [current_month],
            "Income": [income],
            "Expenses": [expenses],
            "Savings": [savings],
            "Debt Repayment": [debt]
        })
        data = pd.concat([data, new_entry], ignore_index=True)
        save_data(data)
        st.success("Data saved successfully!")
    else:
        st.warning("Data for the current month already exists.")

# -------------------------------
# Optional: Enter Data for a Prior Month
# -------------------------------
with st.sidebar.expander("Enter Data for a Prior Month"):
    # Define month and year options
    months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]  

#---------------------------------
# Extract current date
#---------------------------------
    current_date = datetime.today()
#---------------------------------
# Extract the current year
#---------------------------------
    current_year = current_date.year

    years = list(range(2020, current_year + 1))

    # Create separate selectboxes for month and year
    selected_month_name = st.selectbox("Select Month", months)
    selected_year = st.selectbox("Select Year", years[::-1])  # Reverse for descending order

    # Convert selected month and year to a datetime object
    selected_month_index = months.index(selected_month_name) + 1
    prior_month = datetime(selected_year, selected_month_index, 1)

    # Input fields for financial data
    prior_income = st.number_input("Monthly Income ($)", min_value=0.0, step=100.0, value=0.0, key="prior_income")
    prior_expenses = st.number_input("Total Monthly Expenses ($)", min_value=0.0, step=100.0, value=0.0, key="prior_expenses")
    prior_savings = st.number_input("Current Savings ($)", min_value=0.0, step=100.0, value=0.0, key="prior_savings")
    prior_debt = st.number_input("Total Debt ($)", min_value=0.0, step=100.0, value=0.0, key="prior_debt")

    # Button to save the prior month's data
    if st.button("Save Prior Month's Data"):
        data = load_data()
        if not ((data["Month"] == prior_month).any()):
            new_entry = pd.DataFrame({
                "Month": [prior_month],
                "Income": [prior_income],
                "Expenses": [prior_expenses],
                "Savings": [prior_savings],
                "Debt Repayment": [prior_debt]
            })
            data = pd.concat([data, new_entry], ignore_index=True)
            save_data(data)
            st.success(f"Data for {prior_month.strftime('%B %Y')} saved successfully!")
        else:
            st.warning(f"Data for {prior_month.strftime('%B %Y')} already exists.")

# -------------------------------
# Reset Data Function
# -------------------------------
def reset_data():
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)  # Deletes the data file
    return pd.DataFrame(columns=["Month", "Income", "Expenses", "Savings", "Debt Repayment"])

# -------------------------------
# Reset the Data When the App Starts Fresh
# -------------------------------
data = load_data()

# Button to reset the data
if st.sidebar.button("Reset Data"):
    data = reset_data()  # Resets the data to an empty DataFrame
    st.success("Data has been reset.")


investment_goal = st.sidebar.text_area("What are your financial goals? (e.g., Buy a house, Retire early)", placeholder="e.g., Save for a down payment on a house")

# -------------------------------
# Display All Financial Data
# -------------------------------
if not data.empty:
    # Ensure 'Month' column is in datetime format
    data["Month"] = pd.to_datetime(data["Month"])

    # Sort data by Month
    data.sort_values("Month", inplace=True)

    # Display all financial data
    st.subheader("All Financial Data")
    st.dataframe(data.set_index("Month"))
else:
    st.info("No financial data available. Please enter and save your financial details.")

# -------------------------------
# Visualize Financial Trends Over Time
# -------------------------------
st.subheader("Monthly Financial Trends")

if not data.empty:
    # Ensure 'Month' column is in datetime format
    data["Month"] = pd.to_datetime(data["Month"])

    # Sort data by Month
    data.sort_values("Month", inplace=True)

    # Set 'Month' as the index
    data.set_index("Month", inplace=True)

    # Plot Income, Expenses, and Savings
    st.line_chart(data[["Income", "Expenses", "Savings"]])

    # Plot Debt Repayment separately
    st.subheader("Debt Repayment Over Time")
    st.line_chart(data[["Debt Repayment"]])
else:
    st.info("No financial data available to display trends.")

# ------------------------------
# Clean up formattiing
# ------------------------------

def clean_response(text):
    # Remove markdown formatting characters
    text = re.sub(r"[*_`#~]", "", text)

    # Replace weird newlines between characters (e.g. 4\n0\n0\n0)
    text = re.sub(r"(?<=[a-zA-Z0-9])\n(?=[a-zA-Z0-9])", "", text)

    # Normalize double newlines into paragraph spacing
    text = re.sub(r"\n{2,}", "\n\n", text)

    # Collapse excessive spacing
    text = re.sub(r"\s{3,}", "  ", text)

    return text.strip()

# -------------------------------
# Generate AI-Powered Financial Advice
# -------------------------------

if st.sidebar.button("Get AI Financial Advice"):
    if income and expenses and savings and debt and investment_goal:
        with st.spinner("Analyzing your finances…"):
            advice = get_financial_advice(income, expenses, savings, debt, investment_goal)
            cleaned_advice = clean_response(advice)
            st.subheader("AI-Powered Financial Plan")
            st.text_area("Your SafeSpend Financial Plan:", cleaned_advice, height=300)



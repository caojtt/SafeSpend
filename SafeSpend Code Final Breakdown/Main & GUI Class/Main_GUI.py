# ---------------------------
# Streamlit GUI (View Layer)
# ---------------------------

def main():
    st.set_page_config(page_title="SafeSpend", layout="wide")
    st.title("SafeSpend AI Money Coach")

    data_manager = CSVDataManager()
    advisor = OpenAIFinancialAdvisor()
    controller = SafeSpendController(data_manager, advisor)

    
    with st.sidebar.expander("Enter & Save Monthly Financial Data"):
        # Default for current month
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
    
        income = st.number_input("Monthly Income ($)", min_value=0.0, step=100.0)
        expenses = st.number_input("Monthly Expenses ($)", min_value=0.0, step=100.0)
        savings = st.number_input("Savings ($)", min_value=0.0, step=100.0)
        debt = st.number_input("Debt ($)", min_value=0.0, step=100.0)
        goal = st.sidebar.text_area("Financial Goal", placeholder="e.g., I want to save for a house")
        
        if st.button("Save Data"):
            if controller.save_data(selected_date, income, expenses, savings, debt):
                st.success(f"Data for {selected_date.strftime('%B %Y')} saved successfully!")
            else:
                st.warning(f"Data for {selected_date.strftime('%B %Y')} already exists.")

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

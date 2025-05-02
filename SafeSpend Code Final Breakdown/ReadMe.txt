Here is the detailed explanation of the components workflow:                                                                                       
The SafeSpend AI Money Coach app is designed using a modular, object-oriented architecture that separates concerns across different components. Here's a detailed breakdown of how the app works from end to end, including user interaction, internal processing, and backend services:

1. User Interface (<<Streamlit Web GUI>>)
Purpose: This is the only part the user directly sees and interacts with. It handles all inputs, displays outputs, and triggers the backend logic.
How it works:
The user is presented with input fields in a sidebar (income, expenses, savings, debt, financial goals).
When the user clicks the "Get AI Financial Advice" button, the app checks that all inputs are filled.
If valid, it triggers the backend processing by calling the get_financial_advice() function and waits for results.
Once the advice is returned, it's displayed in the app interface as a financial plan.

Code in action:
if st.sidebar.button("Get Financial Advice"):
        if goal.strip():
            with st.spinner("Getting your financial plan..."):
                advice = controller.get_advice(income, expenses, savings, debt, goal)
                clean = ResponseCleaner.clean(advice)
                st.subheader("AI-Powered Financial Plan")
                st.text_area("Advice", clean, height=300)
        else:
            st.warning("Please enter a goal.")
 
2. Controller / Logic Layer
Purpose: Acts as the brain of the app. It decides what should happen when the user triggers an action and how to interact with the backend.
Responsibilities:
Data Management: Reading, writing, and resetting user data in CSV format.

Routing: Bridges the interaction between the UI, data storage, and AI advisor.
Example actions:
When the user submits data, it may save the data to a CSV file using save_data().
If the user wants to reset, it clears all stored data using reset_data().

Code in action:
def load_data(self):
        if os.path.exists(self.file_path):
            return pd.read_csv(self.file_path, parse_dates=["Month"])
        return pd.DataFrame(columns=["Month", "Income", "Expenses", "Savings", "Debt Repayment"])

3. Data Management Layer (CSV Storage)
Purpose: Provides persistent storage of user data across sessions.

How it works:
A file called financial_data.csv is used to store and retrieve user inputs like income, expenses, savings, and debt over time.
This layer is managed exclusively by the controller functions.
Lifecycle:
Data is stored when save_data() is called.
Data is retrieved with load_data().
Data is reset with reset_data() (file is deleted and re-initialized).

 4. AI Financial Advisor (OpenAI GPT-4 API)
Purpose: Acts as the brainy assistant that transforms user inputs into actionable financial advice.
How it works:

When the controller calls get_financial_advice(), it sends a custom prompt to the GPT-4 API with user data embedded in natural language.
The OpenAI service responds with tailored financial strategies which might include budgeting tips, saving plans, or investment guidance.
The result is sent back to the GUI and displayed to the user.

Code in action:
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
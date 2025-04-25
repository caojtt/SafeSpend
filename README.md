Web based product - Link is below

https://safespend-cfqwetjhatg8w9vc5wzrxg.streamlit.app/

STEPS TO RECIEVE FINANCIAL ADVICE FROM SAFESPEND AI MONEY COACH

1. User Opens the App
The app is loaded via Streamlit either locally or through Streamlit Cloud.

A sidebar prompts the user to enter their financial details.

2. User Inputs Monthly Financial Data
The sidebar contains fields for:

Monthly Income

Monthly Expenses

Current Savings

Total Debt

Financial Goal (text input)

The user can also enter prior months’ data via a dropdown (optional).

3. User Saves Financial Data
By clicking "Save This Month's Data" or "Save Prior Month's Data", the app:

Writes the entered data into a local CSV file (financial_data.csv)

Ensures data is not duplicated for the same month

4. User Clicks "Get AI Financial Advice"
When clicked, the app checks if a financial goal is entered

It also:

Pulls the most recent saved data from the CSV file

Uses both the new inputs and historical data to form the prompt

5. Prompt Sent to OpenAI API
The app builds a detailed prompt like:

As of April 2025, the user earns $3000 and spends $2200, has $1000 in savings, and owes $5000 in debt. 
The financial goal is: Save for a house.
This prompt is sent to OpenAI’s GPT-4 model via the openai Python SDK.

6. AI Generates Personalized Financial Plan
The model returns a structured response including:

Budgeting tips

Debt repayment strategies

Goal-aligned savings recommendations

The raw output is cleaned up (removing markdown characters, fixing spacing)

7. AI Advice Displayed to User

8. User Can Reuse Advice or Change Inputs
The user can:

Modify inputs and get updated advice

Reset data entirely using the "Reset Data" button

Continue using the app over time to track monthly trends





Technologies Used
Python 3.8+

Streamlit

Pandas

OpenAI GPT-4

Matplotlib (via Streamlit charting)

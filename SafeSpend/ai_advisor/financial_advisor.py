# ---------------------------
# AI Financial Advisor
# ---------------------------
class OpenAIFinancialAdvisor:
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

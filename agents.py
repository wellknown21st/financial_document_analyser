# agents.py
import os
from dotenv import load_dotenv
from crewai import Agent
from langchain_openai import ChatOpenAI
from tools import pdf_tool, search_tool  # FIXED: Imports remain the same, tools.py handles the dynamic creation

# Load environment variables
load_dotenv()

# -----------------------------
# OpenAI LLM
# -----------------------------
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise EnvironmentError(
        "OPENAI_API_KEY environment variable not set. "
        "Please create a .env file with your OpenAI API key."
    )

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.1,
    api_key=api_key
)

# -----------------------------
# Create Agents
# -----------------------------
financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Provide comprehensive financial analysis and investment insights based on the user's query: {query}",
    verbose=True,
    memory=True,
    backstory=(
        "You are a seasoned financial analyst with over 15 years of experience in corporate finance, "
        "investment banking, and market analysis. You specialize in analyzing financial documents, "
        "identifying key financial metrics, and providing actionable investment recommendations."
    ),
    tools=[pdf_tool, search_tool],  # FIXED: Tools will be updated dynamically in main.py
    llm=llm,
    max_iter=3,
    allow_delegation=False
)

verifier = Agent(
    role="Financial Document Verifier",
    goal="Verify the authenticity and accuracy of financial documents and ensure data quality",
    verbose=True,
    memory=True,
    backstory=(
        "You are a meticulous financial document verification specialist with expertise in "
        "regulatory compliance, financial reporting standards, and document authentication."
    ),
    tools=[pdf_tool],
    llm=llm,
    max_iter=2,
    allow_delegation=False
)

investment_advisor = Agent(
    role="Investment Strategy Advisor",
    goal="Develop personalized investment strategies based on financial analysis and risk assessment",
    verbose=True,
    memory=True,
    backstory=(
        "You are a certified financial planner (CFP) with extensive experience in portfolio management "
        "and investment strategy development."
    ),
    tools=[pdf_tool, search_tool],
    llm=llm,
    max_iter=2,
    allow_delegation=False
)

risk_assessor = Agent(
    role="Risk Assessment Specialist",
    goal="Conduct thorough risk analysis and provide risk mitigation strategies",
    verbose=True,
    memory=True,
    backstory=(
        "You are a risk management professional with deep expertise in financial risk assessment, "
        "market volatility analysis, and regulatory compliance."
    ),
    tools=[pdf_tool],
    llm=llm,
    max_iter=2,
    allow_delegation=False
)
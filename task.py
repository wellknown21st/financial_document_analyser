# task.py

from crewai import Task
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from tools import pdf_tool, search_tool

# -----------------------------
# Main Financial Document Analysis Task
# -----------------------------

analyze_financial_document = Task(
    description="""
    Analyze the financial document provided at {file_path} and answer the user's query: {query}

    Your analysis should include:
    1. Extract key financial metrics and data from the document
    2. Identify trends, strengths, and areas of concern
    3. Provide context about the company's financial health
    4. Address the specific user query with relevant insights
    5. Use reliable financial analysis techniques and industry standards

    Base your analysis solely on the information contained in the financial document.
    Provide accurate, professional, and actionable insights.
    """,
    expected_output="""
    A comprehensive financial analysis report that includes:
    - Executive summary of key findings
    - Detailed financial metrics analysis
    - Risk assessment and opportunities identification
    - Specific answers to the user's query
    - Professional recommendations based on the analysis
    - Clear, well-structured presentation of findings
    """,
    agent=financial_analyst,
    tools=[pdf_tool, search_tool]
)

# -----------------------------
# Investment Analysis Task
# -----------------------------

investment_analysis = Task(
    description="""
    Based on the financial document analysis, provide investment recommendations that address: {query}

    Focus on:
    1. Investment opportunities identified from the financial data
    2. Valuation insights based on financial metrics
    3. Comparison with industry benchmarks and standards
    4. Risk-adjusted return considerations
    5. Timeline and strategy recommendations

    Ensure all recommendations are grounded in the actual financial data from the document.
    """,
    expected_output="""
    Professional investment analysis including:
    - Clear investment thesis based on financial data
    - Specific investment recommendations with rationale
    - Risk assessment and mitigation strategies
    - Target price ranges or valuation insights (if applicable)
    - Investment timeline and key milestones to monitor
    """,
    agent=investment_advisor,
    tools=[search_tool]
)

# -----------------------------
# Risk Assessment Task
# -----------------------------

risk_assessment = Task(
    description="""
    Conduct a comprehensive risk assessment based on the financial document analysis for: {query}

    Evaluate:
    1. Financial risks identified in the document
    2. Market and industry-specific risks
    3. Operational and strategic risks
    4. Regulatory and compliance considerations
    5. Risk mitigation recommendations

    Provide a balanced and professional risk evaluation.
    """,
    expected_output="""
    Detailed risk assessment report containing:
    - Risk categorization and prioritization
    - Quantitative risk metrics where available
    - Qualitative risk factors and their potential impact
    - Risk mitigation strategies and recommendations
    - Monitoring frameworks for ongoing risk management
    """,
    agent=risk_assessor,
    tools=[search_tool]
)

# -----------------------------
# Document Verification Task
# -----------------------------

verification = Task(
    description="""
    Verify the integrity and authenticity of the financial document and validate key data points.

    Check for:
    1. Document format and structure consistency
    2. Data completeness and accuracy indicators
    3. Compliance with financial reporting standards
    4. Identification of any anomalies or inconsistencies

    Ensure the document is suitable for financial analysis.
    """,
    expected_output="""
    Document verification report including:
    - Document authenticity assessment
    - Data quality and completeness evaluation
    - Compliance with reporting standards
    - Any identified issues or limitations
    - Recommendations for data interpretation
    """,
    agent=verifier,
    tools=[pdf_tool]
)
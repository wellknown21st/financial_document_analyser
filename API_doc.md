📄 Financial Document Analyzer – API Documentation
Overview

The Financial Document Analyzer is an AI-powered API that allows you to upload financial documents (PDFs, reports, statements) and receive structured insights, analysis, and answers to your queries.

It uses CrewAI Agents, PDFSearchTool, and Serper Search API to process documents and perform external searches when needed.

🔑 Authentication
Environment Variables Required:

OPENAI_API_KEY → Your OpenAI API Key (for LLM processing).

SERPER_API_KEY → Your Serper.dev API Key (for financial web searches).

Set them in your .env file:

OPENAI_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_serper_api_key_here

📂 Endpoints
1. Analyze Financial Document

Endpoint: /analyze

Method: POST

Description: Upload a financial document and get AI-generated analysis.

Request:
POST /analyze
Content-Type: multipart/form-data


Body Parameters:

Field	Type	Required	Description
file	File (PDF)	✅	The financial document you want to analyze.
Response:
{
  "status": "success",
  "summary": "This document contains quarterly earnings report for Q1 2024...",
  "key_points": [
    "Revenue increased by 12% compared to last quarter",
    "Net profit margin improved by 4%",
    "Operating expenses reduced by 7%"
  ],
  "insights": "The company is performing strongly in the technology segment..."
}

2. Ask Questions on Document

Endpoint: /ask

Method: POST

Description: Ask a natural language question about the uploaded document.

Request:
POST /ask
Content-Type: application/json


Body Parameters:

Field	Type	Required	Description
question	String	✅	The question you want to ask (e.g., “What is the total revenue?”).
doc_id	String	✅	The ID of the document you uploaded earlier.
Response:
{
  "status": "success",
  "answer": "The total revenue reported in Q1 2024 is $4.2 billion."
}

3. Search External Financial Data

Endpoint: /search

Method: GET

Description: Uses Serper API to fetch latest financial news or insights.

Request:
GET /search?query=Tesla Q2 earnings

Response:
{
  "status": "success",
  "results": [
    {
      "title": "Tesla beats Q2 earnings expectations",
      "url": "https://finance.yahoo.com/news/tesla-q2-earnings...",
      "snippet": "Tesla reported record profits in Q2 2024, beating analyst expectations..."
    },
    {
      "title": "Tesla financials breakdown",
      "url": "https://www.reuters.com/business/tesla-earnings...",
      "snippet": "Operating margin improved despite increased competition..."
    }
  ]
}

⚙️ Running the API
Start the server:
# Make sure venv is activated
python financial-document-analyzer-debug/main.py


API will run on:

http://127.0.0.1:5000

📌 Notes

Ensure all dependencies in requirements.txt are installed:

pip install -r requirements.txt

API supports only PDF files for now.
Responses may vary depending on document size and model behavior.
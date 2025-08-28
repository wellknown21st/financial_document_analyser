# tools.py
import os
from crewai_tools import PDFSearchTool, SerperDevTool
from dotenv import load_dotenv

# Load environment variables (for SERPER_API_KEY)
load_dotenv()

# -----------------------------
# PDF Tool: Reads PDF files - FIXED: Updated path to match README
# -----------------------------
def create_pdf_tool(pdf_path):
    """Create a PDF tool for the specified file path"""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    return PDFSearchTool(pdf=pdf_path)

# Default PDF tool - will be created only when needed to avoid import errors
pdf_tool = None  # FIXED: Don't create tool at import time, create when needed

# -----------------------------
# Search Tool: Web search (requires SERPER_API_KEY)
# -----------------------------
search_tool = SerperDevTool()
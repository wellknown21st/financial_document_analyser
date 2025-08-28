from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
import os
import uuid
import logging
from typing import Optional

from crewai import Crew, Process
from agents import financial_analyst
from task import analyze_financial_document
from tools import create_pdf_tool, search_tool  # FIXED: Import the dynamic PDF tool creator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Financial Document Analyzer",
    description="AI-powered financial document analysis using CrewAI",
    version="1.0.0"
)

# Configuration - FIXED: Updated default path to match README instructions
DEFAULT_PDF_PATH = os.path.join("data", "sample.pdf")  # FIXED: Changed from TSLA-Q2-2025-Update.pdf
UPLOAD_DIR = "data"

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

def run_crew(query: str, file_path: str) -> str:
    """
    Run the financial analysis crew with the given query and file path.
    
    Args:
        query: The analysis query from the user
        file_path: Path to the PDF file to analyze
        
    Returns:
        Analysis result as string
    """
    try:
        logger.info(f"Starting crew analysis for query: {query}")
        logger.info(f"Analyzing file: {file_path}")
        
        # FIXED: Create a dynamic PDF tool for the specific file
        dynamic_pdf_tool = create_pdf_tool(file_path)
        
        # Update the agent's tools dynamically
        financial_analyst.tools = [dynamic_pdf_tool, search_tool]
        
        # Create the crew with single agent and task
        financial_crew = Crew(
            agents=[financial_analyst],
            tasks=[analyze_financial_document],
            process=Process.sequential,
            verbose=True
        )
        
        # Execute the analysis
        result = financial_crew.kickoff(inputs={
            'query': query, 
            'file_path': file_path
        })
        
        logger.info("Crew analysis completed successfully")
        return str(result)
        
    except Exception as e:
        error_msg = f"Error in crew analysis: {str(e)}"
        logger.error(error_msg)
        return error_msg

@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "message": "Financial Document Analyzer API is running",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Extended health check with system status."""
    return {
        "status": "healthy",
        "service": "Financial Document Analyzer",
        "version": "1.0.0",
        "endpoints": {
            "analyze": "/analyze",
            "health": "/health"
        }
    }

@app.post("/analyze")
async def analyze_document_endpoint(
    file: Optional[UploadFile] = File(None),
    query: str = Form(default="Analyze this financial document for investment insights")
):
    """
    Analyze financial document and provide comprehensive investment recommendations.
    
    Args:
        file: Optional PDF file upload
        query: Analysis query (defaults to general analysis)
        
    Returns:
        JSON response with analysis results
    """
    file_path = DEFAULT_PDF_PATH
    temp_file_created = False
    
    try:
        # Validate and process uploaded file
        if file:
            # Validate file type
            if not file.filename or not file.filename.lower().endswith('.pdf'):
                raise HTTPException(
                    status_code=400, 
                    detail="Only PDF files are supported"
                )
            
            # Create unique filename for uploaded file
            file_id = str(uuid.uuid4())
            file_path = os.path.join(UPLOAD_DIR, f"financial_document_{file_id}.pdf")
            temp_file_created = True
            
            # Save uploaded file
            try:
                content = await file.read()
                with open(file_path, "wb") as f:
                    f.write(content)
                logger.info(f"Uploaded file saved to: {file_path}")
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to save uploaded file: {str(e)}"
                )
        else:
            # Check if default file exists
            if not os.path.exists(file_path):
                raise HTTPException(
                    status_code=404,
                    detail=f"Default financial document not found at {file_path}. Please upload a PDF file."
                )
        
        # Validate query
        if not query or not query.strip():
            query = "Analyze this financial document for investment insights"
        
        # Run the analysis
        logger.info(f"Starting analysis with query: {query}")
        analysis_result = run_crew(query=query.strip(), file_path=file_path)
        
        # Prepare response
        response_data = {
            "status": "success",
            "query": query,
            "analysis": analysis_result,
            "file_used": file.filename if file else os.path.basename(DEFAULT_PDF_PATH),
            "timestamp": str(uuid.uuid4())  # Simple timestamp alternative
        }
        
        logger.info("Analysis completed successfully")
        return JSONResponse(content=response_data)
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Unexpected error in analyze endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing financial document: {str(e)}"
        )
    finally:
        # Clean up temporary uploaded files
        if temp_file_created and file and os.path.exists(file_path):
            try:
                os.remove(file_path)
                logger.info(f"Cleaned up temporary file: {file_path}")
            except Exception as cleanup_error:
                logger.warning(f"Could not clean up file {file_path}: {str(cleanup_error)}")

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Custom 404 handler."""
    return JSONResponse(
        status_code=404,
        content={
            "status": "error",
            "message": "Endpoint not found",
            "available_endpoints": ["/", "/health", "/analyze"]
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Custom 500 handler."""
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal server error",
            "detail": "Please check the server logs for more information"
        }
    )

if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting Financial Document Analyzer API...")
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )
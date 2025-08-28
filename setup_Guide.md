# Quick Setup Guide - Financial Document Analyzer (Fixed Version)

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables
Create a `.env` file in the project root:
```bash
# .env file
OPENAI_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_serper_api_key_here  # Optional for web search
```

### 3. Prepare Sample Document
Create the `data` directory and add your financial document:
```bash
mkdir -p data
# Download Tesla's Q2 2025 report and save as data/sample.pdf
# OR add any financial PDF as data/sample.pdf
```

### 4. Run the Application
```bash
python main.py
```

The API will start on `http://localhost:8000`

## 📋 API Usage

### Analyze Default Document
```bash
curl -X POST "http://localhost:8000/analyze" \
  -F "query=What are the key financial highlights?"
```

### Upload and Analyze Custom Document  
```bash
curl -X POST "http://localhost:8000/analyze" \
  -F "file=@your_financial_document.pdf" \
  -F "query=Analyze the investment potential"
```

### Health Check
```bash
curl http://localhost:8000/health
```

## 🐛 Bug Fixes Applied

- ✅ Fixed install command typo in README
- ✅ Standardized file paths (sample.pdf)
- ✅ Implemented dynamic PDF tool creation  
- ✅ Enhanced error handling and logging
- ✅ Proper cleanup of temporary files

## 📊 Sample Queries

- "Analyze revenue trends and growth prospects"
- "What are the main financial risks?"
- "Provide investment recommendations"
- "Compare quarterly performance"
- "Assess the company's liquidity position"

## 🔧 Troubleshooting

**Error: Default document not found**
- Ensure `data/sample.pdf` exists or upload a file via the API

**Error: OpenAI API key not set**  
- Check your `.env` file and API key validity

**Error: PDF processing failed**
- Ensure the PDF is not encrypted or corrupted
- Try with a different PDF file

The system is now fully functional and ready to analyze financial documents! 🎉
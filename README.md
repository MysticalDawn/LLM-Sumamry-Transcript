# PDF Applicant Info Extractor

This FastAPI application processes PDF files containing applicant information and extracts key details using OpenAI's GPT-4 model.

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set up environment variables:

```bash
export OPENAI_API_KEY='your-api-key-here'
```

## Running the Application

Start the server:

```bash
uvicorn llm_report:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### POST /process

Process a PDF file to extract applicant information.

**Request:**

- Content-Type: multipart/form-data
- Body: PDF file upload

**Response:**

```json
{
    "tokens": number,
    "mode": "direct" | "RAG",
    "response": string
}
```

## Features

- Handles PDF files up to 4000 tokens directly
- Uses RAG (Retrieval Augmented Generation) for larger documents
- Extracts GPA, intended major, and test scores
- Includes error handling and input validation

"""
Secure version of llm_report.py with enhanced security features.
This file demonstrates security best practices for production deployment.
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import fitz
import tiktoken
import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from fpdf import FPDF
import magic  # python-magic for file type validation

load_dotenv()

app = FastAPI()

# SECURITY: Configure CORS properly for production
# Replace with your actual frontend domain
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # Restrict to specific origins
    allow_credentials=True,
    allow_methods=["POST"],  # Only allow necessary methods
    allow_headers=["*"],
)

# SECURITY: File size and validation constants
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_MIME_TYPES = ["application/pdf"]

enc = tiktoken.encoding_for_model("gpt-4")

# SECURITY: Validate API key exists
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is required")

llm = ChatOpenAI(
    model_name="gpt-4",
    temperature=0,
    api_key=api_key,
)
embedding_model = OpenAIEmbeddings(api_key=api_key)

MAX_TOKENS = 4000


def validate_pdf_file(file: UploadFile, content: bytes) -> None:
    """
    Validate uploaded file for security.

    Args:
        file: The uploaded file
        content: File content bytes

    Raises:
        HTTPException: If validation fails
    """
    # Check file size
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {MAX_FILE_SIZE / 1024 / 1024}MB",
        )

    # Check file extension
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    # Verify actual file type (not just extension)
    try:
        mime = magic.from_buffer(content, mime=True)
        if mime not in ALLOWED_MIME_TYPES:
            raise HTTPException(
                status_code=400, detail=f"Invalid file type. Expected PDF, got {mime}"
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail="Could not verify file type")


@app.post("/process")
async def process_pdf(file: UploadFile = File(...)):
    """
    Process a PDF file and extract applicant information.

    Args:
        file: Uploaded PDF file

    Returns:
        dict: Processing results including tokens, mode, and extracted info
    """
    try:
        pdf_bytes = await file.read()

        # SECURITY: Validate file
        validate_pdf_file(file, pdf_bytes)

        # Process PDF
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = "\n".join([page.get_text() for page in doc])
        doc.close()

        if not text.strip():
            raise HTTPException(
                status_code=400,
                detail="PDF appears to be empty or contains no extractable text",
            )

        token_count = len(enc.encode(text))

        if token_count <= MAX_TOKENS:
            prompt = f"Extract applicant info from this text:\n\n{text}"
            response = llm.predict(prompt)

            # Generate PDF output
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            lines = response.split("\n")
            for line in lines:
                if len(line) > 80:
                    words = line.split()
                    current_line = ""
                    for word in words:
                        if len(current_line + " " + word) < 80:
                            current_line += " " + word
                        else:
                            pdf.cell(
                                0, 10, txt=current_line.strip(), ln=True, align="L"
                            )
                            current_line = word
                    if current_line:
                        pdf.cell(0, 10, txt=current_line.strip(), ln=True, align="L")
                else:
                    pdf.cell(0, 10, txt=line, ln=True, align="L")

            pdf.output("output.pdf", "F")
            return {"tokens": token_count, "mode": "direct", "response": response}

        # Use RAG for larger documents
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_text(text)
        vectordb = FAISS.from_texts(chunks, embedding_model)
        retriever = vectordb.as_retriever()

        qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
        response = qa.run("Extract applicant GPA, intended major, and test scores.")

        # Generate PDF output
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        lines = response.split("\n")
        for line in lines:
            if len(line) > 80:
                words = line.split()
                current_line = ""
                for word in words:
                    if len(current_line + " " + word) < 80:
                        current_line += " " + word
                    else:
                        pdf.cell(0, 10, txt=current_line.strip(), ln=True, align="L")
                        current_line = word
                if current_line:
                    pdf.cell(0, 10, txt=current_line.strip(), ln=True, align="L")
            else:
                pdf.cell(0, 10, txt=line, ln=True, align="L")

        pdf.output("output.pdf", "F")
        return {"tokens": token_count, "mode": "RAG", "response": response}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

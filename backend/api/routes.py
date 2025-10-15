"""API routes."""

from fastapi import APIRouter, File, UploadFile, HTTPException

from backend.utils import validate_pdf_file
from backend.services import pdf_processor, llm_service, pdf_generator

router = APIRouter()


@router.post("/process")
async def process_pdf(file: UploadFile = File(...)):
    """
    Process a PDF file and extract applicant information.

    Args:
        file: Uploaded PDF file

    Returns:
        dict: Processing results including tokens, mode, and extracted info
    """
    try:
        # Read file content
        pdf_bytes = await file.read()

        # Validate file
        validate_pdf_file(file, pdf_bytes)

        # Extract text from PDF
        text = pdf_processor.extract_text(pdf_bytes)

        # Count tokens
        token_count = pdf_processor.count_tokens(text)

        # Determine processing mode and extract information
        if pdf_processor.should_use_rag(token_count):
            # Use RAG for large documents
            response = llm_service.extract_with_rag(text)
            mode = "RAG"
        else:
            # Direct processing for small documents
            response = llm_service.extract_direct(text)
            mode = "direct"

        # Generate PDF report
        output_path = pdf_generator.generate_report(response)

        return {
            "tokens": token_count,
            "mode": mode,
            "response": response,
            "output_file": output_path,
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "pdf-extractor"}

"""PDF processing service."""

import fitz
import tiktoken
from typing import Tuple

from backend.config import settings


class PDFProcessor:
    """Service for processing PDF files."""

    def __init__(self):
        """Initialize PDF processor."""
        self.encoder = tiktoken.encoding_for_model(settings.MODEL_NAME)

    def extract_text(self, pdf_bytes: bytes) -> str:
        """
        Extract text from PDF bytes.

        Args:
            pdf_bytes: PDF file content as bytes

        Returns:
            Extracted text from all pages

        Raises:
            ValueError: If PDF is empty or invalid
        """
        try:
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            text = "\n".join([page.get_text() for page in doc])
            doc.close()

            if not text.strip():
                raise ValueError(
                    "PDF appears to be empty or contains no extractable text"
                )

            return text
        except Exception as e:
            raise ValueError(f"Failed to extract text from PDF: {str(e)}")

    def count_tokens(self, text: str) -> int:
        """
        Count tokens in text.

        Args:
            text: Text to count tokens for

        Returns:
            Number of tokens
        """
        return len(self.encoder.encode(text))

    def should_use_rag(self, token_count: int) -> bool:
        """
        Determine if RAG should be used based on token count.

        Args:
            token_count: Number of tokens in document

        Returns:
            True if RAG should be used, False otherwise
        """
        return token_count > settings.MAX_TOKENS


pdf_processor = PDFProcessor()

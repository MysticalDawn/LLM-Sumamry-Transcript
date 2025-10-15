"""File validation utilities."""

from fastapi import HTTPException, UploadFile
from typing import List
import magic

from backend.config import settings


def validate_file_size(content: bytes) -> None:
    """
    Validate file size.

    Args:
        content: File content bytes

    Raises:
        HTTPException: If file is too large
    """
    if len(content) > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {settings.MAX_FILE_SIZE / 1024 / 1024}MB",
        )


def validate_file_extension(filename: str) -> None:
    """
    Validate file extension.

    Args:
        filename: Name of the file

    Raises:
        HTTPException: If extension is not allowed
    """
    if not filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    extension = "." + filename.lower().split(".")[-1] if "." in filename else ""
    if extension not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File extension not allowed. Allowed: {', '.join(settings.ALLOWED_EXTENSIONS)}",
        )


def validate_mime_type(content: bytes) -> None:
    """
    Validate file MIME type.

    Args:
        content: File content bytes

    Raises:
        HTTPException: If MIME type is not allowed
    """
    try:
        mime = magic.from_buffer(content, mime=True)
        if mime not in settings.ALLOWED_MIME_TYPES:
            raise HTTPException(
                status_code=400, detail=f"Invalid file type. Expected PDF, got {mime}"
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail="Could not verify file type")


def validate_pdf_file(file: UploadFile, content: bytes) -> None:
    """
    Comprehensive PDF file validation.

    Args:
        file: The uploaded file
        content: File content bytes

    Raises:
        HTTPException: If validation fails
    """
    validate_file_size(content)
    validate_file_extension(file.filename or "")
    validate_mime_type(content)

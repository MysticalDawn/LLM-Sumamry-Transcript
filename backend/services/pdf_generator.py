"""PDF generation service."""

import os
from fpdf import FPDF
from typing import Optional

from backend.config import settings


class PDFGenerator:
    """Service for generating PDF reports."""

    def __init__(self):
        """Initialize PDF generator."""
        # Ensure output directory exists
        os.makedirs(settings.OUTPUT_DIR, exist_ok=True)

    def generate_report(self, content: str, output_filename: str = "output.pdf") -> str:
        """
        Generate a PDF report from text content.

        Args:
            content: Text content to include in PDF
            output_filename: Name of output file

        Returns:
            Path to generated PDF file
        """
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        lines = content.split("\n")
        for line in lines:
            self._add_line_to_pdf(pdf, line)

        output_path = os.path.join(settings.OUTPUT_DIR, output_filename)
        pdf.output(output_path, "F")
        return output_path

    def _add_line_to_pdf(self, pdf: FPDF, line: str, max_width: int = 80) -> None:
        """
        Add a line to PDF with word wrapping.

        Args:
            pdf: FPDF instance
            line: Line of text to add
            max_width: Maximum characters per line
        """
        if len(line) > max_width:
            words = line.split()
            current_line = ""
            for word in words:
                if len(current_line + " " + word) < max_width:
                    current_line += " " + word
                else:
                    pdf.cell(0, 10, txt=current_line.strip(), ln=True, align="L")
                    current_line = word
            if current_line:
                pdf.cell(0, 10, txt=current_line.strip(), ln=True, align="L")
        else:
            pdf.cell(0, 10, txt=line, ln=True, align="L")


pdf_generator = PDFGenerator()

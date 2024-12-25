from json import dumps
import requests
from langchain.tools import tool
from pydantic import BaseModel, Field
from markdown2 import markdown
from pathlib import Path
import os
import pdfkit
import uuid
from dotenv import load_dotenv
load_dotenv()

PATH_WKHTMLTOPDF = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
PDFKIT_CONFIG = pdfkit.configuration(wkhtmltopdf=PATH_WKHTMLTOPDF)
OUTPUT_DIRECTORY = Path(__file__).parent.parent.parent / "output"


class MarkdownToPDFInput(BaseModel):
    markdown_text: str = Field(
        description="Markdown text to convert to PDF, provided in valid markdown format."
    )


def generate_html_text(markdown_text: str) -> str:
    """Convert markdown text to HTML text and use an image as the cover."""
    markdown_text = markdown_text.replace("file:///", "").replace("file://", "")
    html_text = markdown(markdown_text)

    # Path to the image
    image_path = OUTPUT_DIRECTORY.parent / "images" / "image.png"

    html_text = f"""
    <html>
    <head>
    </head>
    <body>
    <div class="cover">
        <img src="file:///{image_path}" alt="Cover Image">
    </div>
    <div class="content">
    {html_text}
    </div>
    </body>
    </html>
    """
    return html_text

#@tool("markdown_to_pdf_file", args_schema=MarkdownToPDFInput)
def markdown_to_pdf_file(markdown_text: str) -> str:
    """Convert markdown text to a PDF file. Takes valid markdown as a string as input and will return a string file-path to the generated PDF."""
    html_text = generate_html_text(markdown_text)
    unique_id: uuid.UUID = uuid.uuid4()
    pdf_path = OUTPUT_DIRECTORY / f"{unique_id}.pdf"
    options = {
        "no-stop-slow-scripts": True,
        "print-media-type": True,
        "encoding": "UTF-8",
        "enable-local-file-access": "",
        "disable-smart-shrinking": ""  # Try adding this option
    }
    pdfkit.from_string(
        html_text, str(pdf_path), configuration=PDFKIT_CONFIG, options=options
    )
    if os.path.exists(pdf_path):
        return str(pdf_path)
    else:
        return "Could not generate PDF, please check your input and try again."



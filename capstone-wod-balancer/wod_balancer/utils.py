import io
import markdown
from xhtml2pdf import pisa

def save_markdown_to_pdf(markdown_text, output_filename):
    """
    Converts markdown text to a PDF file.
    """
    # Convert Markdown to HTML
    html_text = markdown.markdown(markdown_text)
    
    # Add some basic styling
    full_html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: sans-serif; font-size: 12px; }}
            h1, h2, h3 {{ color: #333; }}
            p {{ line-height: 1.5; }}
            ul {{ margin-bottom: 10px; }}
        </style>
    </head>
    <body>
        {html_text}
    </body>
    </html>
    """
    
    # Generate PDF
    with open(output_filename, "wb") as result_file:
        pisa_status = pisa.CreatePDF(
            io.BytesIO(full_html.encode("utf-8")),
            dest=result_file
        )
    
    if pisa_status.err:
        print(f"Error generating PDF: {pisa_status.err}")
    else:
        print(f"PDF saved successfully to {output_filename}")

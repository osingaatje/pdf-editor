import fitz  # pymupdf

FILE_IN_PATH = "files/2024-03-26_Sponsorpakketten_JFO_tickets.pdf"
FILE_OUT_PATH = "edit/2024-03-26_Sponsorpakketten_JFO_tickets-EDITED-PyMuPDF.pdf"

REPLACEMENTS :dict[str, str] = {"#2025_000111222333": "#2025_1234567890123"}

def replace_text_in_pdf(input_file, output_file, replacements):
    doc : fitz.Document = fitz.open(input_file)

    for page in doc:
        text = page.get_text("text")
        for old, new in replacements.items():
            text = text.replace(old, new)
        page.insert_text((50, 50), text, fontsize=12)

    doc.save(output_file)
    doc.close()

if __name__ == "__main__":
    replace_text_in_pdf(FILE_IN_PATH, FILE_OUT_PATH, REPLACEMENTS)
# pdf_saver.py
from fpdf import FPDF
import os

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Sunbeam Data Report', 0, 1, 'C')
        self.ln(5)

    def chapter_title(self, label):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        # Ensure label is string and clean
        clean_label = str(label).encode('latin-1', 'replace').decode('latin-1')
        self.cell(0, 6, clean_label, 0, 1, 'L', 1)
        self.ln(2)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        # Clean text to handle Unicode characters not supported by standard PDF fonts
        clean_body = str(body).encode('latin-1', 'replace').decode('latin-1')
        self.multi_cell(0, 5, clean_body)
        self.ln()

def save_to_pdf(data, filename):
    # Ensure filename ends with .pdf
    if not filename.endswith('.pdf'):
        filename = os.path.splitext(filename)[0] + '.pdf'

    pdf = PDFReport()
    pdf.add_page()
    
    if isinstance(data, dict):
        process_dict(pdf, data)
    elif isinstance(data, list):
        process_list(pdf, data)

    pdf.output(filename)
    print(f"Successfully saved PDF to: {filename}")

def process_dict(pdf, data, indent=0):
    for key, value in data.items():
        key_str = str(key).upper()
        pdf.chapter_title(key_str)
        
        if isinstance(value, list):
            process_list(pdf, value)
        elif isinstance(value, dict):
            process_dict(pdf, value, indent + 1)
        else:
            pdf.chapter_body(str(value))

def process_list(pdf, data_list):
    for item in data_list:
        if isinstance(item, dict):
            # Format dictionary items (like table rows) cleanly
            text_lines = []
            for k, v in item.items():
                text_lines.append(f"{k}: {v}")
            pdf.chapter_body(" | ".join(text_lines))
            pdf.ln(1)
        else:
            pdf.chapter_body(str(item))
from fpdf import FPDF

def save_code_as_pdf(code_text, filename="flowchart_code.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Courier", size=12)

    # اضافه کردن متن کد خط‌به‌خط
    for line in code_text.split("\n"):
        pdf.cell(0, 8, txt=line, ln=True)

    pdf.output(filename)
    return filename

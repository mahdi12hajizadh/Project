from fpdf import FPDF


def save_code_as_pdf(code_text, filename="flowchart_code.pdf"):
    """
    ذخیره کد تولیدشده به صورت PDF.

    دو مشکل نسخه‌ی قبلی:
    1) اگر متن کد شامل کاراکتر غیر از حروف لاتین باشه (مثلاً فارسی)،
       فونت پایه‌ی Courier کرش می‌کرد چون فقط از Latin-1 پشتیبانی می‌کنه.
    2) خط‌های طولانی به‌جای شکسته‌شدن، از لبه‌ی صفحه بیرون می‌زدن و بریده می‌شدن،
       چون از pdf.cell() به‌جای multi_cell() استفاده شده بود.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Courier", size=11)

    page_width = pdf.w - pdf.l_margin - pdf.r_margin

    for line in code_text.split("\n"):
        safe_line = _make_pdf_safe(line)
        if safe_line == "":
            pdf.ln(6)
            continue
        pdf.multi_cell(page_width, 6, txt=safe_line)

    pdf.output(filename)
    return filename


def _make_pdf_safe(text: str) -> str:
    """
    تبدیل متن به چیزی که فونت پایه‌ی Courier (فقط Latin-1) بتونه رندرش کنه.
    کاراکترهای پشتیبانی‌نشده (مثل فارسی) به جای کرش‌کردن، با '?' جایگزین می‌شن.
    """
    return text.encode("latin-1", "replace").decode("latin-1")

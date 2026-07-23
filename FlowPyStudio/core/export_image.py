from PIL import ImageGrab

def save_canvas_as_image(canvas, filename="flowchart.png"):
    """
    ذخیره تصویر از Canvas به صورت PNG بدون نیاز به Ghostscript.
    فقط محدوده‌ی دقیق Canvas ذخیره می‌شود.
    """

    # آپدیت Canvas برای گرفتن اندازه دقیق
    canvas.update()

    # گرفتن مختصات دقیق Canvas روی صفحه
    x = canvas.winfo_rootx()
    y = canvas.winfo_rooty()
    w = canvas.winfo_width()
    h = canvas.winfo_height()

    # گرفتن تصویر از محدوده Canvas
    img = ImageGrab.grab(bbox=(x, y, x + w, y + h))

    # ذخیره تصویر
    img.save(filename, "PNG")

    return filename

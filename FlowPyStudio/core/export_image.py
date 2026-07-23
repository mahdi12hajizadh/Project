from PIL import Image, ImageDraw


def save_canvas_as_image(canvas, filename="flowchart.png"):
    """
    ساخت تصویر PNG مستقیماً از روی آیتم‌های واقعی Canvas
    (بدون گرفتن اسکرین‌شات از صفحه).

    این روش وابسته به اسکرین‌شات نیست، پس:
    - اگر پنجره‌ی دیگری روی برنامه باشد تأثیری ندارد
    - در DPI Scaling های مختلف ویندوز درست کار می‌کند
    - حتی اگر پنجره کوچک/جابه‌جا شده باشد نتیجه درست است
    """
    canvas.update()

    width = canvas.winfo_width()
    height = canvas.winfo_height()
    if width <= 1 or height <= 1:
        try:
            width = int(canvas.cget("width"))
            height = int(canvas.cget("height"))
        except Exception:
            width, height = 800, 600

    bg_color = canvas.cget("bg") or "#000000"

    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    for item in canvas.find_all():
        item_type = canvas.type(item)
        coords = canvas.coords(item)
        if not coords:
            continue

        fill = canvas.itemcget(item, "fill") or None

        # فقط rectangle / oval / polygon گزینه‌ی outline دارند؛
        # line و text چنین گزینه‌ای ندارند و خواستنش خطای Tkinter می‌دهد
        if item_type in ("rectangle", "oval", "polygon"):
            outline = canvas.itemcget(item, "outline") or None
        else:
            outline = None

        try:
            line_width = int(round(float(canvas.itemcget(item, "width") or 1)))
        except (ValueError, TypeError):
            line_width = 1
        line_width = max(line_width, 1)

        if item_type == "rectangle":
            draw.rectangle(coords, fill=fill, outline=outline, width=line_width)

        elif item_type == "oval":
            draw.ellipse(coords, fill=fill, outline=outline, width=line_width)

        elif item_type == "polygon":
            draw.polygon(coords, fill=fill, outline=outline)

        elif item_type == "line":
            draw.line(coords, fill=fill or "white", width=line_width)
            # رسم سر پیکان به‌صورت دستی (چون PIL پیکان آماده نداره)
            if len(coords) >= 4:
                _draw_arrowhead(draw, coords, fill or "white")

        elif item_type == "text":
            text = canvas.itemcget(item, "text")
            if text:
                text_fill = fill or "black"
                x, y = coords[0], coords[1]
                try:
                    bbox = draw.textbbox((0, 0), text)
                    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
                except Exception:
                    tw, th = 0, 0
                draw.text((x - tw / 2, y - th / 2), text, fill=text_fill)

    img.save(filename, "PNG")
    return filename


def _draw_arrowhead(draw, coords, color, size=10, angle_deg=25):
    """رسم یک سر پیکان مثلثی ساده در انتهای خط"""
    import math

    x1, y1 = coords[-4], coords[-3]
    x2, y2 = coords[-2], coords[-1]

    angle = math.atan2(y2 - y1, x2 - x1)
    a = math.radians(angle_deg)

    p1 = (
        x2 - size * math.cos(angle - a),
        y2 - size * math.sin(angle - a),
    )
    p2 = (
        x2 - size * math.cos(angle + a),
        y2 - size * math.sin(angle + a),
    )

    draw.polygon([(x2, y2), p1, p2], fill=color)

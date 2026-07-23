import ttkbootstrap as tb
from ui import FlowPyUI
from ui import load_saved_theme

def main():
    saved_theme = load_saved_theme()

    # انتخاب تم ذخیره‌شده
    if saved_theme == "dark":
        root = tb.Window(themename="darkly")
    else:
        root = tb.Window(themename="flatly")

    app = FlowPyUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

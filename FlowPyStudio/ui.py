import os
import json
import tkinter as tk
from tkinter import messagebox, filedialog

import ttkbootstrap as tb
from ttkbootstrap.constants import *

from core.canvas_manager import CanvasManager
from core.event_handler import EventHandler
from core.state_manager import StateManager
from engine.code_generator import CodeGenerator
from engine.code_runner import CodeRunner
from models.flowchart import Flowchart
from theme.theme_manager import ThemeManager
from storage.file_manager import FileManager
from core.export_image import save_canvas_as_image
from core.export_pdf import save_code_as_pdf

CONFIG_FILE = "theme_config.json"


def load_saved_theme():
    """خواندن تم ذخیره‌شده از فایل تنظیمات"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("theme", "dark")
        except:
            return "dark"
    return "dark"


def save_theme(theme: str):
    """ذخیره تم در فایل تنظیمات"""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump({"theme": theme}, f)
    except:
        pass


class FlowPyUI:
    def __init__(self, root: tb.Window):
        # پنجره اصلی
        self.root = root
        self.root.title("FlowPy Studio")
        self.root.geometry("1200x800")

        # تم‌ها
        self.dark_theme = "darkly"
        self.light_theme = "flatly"

        # خواندن تم ذخیره‌شده
        saved_theme = load_saved_theme()
        self.current_theme_mode = saved_theme  # "dark" یا "light"

        # اعمال تم اولیه روی ttkbootstrap
        if self.current_theme_mode == "dark":
            self.root.style.theme_use(self.dark_theme)
        else:
            self.root.style.theme_use(self.light_theme)

        # اجزای اصلی برنامه
        self.flowchart = Flowchart()
        self.canvas_manager = CanvasManager(self.flowchart)
        self.event_handler = EventHandler(self.canvas_manager, self.flowchart)
        self.event_handler.set_ui(self)
        self.state_manager = StateManager(self.flowchart)
        self.canvas_manager.state_manager = self.state_manager

        self.theme_manager = ThemeManager()
        self.file_manager = FileManager()
        self.code_generator = CodeGenerator()
        self.code_runner = CodeRunner()

        # ساخت رابط کاربری
        self.setup_ui()
        self.setup_menu()
        self.apply_theme()

    def _panel_bootstyle(self):
        """استایل مناسب پنل‌ها بر اساس حالت روشن/تیره فعلی"""
        return DARK if self.current_theme_mode == "dark" else LIGHT

    # ---------------------------------------------------------
    # UI SETUP
    # ---------------------------------------------------------
    def setup_ui(self):
        main_container = tb.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # نوار ابزار بالا
        self.toolbar = tb.Frame(main_container)
        self.toolbar.pack(fill=tk.X, pady=(0, 5))

        buttons = [
            ("🖱 Select", lambda: self.set_tool("select")),
            ("🔵 Start", lambda: self.set_tool("start")),
            ("⚙️ Process", lambda: self.set_tool("process")),
            ("🔁 For Loop", lambda: self.set_tool("for_loop")),
            ("🔂 While Loop", lambda: self.set_tool("while_loop")),
            ("🔀 Decision", lambda: self.set_tool("decision")),
            ("📥 IO", lambda: self.set_tool("io")),
            ("➡️ Arrow", lambda: self.set_tool("arrow")),
            ("↩ Undo", self.undo),
            ("↪ Redo", self.redo),
            ("🖼 Save PNG", self.save_png),
            ("📄 Save PDF", self.save_pdf),
            ("🌗 Toggle Theme", self.toggle_theme_mode),
            
        ]

        for text, cmd in buttons:
            tb.Button(self.toolbar, text=text, command=cmd, bootstyle=SECONDARY).pack(side=tk.LEFT, padx=3)

        # ناحیه‌ی Canvas
        panel_style = self._panel_bootstyle()
        self.canvas_frame = tb.Frame(main_container, bootstyle=panel_style)
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        canvas_frame = self.canvas_frame

        self.canvas = tk.Canvas(
            canvas_frame,
            bg="#000000",
            width=800,
            height=600,
            highlightthickness=2,
            highlightbackground="#333333"
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas_manager.set_canvas(self.canvas)

        # رویدادها
        self.canvas.bind("<Button-1>", self.event_handler.on_click)
        self.canvas.bind("<B1-Motion>", self.event_handler.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.event_handler.on_release)
        self.canvas.bind("<KeyPress>", self.event_handler.on_keypress)
        self.canvas.bind("<Double-Button-1>", self.event_handler.on_double_click)
        self.canvas.focus_set()

        # پنل راست (کد و خروجی)
        self.right_panel = tb.Frame(main_container, width=400, bootstyle=panel_style)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(5, 0))
        self.right_panel.pack_propagate(False)
        right_panel = self.right_panel

        self.code_label = tb.Label(right_panel, text="Generated Code:", bootstyle=INVERSE)
        self.code_label.pack(anchor=tk.W)
        self.code_text = tk.Text(right_panel, height=15, bg="#000000", fg="#FFFFFF")
        self.code_text.pack(fill=tk.BOTH, expand=True)

        self.output_label = tb.Label(right_panel, text="Output:", bootstyle=INVERSE)
        self.output_label.pack(anchor=tk.W)
        self.output_text = tk.Text(right_panel, height=10, bg="#000000", fg="#FFFFFF")
        self.output_text.pack(fill=tk.BOTH, expand=True)

        control_frame = tb.Frame(right_panel)
        control_frame.pack(fill=tk.X, pady=5)

        tb.Button(control_frame, text="Generate Code", command=self.generate_code, bootstyle=SUCCESS).pack(side=tk.LEFT, padx=2)
        tb.Button(control_frame, text="Run Code", command=self.run_code, bootstyle=INFO).pack(side=tk.LEFT, padx=2)
        tb.Button(control_frame, text="Clear Output", command=self.clear_output, bootstyle=WARNING).pack(side=tk.LEFT, padx=2)

        self.status_bar = tb.Label(self.root, text="Ready - Click on canvas to draw", bootstyle=panel_style)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    # ---------------------------------------------------------
    # MENU
    # ---------------------------------------------------------
    def setup_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)

        file_menu.add_command(label="New Project", command=self.new_project)
        file_menu.add_command(label="Save Project", command=self.save_project)
        file_menu.add_command(label="Load Project", command=self.load_project)
        file_menu.add_separator()
        file_menu.add_command(label="Export PNG", command=self.save_png)
        file_menu.add_command(label="Export PDF", command=self.save_pdf)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Edit
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.undo)
        edit_menu.add_command(label="Redo", command=self.redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Clear All", command=self.clear_all)

        # View
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Toggle Theme Mode", command=self.toggle_theme_mode)

        # Help
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    # ---------------------------------------------------------
    # TOOL ACTIONS
    # ---------------------------------------------------------
    def set_tool(self, tool: str):
        self.event_handler.current_tool = tool
        if tool != "arrow":
            self.canvas_manager.arrow_start = None
        self.status_bar.config(text=f"Tool: {tool}")

    def undo(self):
        if self.state_manager.undo():
            self.canvas_manager.render()
            self.status_bar.config(text="Undo done")
        else:
            self.status_bar.config(text="Nothing to undo")

    def redo(self):
        if self.state_manager.redo():
            self.canvas_manager.render()
            self.status_bar.config(text="Redo done")
        else:
            self.status_bar.config(text="Nothing to redo")

    # ---------------------------------------------------------
    # CODE GENERATION & EXECUTION
    # ---------------------------------------------------------
    def generate_code(self):
        try:
            code = self.code_generator.generate(self.flowchart)
            self.code_text.delete(1.0, tk.END)
            self.code_text.insert(1.0, code)
            self.status_bar.config(text="Code generated")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run_code(self):
        code = self.code_text.get(1.0, tk.END)
        if not code.strip():
            messagebox.showwarning("Warning", "Generate code first.")
            return

        try:
            output = self.code_runner.run(code)
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(1.0, output)
            self.status_bar.config(text="Code executed")
        except Exception as e:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(1.0, f"Error: {str(e)}")
            self.status_bar.config(text="Code execution failed")

    def clear_output(self):
        self.output_text.delete(1.0, tk.END)

    # ---------------------------------------------------------
    # PROJECT MANAGEMENT
    # ---------------------------------------------------------
    def new_project(self):
        if messagebox.askyesno("New Project", "Clear current project?"):
            self.flowchart.clear()
            self.canvas.delete("all")
            self.code_text.delete(1.0, tk.END)
            self.output_text.delete(1.0, tk.END)
            self.state_manager.clear()
            self.status_bar.config(text="New project created")

    def save_project(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".flowpy",
            filetypes=[("FlowPy Project", "*.flowpy"), ("All Files", "*.*")]
        )
        if filename:
            try:
                self.file_manager.save_project(self.flowchart, filename)
                self.status_bar.config(text=f"Project saved: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save project: {str(e)}")

    def load_project(self):
        filename = filedialog.askopenfilename(
            filetypes=[("FlowPy Project", "*.flowpy"), ("All Files", "*.*")]
        )
        if filename:
            try:
                self.flowchart = self.file_manager.load_project(filename)
                self.canvas_manager.flowchart = self.flowchart
                self.event_handler.flowchart = self.flowchart
                self.state_manager.flowchart = self.flowchart
                self.canvas_manager.render()
                self.status_bar.config(text=f"Project loaded: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load project: {str(e)}")

    # ---------------------------------------------------------
    # EXPORT
    # ---------------------------------------------------------
    def save_png(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png"), ("All Files", "*.*")]
        )
        if filename:
            try:
                save_canvas_as_image(self.canvas, filename)
                self.status_bar.config(text=f"Saved PNG: {filename}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def save_pdf(self):
        code = self.code_text.get(1.0, tk.END)
        if not code.strip():
            messagebox.showwarning("Warning", "Generate code first.")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF File", "*.pdf"), ("All Files", "*.*")]
        )
        if filename:
            try:
                save_code_as_pdf(code, filename)
                self.status_bar.config(text=f"Saved PDF: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save PDF: {str(e)}")

    # ---------------------------------------------------------
    # THEME
    # ---------------------------------------------------------
    def toggle_theme_mode(self):
        if self.current_theme_mode == "dark":
            self.current_theme_mode = "light"
            self.root.style.theme_use(self.light_theme)
            save_theme("light")
            self.status_bar.config(text="Theme: Light Mode")
        else:
            self.current_theme_mode = "dark"
            self.root.style.theme_use(self.dark_theme)
            save_theme("dark")
            self.status_bar.config(text="Theme: Dark Mode")

        self.apply_theme()

    def apply_theme(self):
        if self.current_theme_mode == "dark":
            bg = "#000000"
            fg = "#FFFFFF"
        else:
            bg = "#FFFFFF"
            fg = "#000000"

        self.canvas.config(bg=bg)
        self.code_text.config(bg=bg, fg=fg)
        self.output_text.config(bg=bg, fg=fg)

        # هماهنگ‌سازی پنل‌ها و نوار وضعیت با حالت روشن/تیره فعلی
        panel_style = self._panel_bootstyle()
        self.canvas_frame.configure(bootstyle=panel_style)
        self.right_panel.configure(bootstyle=panel_style)
        self.status_bar.configure(bootstyle=panel_style)

    # ---------------------------------------------------------
    # OTHER
    # ---------------------------------------------------------
    def clear_all(self):
        if messagebox.askyesno("Clear All", "Remove all shapes and arrows?"):
            self.flowchart.clear()
            self.canvas.delete("all")
            self.state_manager.clear()
            self.status_bar.config(text="Cleared all")

    def show_about(self):
        messagebox.showinfo(
            "About FlowPy Studio",
            "FlowPy Studio v1.0\n\n"
            "A flowchart-based Python development environment\n"
            "Design → Generate → Run\n\n"
            "Created by Mahdi_Hajizadh"
        )

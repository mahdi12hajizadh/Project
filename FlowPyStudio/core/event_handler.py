import tkinter as tk
from tkinter import simpledialog
from models.shapes import ShapeType


class EventHandler:
    def __init__(self, canvas_manager, flowchart):
        self.canvas_manager = canvas_manager
        self.flowchart = flowchart
        self.drag_start = None
        self.dragging_item = None
        self.current_tool = "select"
        self.ui = None

    def set_ui(self, ui):
        self.ui = ui

    def on_click(self, event):
        print(f"Click at: {event.x}, {event.y}")
        self.canvas_manager.canvas.focus_set()
        self.canvas_manager.deselect_all()

        tool = self.current_tool
        print(f"TOOL: {tool}")

        # ---------- حالت Arrow ----------
        if tool == "arrow":
            print("Arrow mode activated!")
            items = self.canvas_manager.canvas.find_overlapping(
                event.x - 2, event.y - 2, event.x + 2, event.y + 2
            )
            print(f"Items under click: {len(items)}")

            # فقط آیتم‌هایی که tag "shape" دارند
            shape_items = [
                item for item in items
                if "shape" in self.canvas_manager.canvas.gettags(item)
            ]

            for item in shape_items:
                tags = self.canvas_manager.canvas.gettags(item)
                print(f"Item tags: {tags}")
                for tag in tags:
                    if tag.startswith("shape_"):
                        shape_id = tag.replace("shape_", "")
                        print(f"Arrow: clicked on shape {shape_id}")

                        if self.canvas_manager.arrow_start is None:
                            self.canvas_manager.arrow_start = shape_id
                            if self.ui:
                                self.ui.status_bar.config(
                                    text=f"Arrow: select target shape"
                                )
                            print(f"Arrow start: {shape_id}")
                            return
                        else:
                            from_id = self.canvas_manager.arrow_start
                            if from_id != shape_id:
                                edge = self.canvas_manager.add_arrow(from_id, shape_id)
                                if edge:
                                    if self.ui:
                                        self.ui.status_bar.config(
                                            text=f"Arrow created from {from_id} to {shape_id}"
                                        )
                                    print(f"Arrow created: {from_id} -> {shape_id}")
                                else:
                                    if self.ui:
                                        self.ui.status_bar.config(
                                            text="Arrow already exists!"
                                        )
                            else:
                                if self.ui:
                                    self.ui.status_bar.config(
                                        text="Cannot connect to itself!"
                                    )
                            self.canvas_manager.arrow_start = None
                            return

            # اگر هیچ shape پیدا نشد و قبلاً start تنظیم شده بود → لغو
            if self.canvas_manager.arrow_start is not None:
                self.canvas_manager.arrow_start = None
                if self.ui:
                    self.ui.status_bar.config(text="Arrow cancelled")
                print("Arrow cancelled")
            return

        # ---------- ابزارهای دیگر ----------
        items = self.canvas_manager.canvas.find_overlapping(
            event.x - 2, event.y - 2, event.x + 2, event.y + 2
        )
        print(f"Items under click: {len(items)}")

        # فقط آیتم‌هایی که tag "shape" دارند
        shape_items = [
            item for item in items
            if "shape" in self.canvas_manager.canvas.gettags(item)
        ]

        for item in shape_items:
            tags = self.canvas_manager.canvas.gettags(item)
            print(f"Item tags: {tags}")
            for tag in tags:
                if tag.startswith("shape_"):
                    shape_id = tag.replace("shape_", "")
                    print(f"Found shape: {shape_id}")
                    shape = self.flowchart.get_node(shape_id)
                    if shape:
                        print(f"Shape found in model: {shape.id}")
                        self.canvas_manager.select_item(event.x, event.y)
                        self.drag_start = (event.x, event.y)
                        self.dragging_item = item
                        print(f"dragging_item set to: {self.dragging_item}")
                        return

        print("No shape found")

        # اگر روی شکل کلیک نشده و ابزار select نیست، شکل بساز
        if tool != "select":
            shape_type = self._tool_to_shape_type(tool)
            if shape_type:
                print(f"Making {shape_type}")
                self.canvas_manager.create_shape(shape_type, event.x, event.y)
                self.canvas_manager.select_item(event.x, event.y)
            else:
                print(f"Unknown tool: {tool}")
        else:
            print("Tool is select - no shape")
            self.canvas_manager.select_item(event.x, event.y)

    def on_double_click(self, event):
        print(f"Double click at: {event.x}, {event.y}")
        items = self.canvas_manager.canvas.find_overlapping(
            event.x - 2, event.y - 2, event.x + 2, event.y + 2
        )
        for item in items:
            tags = self.canvas_manager.canvas.gettags(item)
            for tag in tags:
                if tag.startswith("shape_"):
                    shape_id = tag.replace("shape_", "")
                    shape = self.flowchart.get_node(shape_id)
                    if shape:
                        self._edit_shape_text(shape)
                        return

    def _edit_shape_text(self, shape):
        new_text = simpledialog.askstring(
            "Edit Text",
            "Enter new text:",
            initialvalue=shape.text
        )
        if new_text is not None:
            shape.text = new_text
            self.canvas_manager.render()
            if self.ui:
                self.ui.status_bar.config(text=f"Text updated to: {new_text}")

    def on_drag(self, event):
        if self.dragging_item:
            dx = event.x - self.drag_start[0]
            dy = event.y - self.drag_start[1]
            if dx != 0 or dy != 0:
                tags = self.canvas_manager.canvas.gettags(self.dragging_item)
                for tag in tags:
                    if tag.startswith("shape_"):
                        shape_id = tag.replace("shape_", "")
                        self.canvas_manager.move_shape(shape_id, dx, dy)
                        self.drag_start = (event.x, event.y)

    def on_release(self, event):
        self.dragging_item = None
        self.drag_start = None

    def on_keypress(self, event):
        if event.keysym == "Delete":
            self.canvas_manager.delete_selected()

    def _tool_to_shape_type(self, tool):
        mapping = {
            "start": ShapeType.START,
            "process": ShapeType.PROCESS,
            "decision": ShapeType.DECISION,
            "io": ShapeType.INPUT_OUTPUT,
            "text": ShapeType.TEXT,
            "for_loop": ShapeType.FOR_LOOP,
            "while_loop": ShapeType.WHILE_LOOP,
        }
        return mapping.get(tool)

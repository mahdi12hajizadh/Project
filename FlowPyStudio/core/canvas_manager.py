import tkinter as tk
from models.shapes import Shape, ShapeType
from models.arrows import Arrow

class CanvasManager:
    def __init__(self, flowchart):
        self.flowchart = flowchart
        self.canvas = None
        self.selected_item = None
        self.selected_arrow_id = None
        self.selected_arrow_item = None
        self.arrow_start = None
        self.state_manager = None

    def set_canvas(self, canvas):
        self.canvas = canvas
        self.render()

    # ---------------------------------------------------------
    # CREATE SHAPE
    # ---------------------------------------------------------
    def create_shape(self, shape_type, x, y):
        print(f"Creating shape: {shape_type} at ({x}, {y})")
        shape = Shape(shape_type, x, y)
        self.flowchart.add_node(shape)
        self._save_state()
        self.render()
        return shape

    # ---------------------------------------------------------
    # RENDER ALL
    # ---------------------------------------------------------
    def render(self):
        if not self.canvas:
            return

        self.canvas.delete("all")

        # Draw shapes
        for node in self.flowchart.nodes:
            self._draw_shape(node)

        # Draw arrows
        for edge in self.flowchart.edges:
            self._draw_arrow(edge)

    # ---------------------------------------------------------
    # DRAW SHAPE
    # ---------------------------------------------------------
    def _draw_shape(self, shape):
        if not self.canvas:
            return

        x, y = shape.position
        width, height = 120, 60
        shape_type = shape.type
        color = self._get_shape_color(shape_type)

        # START
        if shape_type == ShapeType.START:
            item = self.canvas.create_oval(
                x, y, x + width, y + height,
                fill=color, outline="black", width=2,
                tags=("draggable", "shape", f"shape_{shape.id}")
            )

        # PROCESS
        elif shape_type == ShapeType.PROCESS:
            item = self.canvas.create_rectangle(
                x, y, x + width, y + height,
                fill=color, outline="black", width=2,
                tags=("draggable", "shape", f"shape_{shape.id}")
            )

        # DECISION
        elif shape_type == ShapeType.DECISION:
            points = [
                x + width // 2, y,
                x + width, y + height // 2,
                x + width // 2, y + height,
                x, y + height // 2
            ]
            item = self.canvas.create_polygon(
                *points,
                fill=color, outline="black", width=2,
                tags=("draggable", "shape", f"shape_{shape.id}")
            )

        # INPUT/OUTPUT
        elif shape_type == ShapeType.INPUT_OUTPUT:
            points = [
                x + 20, y,
                x + width - 20, y,
                x + width, y + height,
                x, y + height
            ]
            item = self.canvas.create_polygon(
                *points,
                fill=color, outline="black", width=2,
                tags=("draggable", "shape", f"shape_{shape.id}")
            )

        # FOR LOOP
        elif shape_type == ShapeType.FOR_LOOP:
            item = self.canvas.create_rectangle(
                x, y, x + width, y + height,
                fill="#4A90E2", outline="black", width=2,
                tags=("draggable", "shape", f"shape_{shape.id}")
            )

        # WHILE LOOP
        elif shape_type == ShapeType.WHILE_LOOP:
            item = self.canvas.create_rectangle(
                x, y, x + width, y + height,
                fill="#F5A623", outline="black", width=2,
                tags=("draggable", "shape", f"shape_{shape.id}")
            )

        # DEFAULT
        else:
            item = self.canvas.create_rectangle(
                x, y, x + width, y + height,
                fill="#D3D3D3", outline="black", width=2,
                tags=("draggable", "shape", f"shape_{shape.id}")
            )

        # TEXT
        text_item = self.canvas.create_text(
            x + width // 2, y + height // 2,
            text=shape.text or shape_type.name,
            font=("Arial", 10, "bold"),
            fill="black",
            tags=("draggable", "text", f"text_{shape.id}")
        )

        shape.items = [item, text_item]

    # ---------------------------------------------------------
    # DRAW ARROW
    # ---------------------------------------------------------
    def _draw_arrow(self, edge):
        if not self.canvas:
            return

        from_shape = self.flowchart.get_node(edge.from_id)
        to_shape = self.flowchart.get_node(edge.to_id)

        if not from_shape or not to_shape:
            return

        from_x = from_shape.position[0] + 60
        from_y = from_shape.position[1] + 30
        to_x = to_shape.position[0] + 60
        to_y = to_shape.position[1] + 30

        self.canvas.create_line(
            from_x, from_y, to_x, to_y,
            arrow=tk.LAST,
            width=2,
            fill="white",
            arrowshape=(10, 12, 5),
            tags=("arrow", f"arrow_{edge.id}")
        )

    # ---------------------------------------------------------
    # COLORS
    # ---------------------------------------------------------
    def _get_shape_color(self, shape_type):
        colors = {
            ShapeType.START: "#90EE90",
            ShapeType.PROCESS: "#87CEEB",
            ShapeType.DECISION: "#FFD700",
            ShapeType.INPUT_OUTPUT: "#FFB6C1",
            ShapeType.FOR_LOOP: "#4A90E2",
            ShapeType.WHILE_LOOP: "#F5A623",
        }
        return colors.get(shape_type, "#D3D3D3")

    # ---------------------------------------------------------
    # SELECT / DESELECT
    # ---------------------------------------------------------
    def select_item(self, x, y):
        items = self.canvas.find_overlapping(x - 2, y - 2, x + 2, y + 2)

        # اول شکل‌ها رو بررسی کن (اولویت با شکل‌هاست)
        for item in items:
            tags = self.canvas.gettags(item)
            if "shape" in tags:
                self.selected_item = item
                self.canvas.itemconfig(item, outline="red", width=3)
                return True

        # اگر شکلی زیر کلیک نبود، فلش‌ها رو بررسی کن
        for item in items:
            tags = self.canvas.gettags(item)
            if "arrow" in tags:
                for tag in tags:
                    if tag.startswith("arrow_"):
                        self.selected_arrow_id = tag.replace("arrow_", "")
                        self.selected_arrow_item = item
                        self.canvas.itemconfig(item, fill="red", width=3)
                        return True

        return False

    def deselect_all(self):
        if self.selected_item:
            try:
                self.canvas.itemconfig(self.selected_item, outline="black", width=2)
            except:
                pass
            self.selected_item = None

        if self.selected_arrow_item:
            try:
                self.canvas.itemconfig(self.selected_arrow_item, fill="white", width=2)
            except:
                pass
            self.selected_arrow_item = None
            self.selected_arrow_id = None

    # ---------------------------------------------------------
    # MOVE SHAPE
    # ---------------------------------------------------------
    def move_shape(self, shape_id, dx, dy):
        shape = self.flowchart.get_node(shape_id)
        if not shape:
            return

        old_x, old_y = shape.position
        new_x = old_x + dx
        new_y = old_y + dy
        shape.position = (new_x, new_y)

        for item in shape.items:
            try:
                self.canvas.move(item, dx, dy)
            except:
                pass

        self.update_arrows_for_shape(shape)

    def update_arrows_for_shape(self, shape):
        for edge in self.flowchart.edges:
            if edge.from_id == shape.id or edge.to_id == shape.id:
                old_items = self.canvas.find_withtag(f"arrow_{edge.id}")
                for item in old_items:
                    self.canvas.delete(item)
                self._draw_arrow(edge)

    # ---------------------------------------------------------
    # ARROWS
    # ---------------------------------------------------------
    def add_arrow(self, from_id, to_id):
        print(f"Adding arrow from {from_id} to {to_id}")

        if from_id and to_id and from_id != to_id:
            for edge in self.flowchart.edges:
                if edge.from_id == from_id and edge.to_id == to_id:
                    print("Arrow already exists!")
                    return None

            edge = Arrow(from_id, to_id)
            self.flowchart.add_edge(edge)
            self._save_state()
            self.render()
            print("Arrow added successfully")
            return edge

        print("Invalid arrow")
        return None

    # ---------------------------------------------------------
    # DELETE
    # ---------------------------------------------------------
    def delete_selected(self):
        if self.selected_item:
            tags = self.canvas.gettags(self.selected_item)
            for tag in tags:
                if tag.startswith("shape_"):
                    shape_id = tag.replace("shape_", "")
                    self.flowchart.remove_node(shape_id)

                    edges_to_remove = [
                        edge for edge in self.flowchart.edges
                        if edge.from_id == shape_id or edge.to_id == shape_id
                    ]

                    for edge in edges_to_remove:
                        self.flowchart.remove_edge(edge)

                    self._save_state()
                    self.render()
                    self.selected_item = None
                    return True

        if self.selected_arrow_id:
            edge = next(
                (e for e in self.flowchart.edges if e.id == self.selected_arrow_id),
                None
            )
            if edge:
                self.flowchart.remove_edge(edge)
                self._save_state()
                self.render()
                self.selected_arrow_id = None
                self.selected_arrow_item = None
                return True

        return False

    # ---------------------------------------------------------
    # SAVE STATE
    # ---------------------------------------------------------
    def _save_state(self):
        try:
            if self.state_manager:
                self.state_manager.save_state()
                return True
        except Exception as e:
            print(f"Error saving state: {e}")
        return False

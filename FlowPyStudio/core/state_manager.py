from models.shapes import Shape, ShapeType
from models.arrows import Arrow
import copy

class StateManager:
    def __init__(self, flowchart):
        self.flowchart = flowchart
        self.undo_stack = []
        self.redo_stack = []
        self.max_states = 50
        # ذخیره حالت اولیه
        self.save_state()
        
    def save_state(self):
        """ذخیره وضعیت فعلی برای Undo"""
        print("=== StateManager.save_state called ===")
        try:
            state = self._serialize_flowchart()
            self.undo_stack.append(state)
            if len(self.undo_stack) > self.max_states:
                self.undo_stack.pop(0)
            self.redo_stack.clear()
            print(f"State saved! Stack size: {len(self.undo_stack)}")
            print(f"Nodes in state: {len(state['nodes'])}")
            return True
        except Exception as e:
            print(f"Error saving state: {e}")
            import traceback
            traceback.print_exc()
            return False
        
    def undo(self):
        """بازگشت به حالت قبلی"""
        print("=== StateManager.undo called ===")
        print(f"Undo stack size: {len(self.undo_stack)}")
        
        if len(self.undo_stack) <= 1:
            print("Nothing to undo")
            return False
            
        try:
            # ذخیره حالت فعلی برای Redo
            current_state = self._serialize_flowchart()
            self.redo_stack.append(current_state)
            
            # حذف حالت فعلی و رفتن به حالت قبلی
            self.undo_stack.pop()
            state = self.undo_stack[-1]
            self._deserialize_flowchart(state)
            print(f"Undo successful! Redo stack: {len(self.redo_stack)}")
            return True
        except Exception as e:
            print(f"Error undoing: {e}")
            import traceback
            traceback.print_exc()
            return False
        
    def redo(self):
        """رفتن به حالت بعدی"""
        print("=== StateManager.redo called ===")
        print(f"Redo stack size: {len(self.redo_stack)}")
        
        if not self.redo_stack:
            print("Nothing to redo")
            return False
            
        try:
            # ذخیره حالت فعلی برای Undo
            current_state = self._serialize_flowchart()
            self.undo_stack.append(current_state)
            
            # بازیابی حالت بعدی
            state = self.redo_stack.pop()
            self._deserialize_flowchart(state)
            print(f"Redo successful! Redo stack: {len(self.redo_stack)}")
            return True
        except Exception as e:
            print(f"Error redoing: {e}")
            import traceback
            traceback.print_exc()
            return False
        
    def clear(self):
        """پاک کردن همه حالت‌ها"""
        self.undo_stack.clear()
        self.redo_stack.clear()
        self.save_state()
        
    def _serialize_flowchart(self):
        """تبدیل فلوچارت به دیکشنری"""
        data = {
            "nodes": [],
            "edges": []
        }
        
        for node in self.flowchart.nodes:
            # بررسی نوع node.type
            if hasattr(node.type, 'value'):
                type_str = node.type.value
            else:
                type_str = str(node.type)
                
            data["nodes"].append({
                "id": node.id,
                "type": type_str,
                "text": node.text,
                "x": node.position[0],
                "y": node.position[1]
            })
            
        for edge in self.flowchart.edges:
            data["edges"].append({
                "from": edge.from_id,
                "to": edge.to_id
            })
            
        return data
        
    def _deserialize_flowchart(self, data):
        """بازیابی فلوچارت از دیکشنری"""
        # پاک کردن فلوچارت فعلی
        self.flowchart.clear()
        
        # بازیابی گره‌ها
        for node_data in data["nodes"]:
            type_str = node_data["type"]
            try:
                shape_type = ShapeType(type_str)
            except ValueError:
                shape_type = ShapeType.PROCESS
                
            shape = Shape(shape_type, node_data["x"], node_data["y"])
            shape.id = node_data["id"]
            shape.text = node_data["text"]
            self.flowchart.add_node(shape)
            
        # بازیابی یال‌ها
        for edge_data in data["edges"]:
            edge = Arrow(edge_data["from"], edge_data["to"])
            self.flowchart.add_edge(edge)
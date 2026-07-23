import uuid
from enum import Enum

class ShapeType(Enum):
    START = "start"
    PROCESS = "process"
    DECISION = "decision"
    INPUT_OUTPUT = "io"
    TEXT = "text"
    SELECT = "select"
    ARROW = "arrow"
    FOR_LOOP = "for_loop"
    WHILE_LOOP = "while_loop"

class Shape:
    def __init__(self, shape_type, x, y):
        self.id = str(uuid.uuid4())[:8]
        self.type = shape_type
        self.position = (x, y)
        self.text = self._get_default_text()
        self.width = 120
        self.height = 60
        
    def _get_default_text(self):
        defaults = {
            ShapeType.START: "Start",
            ShapeType.PROCESS: "Process",
            ShapeType.DECISION: "Condition",
            ShapeType.INPUT_OUTPUT: "Input/Output",
            ShapeType.TEXT: "Text"
        }
        return defaults.get(self.type, "Shape")
        
    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type.value,
            "text": self.text,
            "x": self.position[0],
            "y": self.position[1]
        }
        
    @classmethod
    def from_dict(cls, data):
        shape = cls(ShapeType(data["type"]), data["x"], data["y"])
        shape.id = data["id"]
        shape.text = data["text"]
        return shape

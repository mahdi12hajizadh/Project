import uuid

class Arrow:
    def __init__(self, from_id, to_id, direction=None):
        self.id = str(uuid.uuid4())[:8]
        self.from_id = from_id
        self.to_id = to_id
        self.direction = direction or "down"
        self.style = "solid"
        
    def to_dict(self):
        return {
            "id": self.id,
            "from": self.from_id,
            "to": self.to_id,
            "direction": self.direction
        }
        
    @classmethod
    def from_dict(cls, data):
        arrow = cls(data["from"], data["to"], data.get("direction", "down"))
        arrow.id = data["id"]
        return arrow

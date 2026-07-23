import json
from models.shapes import Shape, ShapeType
from models.arrows import Arrow
from models.flowchart import Flowchart

class Serializer:
    @staticmethod
    def serialize_shape(shape):
        return {
            "id": shape.id,
            "type": shape.type.value,
            "text": shape.text,
            "x": shape.position[0],
            "y": shape.position[1]
        }
        
    @staticmethod
    def deserialize_shape(data):
        shape = Shape(ShapeType(data["type"]), data["x"], data["y"])
        shape.id = data["id"]
        shape.text = data["text"]
        return shape
        
    @staticmethod
    def serialize_arrow(arrow):
        return {
            "id": arrow.id,
            "from": arrow.from_id,
            "to": arrow.to_id,
            "direction": arrow.direction
        }
        
    @staticmethod
    def deserialize_arrow(data):
        arrow = Arrow(data["from"], data["to"], data.get("direction", "down"))
        arrow.id = data["id"]
        return arrow
        
    @staticmethod
    def serialize_flowchart(flowchart):
        return {
            "name": flowchart.name,
            "nodes": [Serializer.serialize_shape(n) for n in flowchart.nodes],
            "edges": [Serializer.serialize_arrow(e) for e in flowchart.edges]
        }
        
    @staticmethod
    def deserialize_flowchart(data):
        flowchart = Flowchart()
        flowchart.name = data.get("name", "Untitled")
        
        for node_data in data.get("nodes", []):
            flowchart.add_node(Serializer.deserialize_shape(node_data))
            
        for edge_data in data.get("edges", []):
            flowchart.add_edge(Serializer.deserialize_arrow(edge_data))
            
        return flowchart

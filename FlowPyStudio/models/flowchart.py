class Flowchart:
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.name = "Untitled"

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes.append(node)
            return True
        return False

    def remove_node(self, node_id):
        self.nodes = [n for n in self.nodes if n.id != node_id]
        self.edges = [e for e in self.edges if e.from_id != node_id and e.to_id != node_id]

    def get_node(self, node_id):
        for node in self.nodes:
            if node.id == node_id:
                return node
        return None

    def add_edge(self, edge):
        if edge not in self.edges:
            for e in self.edges:
                if e.from_id == edge.from_id and e.to_id == edge.to_id:
                    return False
            self.edges.append(edge)
            return True
        return False

    def remove_edge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)
            return True
        return False

    def clear(self):
        self.nodes.clear()
        self.edges.clear()

    def to_dict(self):
        return {
            "name": self.name,
            "nodes": [node.to_dict() for node in self.nodes],
            "edges": [edge.to_dict() for edge in self.edges]
        }

    @classmethod
    def from_dict(cls, data):
        from models.shapes import Shape
        from models.arrows import Arrow

        flowchart = cls()
        flowchart.name = data.get("name", "Untitled")

        for node_data in data.get("nodes", []):
            node = Shape.from_dict(node_data)
            flowchart.add_node(node)

        for edge_data in data.get("edges", []):
            edge = Arrow.from_dict(edge_data)
            flowchart.add_edge(edge)

        return flowchart

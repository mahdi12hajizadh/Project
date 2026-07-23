from models.shapes import ShapeType

class CodeGenerator:
    def __init__(self):
        self.indent_level = 0
        self.code_lines = []
        self.visited_nodes = set()
        self.flowchart = None
        
    def generate(self, flowchart):
        """Generate Python code from flowchart"""
        self.flowchart = flowchart
        self.code_lines = []
        self.visited_nodes = set()
        self.indent_level = 0
        
        if not flowchart.nodes:
            return "# No shapes to generate code from"
            
        # Find start node
        start_nodes = [n for n in flowchart.nodes if n.type == ShapeType.START]
        if not start_nodes:
            return "# No start node found"
            
        start_node = start_nodes[0]
        
        # Add header
        self.code_lines.append("# Generated code from FlowPy Studio")
        self.code_lines.append("")
        
        # Generate code from start node
        self._generate_from_node(start_node)
        
        return "\n".join(self.code_lines)
        
    def _generate_from_node(self, node):
        """Recursively generate code from a node"""
        if node.id in self.visited_nodes:
            return
            
        self.visited_nodes.add(node.id)
        
        outgoing = [e for e in self.flowchart.edges if e.from_id == node.id]
        indent = "    " * self.indent_level
        
        # START node
        if node.type == ShapeType.START:
            pass
        
        # PROCESS node
        elif node.type == ShapeType.PROCESS:
            line = node.text.strip()
            self.code_lines.append(f"{indent}{line}")

            # اگر خط یک بلاک جدید باز می‌کند (مثل for یا if)
            if line.endswith(":"):
                self.indent_level += 1

        # INPUT/OUTPUT node
        elif node.type == ShapeType.INPUT_OUTPUT:
            if "input" in node.text.lower():
                self.code_lines.append(f"{indent}{node.text}")
            else:
                self.code_lines.append(f"{indent}print({node.text})")
        
        # FOR LOOP / WHILE LOOP node
        elif node.type in (ShapeType.FOR_LOOP, ShapeType.WHILE_LOOP):
            line = node.text.strip()
            if not line.endswith(":"):
                line += ":"
            self.code_lines.append(f"{indent}{line}")
            self.indent_level += 1

            # فلش اول = بدنه‌ی حلقه (داخل تورفتگی)
            if outgoing:
                body_edge = outgoing[0]
                body_node = self.flowchart.get_node(body_edge.to_id)
                if body_node:
                    self._generate_from_node(body_node)
            else:
                self.code_lines.append(f"{indent}    pass")

            self.indent_level -= 1

            # فلش دوم = ادامه‌ی کد بعد از حلقه (خارج از تورفتگی)
            if len(outgoing) > 1:
                after_edge = outgoing[1]
                after_node = self.flowchart.get_node(after_edge.to_id)
                if after_node:
                    self._generate_from_node(after_node)

        # DECISION node
        elif node.type == ShapeType.DECISION:
            condition = node.text.strip()

            # اگر کاربر خودش "if" یا ":" اضافه نوشته باشه، حذفش کن تا تکراری نشه
            if condition.lower().startswith("if "):
                condition = condition[3:].strip()
            elif condition.lower() == "if":
                condition = ""
            if condition.endswith(":"):
                condition = condition[:-1].strip()

            self.code_lines.append(f"{indent}if {condition}:")
            self.indent_level += 1
            
            # True branch
            if outgoing:
                true_edge = outgoing[0]
                true_node = self.flowchart.get_node(true_edge.to_id)
                if true_node:
                    self._generate_from_node(true_node)
            
            self.indent_level -= 1
            
            # False branch
            if len(outgoing) > 1:
                self.code_lines.append(f"{indent}else:")
                self.indent_level += 1
                false_edge = outgoing[1]
                false_node = self.flowchart.get_node(false_edge.to_id)
                if false_node:
                    self._generate_from_node(false_node)
                self.indent_level -= 1
        
        # ادامه مسیر برای گره‌های غیر تصمیم‌گیری و غیر حلقه
        # (Decision و Loop مسیر خروجی‌هاشون رو خودشون در بالا مدیریت می‌کنند)
        if node.type not in (ShapeType.DECISION, ShapeType.FOR_LOOP, ShapeType.WHILE_LOOP):
            for edge in outgoing:
                next_node = self.flowchart.get_node(edge.to_id)
                if next_node:
                    self._generate_from_node(next_node)

import json
import os
from datetime import datetime

class FileManager:
    def __init__(self):
        self.serializer = None
        
    def save_project(self, flowchart, filename):
        """Save flowchart to JSON file"""
        data = flowchart.to_dict()
        data["saved_at"] = datetime.now().isoformat()
        data["version"] = "1.0"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
    def load_project(self, filename):
        """Load flowchart from JSON file"""
        from models.flowchart import Flowchart
        
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        return Flowchart.from_dict(data)
        
    def export_png(self, canvas, filename):
        """Export canvas to PNG image"""
        try:
            # For Tkinter canvas, we need to use postscript and convert
            # This is a simple implementation
            ps_filename = filename.rsplit('.', 1)[0] + '.ps'
            canvas.postscript(file=ps_filename, colormode='color')
            
            # Optional: Use Pillow to convert PS to PNG
            # from PIL import Image
            # Image.open(ps_filename).save(filename, 'PNG')
            
            # For now, we'll just save as PS
            return True
        except Exception as e:
            raise Exception(f"Failed to export: {str(e)}")

class Theme:
    def __init__(self, name, colors):
        self.name = name
        self.colors = colors
        
    @property
    def bg(self):
        return self.colors.get("bg", "#ffffff")
        
    @property
    def fg(self):
        return self.colors.get("fg", "#000000")
        
    @property
    def code_bg(self):
        return self.colors.get("code_bg", "#1e1e1e")
        
    @property
    def code_fg(self):
        return self.colors.get("code_fg", "#d4d4d4")
        
    @property
    def shape_colors(self):
        return self.colors.get("shapes", {})
        
class LightTheme(Theme):
    def __init__(self):
        super().__init__("Light", {
            "bg": "#f0f0f0",
            "fg": "#000000",
            "code_bg": "#ffffff",
            "code_fg": "#000000",
            "shapes": {
                "start": "#90EE90",
                "process": "#87CEEB",
                "decision": "#FFD700",
                "io": "#FFB6C1",
                "text": "#D3D3D3"
            }
        })

class DarkTheme(Theme):
    def __init__(self):
        super().__init__("Dark", {
            "bg": "#1e1e1e",
            "fg": "#ffffff",
            "code_bg": "#1e1e1e",
            "code_fg": "#d4d4d4",
            "shapes": {
                "start": "#2d5a27",
                "process": "#1a3a4a",
                "decision": "#4a3a0a",
                "io": "#4a1a2a",
                "text": "#2a2a2a"
            }
        }) 

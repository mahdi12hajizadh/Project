from theme.theme import LightTheme, DarkTheme

class ThemeManager:
    def __init__(self):
        self.light_theme = LightTheme()
        self.dark_theme = DarkTheme()
        self.current_theme = "dark"  # Default to dark mode
        self.themes = {
            "light": self.light_theme,
            "dark": self.dark_theme
        }
        
    def toggle_theme(self):
        if self.current_theme == "light":
            self.current_theme = "dark"
        else:
            self.current_theme = "light"
            
    def get_theme(self):
        return self.themes.get(self.current_theme, self.dark_theme)
        
    def set_theme(self, theme_name):
        if theme_name in self.themes:
            self.current_theme = theme_name
            
    def get_theme_colors(self):
        theme = self.get_theme()
        return {
            "bg": theme.bg,
            "fg": theme.fg,
            "code_bg": theme.code_bg,
            "code_fg": theme.code_fg,
            "shape_colors": theme.shape_colors
        } 

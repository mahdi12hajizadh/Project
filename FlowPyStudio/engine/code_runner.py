import sys
import io
import subprocess
import tempfile
import os

class CodeRunner:
    def __init__(self):
        self.output = None
        self.error = None
        
    def run(self, code):
        """Execute Python code and capture output"""
        if not code or not code.strip():
            return "No code to execute"
            
        # Method 1: Using exec (simpler, but limited)
        try:
            # Capture stdout
            old_stdout = sys.stdout
            sys.stdout = io.StringIO()
            
            # Execute code
            exec_globals = {}
            exec(code, exec_globals)
            
            # Get output
            output = sys.stdout.getvalue()
            
            # Restore stdout
            sys.stdout = old_stdout
            
            return output if output else "Code executed successfully (no output)"
            
        except Exception as e:
            # Restore stdout on error
            sys.stdout = old_stdout
            return f"Error: {str(e)}"
            
    def run_with_subprocess(self, code):
        """Execute code in subprocess (more secure)"""
        if not code or not code.strip():
            return "No code to execute"
            
        try:
            # Write code to temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
                
            # Run the script
            result = subprocess.run(
                [sys.executable, temp_file],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Clean up
            os.unlink(temp_file)
            
            output = result.stdout
            if result.stderr:
                output += "\n" + result.stderr
                
            return output if output else "Code executed successfully (no output)"
            
        except subprocess.TimeoutExpired:
            return "Error: Code execution timed out (30 seconds)"
        except Exception as e:
            return f"Error: {str(e)}"

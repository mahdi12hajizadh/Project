# FlowPy Studio

FlowPy Studio is a desktop app (built with Python + Tkinter/ttkbootstrap) for visually
designing flowcharts and automatically generating runnable Python code from them.

## Features

- Drag-and-drop flowchart editor on an interactive canvas
- Shapes: Start/End, Process, Decision, For Loop, While Loop, Input/Output
- Automatic Python code generation from the flowchart
- Run the generated code directly inside the app and see the output
- Export the flowchart as a PNG image
- Export the generated code as a PDF
- Undo / Redo
- Light and dark theme

## Requirements

- Python 3.10+
- See [requirements.txt](requirements.txt)

## Installation

```bash
git clone https://github.com/<your-username>/FlowPyStudio.git
cd FlowPyStudio
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

1. Pick a shape from the toolbar and click on the canvas to place it.
2. Connect shapes with the **Arrow** tool (for a For/While Loop, draw two
   arrows out of the loop shape: the first one is the loop body, the second
   one is what runs after the loop finishes).
3. Double-click a shape to edit its text.
4. Click **Generate Code** to turn the flowchart into Python code, then
   **Run Code** to execute it.

## Project structure

```
FlowPyStudio/
├── main.py            # entry point
├── ui.py               # main application window / layout
├── core/                # canvas rendering, event handling, undo/redo, export
├── engine/              # flowchart → Python code generation & execution
├── models/               # Shape / Arrow / Flowchart data models
├── storage/              # save/load project files
├── theme/                # theming
└── assets/
```

## License

MIT

import os

import dash
from dash import html, dcc, Input, Output, State, callback
import dash_uploader as du


# ============================================================
# Register page
# ============================================================

dash.register_page(__name__, path="/")


# ============================================================
# Directories
# ============================================================

UPLOAD_DIR = r"G:\My Drive\PPMAndSubs\Investors"
PPM_DIR = os.path.abspath(r"G:\My Drive\PPMAndSubs\PPMs")


# ============================================================
# Helper functions
# ============================================================

def get_file_icon(filename):
    return "📄"


def list_ppm_files():
    try:
        files = os.listdir(PPM_DIR)
        return [f for f in files if f.endswith(".pdf")]
    except FileNotFoundError:
        return []


# ============================================================
# Layout
# ============================================================

layout = html.Div([

    # --------------------------------------------------------
    # Title
    # --------------------------------------------------------

    html.H1(
        "Alpha Exchange",
        style={
            "fontSize": "40px",
            "fontFamily": "Times New Roman, serif",
            "textAlign": "center",
            "marginBottom": "10px",
        }
    ),

    html.Hr(
        style={
            "border": "none",
            "height": "2px",
            "backgroundColor": "rgb(215, 112, 27)",
            "width": "5cm",
            "margin": "0 auto 20px auto",
        }
    ),

    # --------------------------------------------------------
    # New user button
    # --------------------------------------------------------

    dcc.Link(
        html.Button("New user"),
        href="/new-user"
    ),

    # --------------------------------------------------------
    # Upload section
    # --------------------------------------------------------

    html.H1(
        "Drag and Drop File Upload",
        style={
            "fontSize": "30px",
            "fontFamily": "Times New Roman, serif",
        }
    ),

    du.Upload(
        id="upload-file",
        text="Drag and drop a file here or click to select",
        max_file_size=10,
        filetypes=["pdf"],
        default_style={
            "border": "2px dashed #ccc",
            "padding": "20px",
            "text-align": "center",
            "margin": "20px",
        },
    ),

    html.Div(id="upload-status"),

    # --------------------------------------------------------
    # PPM section
    # --------------------------------------------------------

    html.H2(
        "Display PPMs",
        style={
            "fontSize": "30px",
            "fontFamily": "Times New Roman, serif",
        }
    ),

    html.Div(
        id="ppm-files",
        children=[
            html.A(
                [
                    html.Span(
                        get_file_icon(file),
                        style={"margin-right": "10px"}
                    ),
                    html.Span(file),
                ],
                href=f"/ppms/{file}",
                target="_blank",
                style={
                    "margin": "10px",
                    "padding": "5px",
                    "border": "1px solid #ddd",
                    "display": "block"
                }
            )
            for file in list_ppm_files()
        ]
    ),
])


# ============================================================
# Callback: upload status
# ============================================================

@callback(
    Output("upload-status", "children"),
    Input("upload-file", "isCompleted"),
    State("upload-file", "fileNames"),
    State("upload-file", "upload_id"),
)
def update_status(is_completed, file_names, upload_id):

    if is_completed:
        return html.Div([
            html.P(
                f"File(s) uploaded: {', '.join(file_names)}"
            ),
            html.P(
                f"Saved to: {os.path.abspath(UPLOAD_DIR)}"
            ),
        ])

    return html.P("Upload a file to see the status.")
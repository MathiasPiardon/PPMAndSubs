import os

import dash
from dash import html, dcc, callback, Input, Output, State
import dash_uploader as du


# ============================================================
# Register page
# ============================================================

dash.register_page(__name__, path="/new-user")


# ============================================================
# Directories
# ============================================================

UPLOAD_DIR = r"G:\My Drive\PPMAndSubs\Investors"


# ============================================================
# Layout
# ============================================================

layout = html.Div(
    [

        dcc.Link(
                "⌂",
                href="/",
                style={
                    "position": "absolute",
                    "top": "15px",
                    "fontSize": "28px",
                    "textDecoration": "none",
                    "color": "#333",
                    "zIndex": 1000,
                }
            ),

        html.H1(
            "New User",
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

        dcc.Input(
            id="first-name",
            placeholder="First name",
            style={"width": "400px"}
        ),

        dcc.Input(
            id="last-name",
            placeholder="Last name",
            style={"width": "400px"}
        ),

        dcc.Input(
            id="date-of-birth",
            placeholder="Date of Birth",
            style={"width": "400px"}
        ),

        dcc.Input(
            id="nationality",
            placeholder="Nationality",
            style={"width": "400px"}
        ),

        dcc.Input(
            id="sex",
            placeholder="Sex",
            style={"width": "400px"}
        ),

        dcc.Input(
            id="proof-of-id_number",
            placeholder="Proof of ID Number",
            style={"width": "400px"}
        ),

        dcc.Input(
            id="email",
            placeholder="Email",
            style={"width": "400px"}
        ),

        html.Button(
            "Save",
            id="save-user",
            style={"width": "200px"}
        ),

        html.Hr(
            style={
                "border": "none",
                "height": "2px",
                "backgroundColor": "rgb(215, 112, 27)",
                "width": "20cm",
                "margin": "0 auto 20px auto",
            }
        ),

        # ----------------------------------------------------
        # Drag & Drop File Upload
        # ----------------------------------------------------

        html.H1(
            "Upload Proof of ID",
            style={
                "fontSize": "30px",
                "fontFamily": "Times New Roman, serif",
            }
        ),

        du.Upload(
            id="upload-file",
            text="Drop here your proof of ID",
            max_file_size=10,
            filetypes=["pdf"],
            default_style={
                "border": "2px dashed #ccc",
                "padding": "20px",
                "textAlign": "center",
                "margin": "20px",
                "width": "400px",
                "backgroundColor": "white",
            },
        ),

        html.Div(id="upload-status"),
    ],

    style={
        "display": "flex",
        "flexDirection": "column",
        "alignItems": "left",
        "marginLeft": "30px",
        "gap": "10px",
    },
)


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
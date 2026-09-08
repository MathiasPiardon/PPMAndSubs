import os
import dash
from dash import html, dcc
import dash_uploader as du


# ============================================================
# Register page
# ============================================================

dash.register_page(__name__, path="/select-managers")


# ============================================================
# Directories
# ============================================================


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
            "Select Managers",
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
                                    style={"marginRight": "10px"}
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
    ],

    style={
            "display": "flex",
            "flexDirection": "column",
            "alignItems": "left",
            "marginLeft": "30px",
            "gap": "10px",
        },
    
)
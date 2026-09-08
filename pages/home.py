import os

import dash
from dash import html, dcc


# ============================================================
# Register page
# ============================================================

dash.register_page(__name__, path="/")



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
    # Text
    # --------------------------------------------------------

    html.H2(
            [
            "Subscribe or redeem in one click to hedge funds.",
            html.Br(),
            html.Br(),
            "Get a summary of the risks in the PPM.",
            html.Br(),
            html.Br(),
            "Monitor your investments and get alerts when new PPMs are available.",
            html.Br(),
            html.Br(),
            "Chat directly with managers",
            html.Br(),
            html.Br(),
            "Get reminders for your subscription and redemption deadlines.",
            html.Br(),
            html.Br(),
            ],
            style={
                "fontSize": "20px",
                "fontFamily": "Times New Roman, serif",
                "textAlign": "left",
                "marginLeft": "100px",
                "marginBottom": "10px",
            }
        ),


    # --------------------------------------------------------
    # Buttons
    # --------------------------------------------------------

    html.Div(
            [
                dcc.Link(
                    html.Button(
                        "New user",
                        style={
                            "width": "200px",
                            "fontSize": "20px",
                            "backgroundColor": "White",
                            "borderColor": "hsl(24, 66%, 49%)",
                        }
                    ),
                    href="/new-user"
                ),

                dcc.Link(
                    html.Button(
                        "Select Managers",
                        style={
                            "width": "200px",
                            "fontSize": "20px",
                            "backgroundColor": "White",
                            "borderColor": "hsl(140, 80%, 90%)",
                        }
                    ),
                    href="/select-managers"
                ),
            ],
            style={
                "display": "flex",
                "gap": "20px",
                "justifyContent": "center",
            }
        ),

    ],
"""
 style={
            "display": "flex",
            "flexDirection": "column",
            "alignItems": "left",
            "marginLeft": "30px",
            "gap": "10px",
        },
"""


)
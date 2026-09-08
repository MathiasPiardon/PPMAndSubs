import dash
from dash import html, dcc

dash.register_page(__name__, path="/new-user")

layout = html.Div(
    [
    html.H1("New User"),

    dcc.Input(id="first-name", placeholder="First name", style={"width": "400px"}),
    dcc.Input(id="last-name", placeholder="Last name", style={"width": "400px"}),
    dcc.Input(id="date-of-birth", placeholder="Date of Birth", style={"width": "400px"}),
    dcc.Input(id="nationality", placeholder="Nationality", style={"width": "400px"}),
    dcc.Input(id="sex", placeholder="Sex", style={"width": "400px"}),    
    dcc.Input(id="proof-of-id", placeholder="Proof of ID", style={"width": "400px"}),
    dcc.Input(id="email", placeholder="Email", style={"width": "400px"}),

    html.Button("Save", id="save-user", style={"width": "200px"}),
    ],
    style={"display": "flex", "flexDirection": "column", "alignItems": "left","marginLeft": "30px", "gap": "10px"},
)
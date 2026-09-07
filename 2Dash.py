import os
from dash import Dash, html, Input, Output, State, callback
import dash_uploader as du
import dash_bootstrap_components as dbc
from flask import send_from_directory

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

# Define the upload and PPM directories
UPLOAD_DIR = r"G:\My Drive\PPMAndSubs\Investors"
PPM_DIR = os.path.abspath(r"G:\My Drive\PPMAndSubs\PPMs")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PPM_DIR, exist_ok=True)

# Configure the uploader
du.configure_upload(app, UPLOAD_DIR)

# Serve PDFs under `/ppms/` instead of `/static/`
@app.server.route('/ppms/<path:filename>')
def serve_ppm(filename):
    return send_from_directory(PPM_DIR, filename)

# Function to get file icons
def get_file_icon(filename):
    return "📄"

# Function to list files in the PPM directory
def list_ppm_files():
    try:
        files = os.listdir(PPM_DIR)
        return [f for f in files if f.endswith('.pdf')]
    except FileNotFoundError:
        return []

# Define the app layout
app.layout = html.Div([
    html.H1("Drag and Drop File Upload"),
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
    html.H2("Display PPMs"),
    html.Div(
        id="ppm-files",
        children=[
            html.A(
                [
                    html.Span(get_file_icon(file), style={"margin-right": "10px"}),
                    html.Span(file),
                ],
                href=f"/ppms/{file}",  # Updated to use `/ppms/`
                target="_blank",
                style={"margin": "10px", "padding": "5px", "border": "1px solid #ddd", "display": "block"}
            )
            for file in list_ppm_files()
        ]
    ),
])

# Callback to handle file upload
@callback(
    Output("upload-status", "children"),
    Input("upload-file", "isCompleted"),
    State("upload-file", "fileNames"),
    State("upload-file", "upload_id"),
)
def update_status(is_completed, file_names, upload_id):
    if is_completed:
        return html.Div([
            html.P(f"File(s) uploaded: {', '.join(file_names)}"),
            html.P(f"Saved to: {os.path.abspath(UPLOAD_DIR)}"),
        ])
    return html.P("Upload a file to see the status.")

if __name__ == "__main__":
    app.run(debug=True)
import os

from dash import Dash, html, page_container
import dash_bootstrap_components as dbc
import dash_uploader as du
from flask import send_from_directory


# ============================================================
# Directories
# ============================================================

UPLOAD_DIR = r"G:\My Drive\PPMAndSubs\Investors"
PPM_DIR = os.path.abspath(r"G:\My Drive\PPMAndSubs\PPMs")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PPM_DIR, exist_ok=True)


# ============================================================
# Initialize Dash app
# ============================================================

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.SLATE],
)


# ============================================================
# Configure uploader
# ============================================================

du.configure_upload(app, UPLOAD_DIR)


# ============================================================
# Serve PDFs under /ppms/
# ============================================================

@app.server.route("/ppms/<path:filename>")
def serve_ppm(filename):
    return send_from_directory(PPM_DIR, filename)


# ============================================================
# Main application layout
# ============================================================

app.layout = html.Div([
    page_container
])


# ============================================================
# Run
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)
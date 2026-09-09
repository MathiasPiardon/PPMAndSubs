import os
import dash
from dash import html, dcc, callback, Input, Output, State
import dash_uploader as du

from utils.ReadDataFromDoc import parse_passport


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

        # ----------------------------------------------------
        # User information
        # ----------------------------------------------------
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
# Callback: upload + organize file + parse passport
# ============================================================
@callback(
    [
        Output("upload-status", "children"),

        # Populate user fields
        Output("first-name", "value"),
        Output("last-name", "value"),
        Output("date-of-birth", "value"),
        Output("nationality", "value"),
        Output("sex", "value"),
        Output("proof-of-id_number", "value"),
    ],

    Input("upload-file", "isCompleted"),

    State("upload-file", "fileNames"),
    State("upload-file", "upload_id"),

    # Prevent Dash from overwriting existing values before upload
    prevent_initial_call=False,
)
def update_status(
    is_completed,
    file_names,
    upload_id,
):
    # --------------------------------------------------------
    # Default values
    # --------------------------------------------------------
    empty_values = (
        None,   # first name
        None,   # last name
        None,   # date of birth
        None,   # nationality
        None,   # sex
        None,   # passport number
    )

    if not is_completed:
        return (
            html.P("Upload a file to see the status."),
            *empty_values,
        )

    if not file_names:
        return (
            html.P("No file was uploaded."),
            *empty_values,
        )

    saved_files = []

    # We will store the passport data here
    passport_data = None

    for filename in file_names:

        # ----------------------------------------------------
        # 1. Get the original filename
        # ----------------------------------------------------
        filename = os.path.basename(filename)

        # ----------------------------------------------------
        # 2. Remove extension to get folder name
        #
        # PassportPiardon.pdf
        #       ↓
        # PassportPiardon
        # ----------------------------------------------------
        document_name, extension = os.path.splitext(filename)

        # ----------------------------------------------------
        # 3. Create/use destination folder
        # ----------------------------------------------------
        destination_folder = os.path.join(
            UPLOAD_DIR,
            document_name
        )

        os.makedirs(
            destination_folder,
            exist_ok=True
        )

        # ----------------------------------------------------
        # 4. Find temporary file
        # ----------------------------------------------------
        if upload_id:
            temporary_folder = os.path.join(
                UPLOAD_DIR,
                upload_id
            )

            source_file = os.path.join(
                temporary_folder,
                filename
            )

        else:
            temporary_folder = None

            source_file = os.path.join(
                UPLOAD_DIR,
                filename
            )

        # ----------------------------------------------------
        # 5. Determine final filename
        # ----------------------------------------------------
        destination_file = os.path.join(
            destination_folder,
            filename
        )

        counter = 2

        while os.path.exists(destination_file):

            new_filename = (
                f"{document_name}_{counter}{extension}"
            )

            destination_file = os.path.join(
                destination_folder,
                new_filename
            )

            counter += 1

        # ----------------------------------------------------
        # 6. Move file to final destination
        # ----------------------------------------------------
        if os.path.exists(source_file):

            os.replace(
                source_file,
                destination_file
            )

        else:

            # Fallback if dash_uploader saved directly
            # in UPLOAD_DIR
            direct_file = os.path.join(
                UPLOAD_DIR,
                filename
            )

            if os.path.exists(direct_file):

                os.replace(
                    direct_file,
                    destination_file
                )

            else:

                saved_files.append(
                    f"Could not find uploaded file: {filename}"
                )

                continue

        # ----------------------------------------------------
        # 7. Parse passport AFTER it has been moved
        # ----------------------------------------------------
        try:

            passport_data = parse_passport(
                destination_file
            )

        except Exception as e:

            saved_files.append(
                f"File saved, but passport could not be read: {e}"
            )

            passport_data = None

        # ----------------------------------------------------
        # 8. Delete temporary upload folder
        # ----------------------------------------------------
        if temporary_folder and os.path.isdir(temporary_folder):

            try:
                os.rmdir(temporary_folder)

            except OSError:
                # Folder not empty
                pass

        saved_files.append(
            destination_file
        )

    # ========================================================
    # 9. Extract values from passport
    # ========================================================

    if passport_data:

        first_name = passport_data.get("first_name")
        last_name = passport_data.get("last_name")
        date_of_birth = passport_data.get("date_of_birth")
        nationality = passport_data.get("nationality")
        sex = passport_data.get("sex")
        passport_number = passport_data.get("passport_number")

        # Convert Python date -> string for Dash input
        if date_of_birth:
            date_of_birth = date_of_birth.strftime("%Y-%m-%d")

        status_message = html.Div(
            [
                html.P("Passport successfully read."),
                html.P("Extracted information:"),
                html.Ul(
                    [
                        html.Li(
                            f"First name: {first_name}"
                        ),
                        html.Li(
                            f"Last name: {last_name}"
                        ),
                        html.Li(
                            f"Date of birth: {date_of_birth}"
                        ),
                        html.Li(
                            f"Nationality: {nationality}"
                        ),
                        html.Li(
                            f"Sex: {sex}"
                        ),
                        html.Li(
                            f"Passport number: {passport_number}"
                        ),
                    ]
                ),
                html.P("Saved to:"),
                html.Ul(
                    [
                        html.Li(path)
                        for path in saved_files
                    ]
                ),
            ]
        )

        return (
            status_message,
            first_name,
            last_name,
            date_of_birth,
            nationality,
            sex,
            passport_number,
        )

    # ========================================================
    # 10. File was saved but parsing failed
    # ========================================================

    return (
        html.Div(
            [
                html.P("File uploaded and saved."),
                html.P("Saved to:"),
                html.Ul(
                    [
                        html.Li(path)
                        for path in saved_files
                    ]
                ),
            ]
        ),
        None,
        None,
        None,
        None,
        None,
        None,
    )
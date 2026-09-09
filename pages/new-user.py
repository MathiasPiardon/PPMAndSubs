import os
import dash
from dash import html, dcc, callback, Input, Output, State
import dash_uploader as du

from utils.ReadDataFromDoc import parse_passport
from utils.SaveInvestorData import SaveInvestorData
from utils.SaveInvestorData import SaveUsernameAndPassword

dash.register_page(__name__, path="/new-user")


UPLOAD_DIR = r"G:\My Drive\PPMAndSubs\Investors"


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

        # ---------------------------------------------------------
        # First name + Username
        # ---------------------------------------------------------
        html.Div(
            [
                dcc.Input(
                    id="first-name",
                    placeholder="First name",
                    style={"width": "400px"}
                ),

                dcc.Input(
                    id="username",
                    placeholder="Username",
                    style={"width": "400px"}
                ),
            ],
            style={
                "display": "flex",
                "gap": "20px",
            }
        ),

        # ---------------------------------------------------------
        # Last name + Password
        # ---------------------------------------------------------
        html.Div(
            [
                dcc.Input(
                    id="last-name",
                    placeholder="Last name",
                    style={"width": "400px"}
                ),

                dcc.Input(
                    id="password",
                    placeholder="Password",
                    type="password",
                    style={"width": "400px"}
                ),
            ],
            style={
                "display": "flex",
                "gap": "20px",
            }
        ),

        # ---------------------------------------------------------
        # Remaining user information
        # ---------------------------------------------------------
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
            n_clicks=0,
            style={"width": "200px"}
        ),

        html.Div(
            id="save-status",
            style={
                "marginTop": "10px",
                "fontSize": "18px",
            }
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


# ================================================================
# SAVE USER
# ================================================================

@callback(
    Output("save-status", "children"),

    Input("save-user", "n_clicks"),

    State("first-name", "value"),
    State("last-name", "value"),
    State("date-of-birth", "value"),
    State("nationality", "value"),
    State("sex", "value"),
    State("proof-of-id_number", "value"),
    State("email", "value"),
    State("username", "value"),
    State("password", "value"),

    prevent_initial_call=True,
)
def save_investor_data(
    n_clicks,
    first_name,
    last_name,
    date_of_birth,
    nationality,
    sex,
    proof_of_id_number,
    email,
    username,
    password
):

    if not n_clicks:
        return None

    fields = {
        "First name": first_name,
        "Last name": last_name,
        "Date of birth": date_of_birth,
        "Nationality": nationality,
        "Sex": sex,
        "Proof of ID Number": proof_of_id_number,
        "Email": email,
        "Username": username,
        "Password": password
    }

    missing_fields = [
        field_name
        for field_name, value in fields.items()
        if value is None or str(value).strip() == ""
    ]

    if missing_fields:

        return html.Div(
            [
                html.P(
                    "Please populate all fields before saving."
                ),

                html.P(
                    "Missing fields: "
                    + ", ".join(missing_fields)
                ),
            ],

            style={
                "fontWeight": "bold",
            },
        )
# ================================================================
# Save investor data to the database
# ================================================================

    try:
        # 1. Save investor data
        investor_id = SaveInvestorData(
            first_name=first_name.strip(),
            last_name=last_name.strip(),
            date_of_birth=date_of_birth,
            nationality=nationality.strip(),
            sex=sex.strip(),
            proof_of_id_number=proof_of_id_number.strip(),
            email=email.strip(),
        )

        # 2. Save username and password
        SaveUsernameAndPassword(
            investorID=investor_id,
            username=username,
            password=password
        )

        # 3. Return only after both succeeded
        return html.Div(
            [
                html.P("Investor successfully saved."),
                html.P(f"Investor ID: {investor_id}"),
                html.P("Username and password successfully saved."),
            ],
            style={"fontWeight": "bold"},
        )

    except Exception as e:
        return html.Div(
            [
                html.P("The investor could not be saved."),
                html.P(f"Database error: {e}"),
            ],
            style={"fontWeight": "bold"},
        )

        


# ================================================================
# UPLOAD PROOF OF ID
# ================================================================

@callback(
    [
        Output("upload-status", "children"),
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

    prevent_initial_call=False,
)
def update_status(
    is_completed,
    file_names,
    upload_id,
):

    empty_values = (
        None,
        None,
        None,
        None,
        None,
        None,
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

    passport_data = None

    for filename in file_names:

        filename = os.path.basename(filename)

        document_name, extension = os.path.splitext(filename)

        destination_folder = os.path.join(
            UPLOAD_DIR,
            document_name
        )

        os.makedirs(
            destination_folder,
            exist_ok=True
        )

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

        if os.path.exists(source_file):

            os.replace(
                source_file,
                destination_file
            )

        else:

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

        try:

            passport_data = parse_passport(
                destination_file
            )

        except Exception as e:

            saved_files.append(
                f"File saved, but passport could not be read: {e}"
            )

            passport_data = None

        if temporary_folder and os.path.isdir(temporary_folder):

            try:

                os.rmdir(temporary_folder)

            except OSError:

                pass

        saved_files.append(
            destination_file
        )

    if passport_data:

        first_name = passport_data.get("first_name")
        last_name = passport_data.get("last_name")
        date_of_birth = passport_data.get("date_of_birth")
        nationality = passport_data.get("nationality")
        sex = passport_data.get("sex")
        passport_number = passport_data.get("passport_number")

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

        *empty_values,
    )

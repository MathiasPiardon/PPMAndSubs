import dash
from dash import html, dcc, Input, Output, State
import psycopg2

from utils.DBparams import db_params


# ============================================================
# Register page
# ============================================================

dash.register_page(__name__, path="/login")


# ============================================================
# Layout
# ============================================================

layout = html.Div(
    [

        # --------------------------------------------------------
        # Redirect component
        # --------------------------------------------------------

        dcc.Location(
            id="login-redirect",
            refresh=True
        ),

        # --------------------------------------------------------
        # Home link
        # --------------------------------------------------------

        dcc.Link(
            "⌂",
            href="/",
            style={
                "position": "absolute",
                "top": "15px",
                "left": "30px",
                "fontSize": "28px",
                "textDecoration": "none",
                "color": "#333",
                "zIndex": 1000,
            }
        ),

        # --------------------------------------------------------
        # Page title
        # --------------------------------------------------------

        html.H1(
            "Login",
            style={
            "fontSize": "40px",
            "fontFamily": "Times New Roman, serif",
            "textAlign": "center",
            "width": "100%",
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
        # Username
        # --------------------------------------------------------

        dcc.Input(
            id="Username",
            placeholder="Username",
            type="text",
            style={
                "width": "400px",
                "padding": "10px",
                "fontSize": "16px",
                "boxSizing": "border-box",
            }
        ),

        # --------------------------------------------------------
        # Password
        # --------------------------------------------------------

        dcc.Input(
            id="Password",
            placeholder="Password",
            type="password",
            style={
                "width": "400px",
                "padding": "10px",
                "fontSize": "16px",
                "boxSizing": "border-box",
            }
        ),

        # --------------------------------------------------------
        # Login button
        # --------------------------------------------------------

        html.Button(
            "Login",
            id="login-button",
            n_clicks=0,
            style={
                "width": "400px",
                "padding": "10px",
                "fontSize": "16px",
                "cursor": "pointer",
                "marginTop": "10px",
            }
        ),

        # --------------------------------------------------------
        # Login status/error message
        # --------------------------------------------------------

        html.Div(
            id="login-message",
            style={
                "width": "400px",
                "marginTop": "10px",
                "fontSize": "16px",
            }
        ),

    ],

    style={
        "display": "flex",
        "flexDirection": "column",
        "alignItems": "flex-start",
        "marginLeft": "30px",
        "gap": "10px",
    },
)


# ============================================================
# Login callback
# ============================================================

@dash.callback(
    Output("login-redirect", "pathname"),
    Output("login-message", "children"),

    Input("login-button", "n_clicks"),

    State("Username", "value"),
    State("Password", "value"),

    prevent_initial_call=True,
)
def login_user(n_clicks, username, password):

    # --------------------------------------------------------
    # Check that both fields have been entered
    # --------------------------------------------------------

    if not username or not password:
        return dash.no_update, html.Div(
            "Please enter both username and password.",
            style={"color": "red"}
        )

    # Remove accidental spaces around username
    username = username.strip()

    # --------------------------------------------------------
    # Connect to PostgreSQL and check credentials
    # --------------------------------------------------------

    connection = None

    try:

        connection = psycopg2.connect(**db_params)

        cursor = connection.cursor()

        query = """
            SELECT 1
            FROM "PPMAndSubs"."UserIDs"
            WHERE user_name = %s
              AND password = %s
            LIMIT 1
        """

        cursor.execute(
            query,
            (username, password)
        )

        user_exists = cursor.fetchone() is not None

        cursor.close()

        # ----------------------------------------------------
        # Successful login
        # ----------------------------------------------------

        if user_exists:

            return "/select-managers", ""

        # ----------------------------------------------------
        # Invalid credentials
        # ----------------------------------------------------

        return dash.no_update, html.Div(
            "Invalid username or password.",
            style={"color": "red"}
        )

    # --------------------------------------------------------
    # Database error
    # --------------------------------------------------------

    except psycopg2.Error as e:

        print(f"Database error during login: {e}")

        return dash.no_update, html.Div(
            "Unable to connect to the database. Please try again later.",
            style={"color": "red"}
        )

    finally:

        if connection is not None:
            connection.close()
import calendar
from datetime import date

import dash
from dash import html, dcc, dash_table
import psycopg2

from utils.DBparams import db_params

import plotly.graph_objects as go


dash.register_page(__name__, path="/positions")


default_investor_id = 6


def get_last_12_completed_months():
    today = date.today()
    current_month = today.replace(day=1)

    months = []

    for i in range(12, 0, -1):
        year = current_month.year
        month = current_month.month - i

        while month <= 0:
            month += 12
            year -= 1

        months.append(date(year, month, 1))

    return months

def get_month_label(month_date):
    return month_date.strftime("%b-%Y")


def get_positions_data(investor_id):
    display_months = get_last_12_completed_months()

    first_display_month = display_months[0]
    last_display_month = display_months[-1]

    first_perf_year = first_display_month.year
    first_perf_month = first_display_month.month - 1

    if first_perf_month == 0:
        first_perf_month = 12
        first_perf_year -= 1

    first_perf_date = date(
        first_perf_year,
        first_perf_month,
        1,
    )

    last_perf_year = last_display_month.year
    last_perf_month = last_display_month.month - 1

    if last_perf_month == 0:
        last_perf_month = 12
        last_perf_year -= 1

    if last_perf_month == 12:
        end_perf_date = date(last_perf_year + 1, 1, 1)
    else:
        end_perf_date = date(
            last_perf_year,
            last_perf_month + 1,
            1,
        )

    connection = None

    try:
        connection = psycopg2.connect(**db_params)

        with connection.cursor() as cursor:

            # Get positions, including each fund's initial position date
            cursor.execute(
                """
                SELECT
                    p."fundID",
                    f.fund_name,
                    f.fund_manager,
                    p.initial_position,
                    p.initial_position_currency,
                    p.initial_position_date
                FROM "PPMAndSubs"."Positions" p
                LEFT JOIN "PPMAndSubs"."Funds" f
                    ON f."fundID" = p."fundID"
                WHERE p."investorID" = %s
                ORDER BY f.fund_name
                """,
                (investor_id,)
            )

            positions = cursor.fetchall()

            # Get performance for the overall display period
            cursor.execute(
                """
                SELECT
                    "fundID",
                    month,
                    perf
                FROM "PPMAndSubs"."FundsPerformance"
                WHERE month >= %s
                  AND month < %s
                ORDER BY "fundID", month
                """,
                (
                    first_perf_date,
                    end_perf_date,
                )
            )

            performance_rows = cursor.fetchall()

    finally:
        if connection is not None:
            connection.close()

    performance_by_fund = {}

    for fund_id, performance_date, perf in performance_rows:

        performance_year = performance_date.year
        performance_month = performance_date.month

        if performance_month == 1:
            display_year = performance_year - 1
            display_month = 12
        else:
            display_year = performance_year
            display_month = performance_month - 1

        display_month_date = date(
            display_year,
            display_month,
            1,
        )

        performance_by_fund.setdefault(
            fund_id,
            {}
        )[display_month_date] = perf

    rows = []

    for (
        fund_id,
        fund_name,
        fund_manager,
        initial_position,
        initial_currency,
        initial_position_date,
    ) in positions:

        row = {
            "fundID": fund_id,
            "fund_name": fund_name,
            "fund_manager": fund_manager,
            "currency": initial_currency,
            "position_initial": initial_position,
            "position_final": None,
        }

        # Only display performance for months AFTER the fund's
        # initial_position_date.
        for month_date in display_months:

            value = None

            if initial_position_date is not None:

                # Normalize initial_position_date to the first day
                # of its month for comparison.
                if hasattr(initial_position_date, "date"):
                    initial_position_month = initial_position_date.date().replace(
                        day=1
                    )
                else:
                    initial_position_month = initial_position_date.replace(
                        day=1
                    )

                # Only show performance for months strictly AFTER
                # the initial position month.
                if month_date >= initial_position_month:
                    value = performance_by_fund.get(
                        fund_id,
                        {}
                    ).get(month_date)

            row[
                f"month_{month_date.strftime('%Y_%m')}"
            ] = value

        rows.append(row)

    total_row = {
        "fund_name": "Total",
        "fund_manager": None,
        "currency": None,
        "position_initial": None,
        "position_final": None,
    }

    for month_date in display_months:
        total_row[
            f"month_{month_date.strftime('%Y_%m')}"
        ] = None

    rows.append(total_row)

    return rows, display_months



def CalculateFinalAndTotalPosition(table_rows, display_months):
    """
    Calculate the final position for every fund.

    Formula:
        Final Position =
            Initial Position
            * (1 + month_1)
            * (1 + month_2)
            * ...
            * (1 + month_n)

    For the Total row:
        Position Initial = sum of all fund initial positions
        Position Final   = sum of all fund final positions
    """

    total_initial_position = 0
    total_final_position = 0

    for row in table_rows:

        # Skip the Total row while calculating individual funds
        if row.get("fund_name") == "Total":
            continue

        initial_position = row.get("position_initial")

        if initial_position is None:
            row["position_final"] = None
            continue

        # Add to total initial position
        total_initial_position += initial_position

        # Calculate compounded final position
        final_position = initial_position

        for month_date in display_months:

            column_id = f"month_{month_date.strftime('%Y_%m')}"
            performance = row.get(column_id)

            # Ignore months where there is no performance
            if performance is not None:
                final_position *= (1 + performance)

        row["position_final"] = final_position

        # Add to total final position
        total_final_position += final_position

    # Update the Total row
    for row in table_rows:

        if row.get("fund_name") == "Total":
            row["position_initial"] = total_initial_position
            row["position_final"] = total_final_position
            break

    return table_rows


def CalculateFundsNAV(table_rows, display_months):
    """
    Calculate monthly NAV for every fund.

    The NAV for the month immediately before the first month
    with performance is 100.

    For each subsequent month:

        NAV = Previous NAV * (1 + monthly performance)

    Returns:
        funds_nav = {
            fundID: {
                month_date: nav
            }
        }
    """

    funds_nav = {}

    for row in table_rows:

        # Ignore Total row
        if row.get("fund_name") == "Total":
            continue

        fund_id = row.get("fundID")

        if fund_id is None:
            continue

        # Find the first month for which performance exists
        first_perf_month = None

        for month_date in display_months:
            column_id = f"month_{month_date.strftime('%Y_%m')}"
            performance = row.get(column_id)

            if performance is not None:
                first_perf_month = month_date
                break

        # No performance available for this fund
        if first_perf_month is None:
            funds_nav[fund_id] = {}
            continue

        nav_by_month = {}

        # NAV starts at 100 in the month immediately before
        # the first month for which performance exists.
        first_month_index = display_months.index(first_perf_month)

        if first_month_index > 0:
            previous_month = display_months[first_month_index - 1]
            nav_by_month[previous_month] = 100.0

        # Calculate NAV from the first performance month onwards
        nav = 100.0

        for month_date in display_months[first_month_index:]:

            column_id = f"month_{month_date.strftime('%Y_%m')}"
            performance = row.get(column_id)

            if performance is not None:
                performance = float(performance)
                nav *= (1 + performance)
                nav_by_month[month_date] = nav

        funds_nav[fund_id] = nav_by_month

    return funds_nav





table_rows, display_months = get_positions_data(
    default_investor_id
)

table_rows = CalculateFinalAndTotalPosition(
    table_rows,
    display_months
)

funds_nav = CalculateFundsNAV(
    table_rows,
    display_months
)

# we calcualte the NAV for each fund and plot it in a line chart using Plotly
nav_figure = go.Figure()

for row in table_rows:

    if row.get("fund_name") == "Total":
        continue

    fund_id = row.get("fundID")
    fund_name = row.get("fund_name")

    nav_data = funds_nav.get(fund_id, {})

    if not nav_data:
        continue

    x_values = list(nav_data.keys())
    y_values = list(nav_data.values())

    nav_figure.add_trace(
        go.Scatter(
            x=x_values,
            y=y_values,
            mode="lines",
            name=fund_name,
        )
    )

nav_figure.update_layout(
    title="Fund NAV",
    xaxis_title="Date",
    yaxis_title="NAV",
    hovermode="x unified",
    template="plotly_white",
    margin=dict(l=60, r=30, t=60, b=50),
)

# here we define the columns for the DataTable, including the initial position, monthly performance, and final position. The monthly performance columns are dynamically generated based on the display_months list.
columns = [
    {
        "name": "Hedge Fund",
        "id": "fund_name",
    },
    {
        "name": "Manager",
        "id": "fund_manager",
    },
    {
        "name": "Currency",
        "id": "currency",
    },
    {
        "name": "Position Initial",
        "id": "position_initial",
        "type": "numeric",
        "format": dash_table.Format.Format(
            precision=2,
            scheme=dash_table.Format.Scheme.fixed,
            group=True,
        ),
    },
]


for month_date in display_months:

    column_id = f"month_{month_date.strftime('%Y_%m')}"

    columns.append(
        {
            "name": get_month_label(month_date),
            "id": column_id,
            "type": "numeric",
            "format": dash_table.Format.Format(
                precision=2,
                scheme=dash_table.Format.Scheme.percentage,
            ),
        }
    )


columns.append(
    {
        "name": "Position Final",
        "id": "position_final",
        "type": "numeric",
        "format": dash_table.Format.Format(
            precision=2,
            scheme=dash_table.Format.Scheme.fixed,
            group=True,
        ),
    }
)

# here we define the layout of the page, which includes a title, a horizontal line, a message area for login status or errors, and a DataTable to display the positions data. The DataTable is styled for better readability and usability.
layout = html.Div(
    [

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

        html.H1(
            "Positions",
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

        html.Div(
            id="login-message",
            style={
                "width": "400px",
                "marginTop": "10px",
                "fontSize": "16px",
            }
        ),

        html.Div(
            dash_table.DataTable(
                id="positions-table",
                columns=columns,
                data=table_rows,
                sort_action="native",
                sort_mode="single",
                page_action="none",
                style_table={
                    "overflowX": "auto",
                    "width": "100%",
                    "minWidth": "1400px",
                },
                style_cell={
                    "fontFamily": "Arial, sans-serif",
                    "fontSize": "14px",
                    "padding": "10px 12px",
                    "textAlign": "right",
                    "whiteSpace": "nowrap",
                    "minWidth": "100px",
                    "width": "100px",
                    "maxWidth": "180px",
                },
                style_cell_conditional=[
                    {
                        "if": {
                            "column_id": "fund_name"
                        },
                        "textAlign": "left",
                        "minWidth": "180px",
                        "width": "220px",
                        "maxWidth": "300px",
                    },
                    {
                        "if": {
                            "column_id": "fund_manager"
                        },
                        "textAlign": "left",
                        "minWidth": "150px",
                        "width": "180px",
                        "maxWidth": "250px",
                    },
                    {
                        "if": {
                            "column_id": "currency"
                        },
                        "textAlign": "center",
                        "minWidth": "80px",
                        "width": "80px",
                        "maxWidth": "100px",
                    },
                ],
                style_header={
                    "backgroundColor": "#f2f2f2",
                    "fontWeight": "bold",
                    "border": "1px solid #cccccc",
                    "textAlign": "center",
                    "whiteSpace": "normal",
                    "height": "45px",
                },
                style_data={
                    "border": "1px solid #dddddd",
                },
                style_data_conditional=[
                    {
                        "if": {
                            "filter_query": '{fund_name} = "Total"'
                        },
                        "fontWeight": "bold",
                        "backgroundColor": "#f7f7f7",
                        "borderTop": "2px solid #333333",
                    },
                ],
            ),
            style={
                "width": "calc(100vw - 60px)",
                "maxWidth": "1800px",
                "marginTop": "20px",
            },
        ),
        # NAV chart below the grid
        html.Div(
            dcc.Graph(
                id="funds-nav-chart",
                figure=nav_figure,
                style={
                    "width": "100%",
                    "height": "300px",
                },
            ),
            style={
                "width": "calc(100vw - 60px)",
                "maxWidth": "1800px",
                "marginTop": "30px",
            },
        ),

    ],
    style={
        "display": "flex",
        "flexDirection": "column",
        "alignItems": "flex-start",
        "marginLeft": "30px",
        "marginRight": "30px",
        "gap": "10px",
        "width": "calc(100% - 60px)",
    },
)


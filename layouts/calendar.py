from dash import html, dcc, dash_table as dt
import dash_bootstrap_components as dbc


tabs = dbc.CardHeader(
        dbc.Tabs(
            [
                dbc.Tab(label="UTC", tab_id="utc", className="tab_heading"),
                dbc.Tab(label="Central EU", tab_id="central_eu", className="tab_heading"),
                dbc.Tab(label="UK", tab_id="uk", className="tab_heading"),
                dbc.Tab(label="US Pacific", tab_id="us_pacific", className="tab_heading"),
                dbc.Tab(label="US Mountain", tab_id="us_mountain", className="tab_heading"),
                dbc.Tab(label="US Central", tab_id="us_central", className="tab_heading"),
                dbc.Tab(label="US Eastern", tab_id="us_eastern", className="tab_heading"),
            ],
            id="tz_tabs", 
            active_tab="central_eu"
        )
    )



content = html.Div(id="tz-tab-content")

layout = html.Div([
    dbc.Alert("We obviously do not guarentee completeness/correctness. If you find errors, please write to McVizn or Dremet on Discord.", 
        color="dark", 
        style={"margin-top": "10px"}
    ),
    dbc.Card([
        tabs,
        dbc.CardBody(content)
    ])
])
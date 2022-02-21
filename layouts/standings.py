from dash import html, dcc, dash_table as dt
import dash_bootstrap_components as dbc


layout = html.Div([
    dbc.Row(
        [dbc.Col([
            html.H5("Championship", className="dropdown_header"),
            dcc.Dropdown(
                id='season_cs',
                options=[
                    {'label': 'ICSTC', 'value': 'ICSTC'},
                    {'label': 'ICSES', 'value': 'ICSES'},
                    {'label': 'ICSAS', 'value': 'ICSAS'}
                ],
                value='ICSTC'
            )]
        ),
        dbc.Col([
            html.H5("League", className="dropdown_header"),
            dcc.Dropdown(
                id='season_league',
                options=[
                    {'label': 'Superstars', 'value': 'Superstars'},
                    {'label': 'Experts', 'value': 'Experts'},
                    {'label': 'Pros', 'value': 'Pros'},
                    {'label': 'Semi Pros', 'value': 'Semi Pros'},
                    {'label': 'Amateur', 'value': 'Amateur'}
                ],
                value='Superstars'
            )]
        ),
        dbc.Col([
            html.H5("Season", className="dropdown_header"),
            dcc.Dropdown(
                id='season',
                options=[
                    {'label': '2', 'value': '2'},
                    {'label': '3', 'value': '3'}
                ],
                value='3'
            )]
        )]
    ),
    dbc.Row(dbc.Col(
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.P(
                            "", 
                            id="cs_description_standings",
                            style={"margin":"2px"}
                        )
                    ]
                )
            ], 
            color="dark", 
            inverse=True,
            style={"margin-bottom": "10px", "margin-top": "10px"}
        )
    )),
    dbc.Row([
        dbc.Col([html.H3("Teams", className="graph_header"), dcc.Graph(id="team_standings")], id="col_team_standings")
    ]),
    dbc.Row([
        dbc.Col(
            dt.DataTable(
                id='team_standings_table', 
                style_cell={
                    'whiteSpace': 'pre-line'
                }
            ),
            id="col_team_standings_table"
        )
    ]),
    dbc.Row([
        dbc.Col([html.H3("Drivers", className="graph_header"), dcc.Graph(id="driver_standings")])
    ])
])
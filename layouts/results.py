from dash import html, dcc, dash_table as dt
import dash_bootstrap_components as dbc


layout = html.Div([dbc.Row([
    dbc.Col([
        html.H5("Championship", className="dropdown_header"),
        dcc.Dropdown(
            id='race_cs',
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
            id='race_league',
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
            id='race_season',
            options=[
                #{'label': '1', 'value': '1'},
                {'label': '2', 'value': '2'}
            ],
            value='2'
        )]
    ),
    dbc.Col([
        html.H5("Event Date", className="dropdown_header"),
        dcc.Dropdown(
            id='race_event',
            #options=[],
            #value=''
        )]
    ),
    dbc.Col([
        html.H5("Race", className="dropdown_header"),
        dcc.Dropdown(
            id='race',
            #options=[],
            #value=''
        )]
    )
    ]
),
dbc.Row(dbc.Col(
    dbc.Card(
        [
            dbc.CardBody(
                [
                    html.P(
                        "", 
                        id="cs_description_race_results",
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
dbc.Row([html.H3("Race Details", className="table_header")], style={"margin-top":"10px"}),
dbc.Row([
    dbc.Col(
        dt.DataTable(
            id='race_table', 
            style_cell={
                'whiteSpace': 'pre-line'
            }
        )
    )
]),

dbc.Row([html.H3("Race Results", className="table_header")], style={"margin-top":"10px"}),
dbc.Row([
    dbc.Col(
        dt.DataTable(
            id='driver_race_table', 
            style_cell={
                'whiteSpace': 'pre-line'
            }
        )
    )
    #dcc.Graph(id="lap_table")
]),
])
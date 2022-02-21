from dash import html, dcc, dash_table as dt
import dash_bootstrap_components as dbc


layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.H5("Championship", className="dropdown_header"),
            dcc.Dropdown(
                id='misc_cs',
                options=[
                    {'label': 'ICSTC', 'value': 'ICSTC'},
                    {'label': 'ICSES', 'value': 'ICSES'},
                    {'label': 'ICSAS', 'value': 'ICSAS'}
                ],
                value='ICSTC'
            )]
        ),
        dbc.Col([
            html.H5("Season", className="dropdown_header"),
            dcc.Dropdown(
                id='misc_season',
                options=[
                    {'label': '1', 'value': '1'},
                    {'label': '2', 'value': '2'}
                ],
                value='2'
            )]
        )
    ]),dbc.Row(dbc.Col(
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.P(
                            "", 
                            id="cs_description_misc",
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
    dbc.Row(
        dbc.Col([
            dbc.Card(
                [
                    dbc.CardHeader("Explanation of analyses below:"),
                    dbc.CardBody(
                        [
                            html.H5("Calculations performed among all players across all leagues", className="card-title"),
                            html.P(
                                "Players that missed one or more races are excluded in the content below. A full league is excluded, if there are no race times for any race. When players where lapped, their average lap time is added to the race time multiplied by the amount of lappings. "
                                "The overall ranking can be highly influenced by one single very bad race result. "
                                "Possible future change: Delete worst race result before calculating mean position so that one bad result has no effect.", 
                                className="card-text",
                            ),
                        ]
                    ),
                    dbc.CardFooter("Hence, it is less useful to see who is worse than expected in the respective league, but useful to see who should be up higher in terms of the league they are in.", id="important-footer-note")
                ], color="warning", outline=True
            )
        ]),
        style={"margin-top":"15px", "margin-bottom":"15px"}
    ),
    dbc.Row([html.H3("Virtual Table", className="table_header")], style={"margin-top":"10px"}),
    dbc.Row([
        dbc.Col(
            dt.DataTable(
                id='virtual_table', 
                style_cell={
                    'whiteSpace': 'pre-line'
                }
            )
        )
        ]
    ),
    dbc.Row([html.H3("League Clouds", className="table_header")], style={"margin-top":"10px"}),
    dbc.Row([dbc.Col(
        dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.H5("In order to understand, which data was used, please see the info box above.", className="card-title"),
                            html.P(
                                "This graph called 'League Clouds' gives an overview of skill differences between leagues. "
                                "If applicable: Given a certain skill (=certain sum of race time) one gets less points in higher leagues than in the lower ones. "
                                "If leagues would be perfectly balanced, you would see parallel lines with different colors (=leagues) next to each other with the highest league on the left. ", 
                                className="card-text",
                            ),
                        ]
                    )
                ], color="warning", outline=True
            )
    )]),
    dbc.Row([dcc.Graph(id="league_clouds")])
])
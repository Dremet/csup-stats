from dash import html, dcc, dash_table as dt
import dash_bootstrap_components as dbc
from callbacks import drivers

layout = html.Div([
        #,
        # dbc.Row(dcc.Dropdown(
        #     id='region',
        #     options=[
        #         {'label': 'World', 'value': 'world'},
        #         {'label': 'Europe', 'value': 'EU'},
        #         {'label': 'North America', 'value': 'NA'},
        #         {'label': 'South America', 'value': 'SA'}
        #     ],
        #     value='world'
        # )),
        # dbc.Row([
            
        # ])
        dbc.Row([
            dbc.Col([html.H3("ELO Skill Level", className="graph_header")])
        ]),
        dbc.Row(dbc.Col(
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.P(
                                [
                                    "The ELO value is a measure of the skill of a driver. It is calculated on the basis of past competitions. The calculation is not done by the operators of this site, but by muritopin, one of the organizers of the ICSTC. ",
                                    "For more details see this Excel file used as a data source: ",
                                    dcc.Link("Link to Excel file", href="https://docs.google.com/spreadsheets/d/1vDXzmsh4Idv98Nxi5eWOPecIGkyklb12/edit#gid=1801297124")
                                ], 
                                id="driver_elo_description",
                                style={"margin":"2px"}
                            )
                        ]
                    )
                ], 
                color="light", 
                style={"margin-bottom": "10px", "margin-top": "10px"}
            )
        )),
        dbc.Row([
            dbc.Col([
                html.H3("Region Selection for ELO Table", className="dropdown_header"),
                html.P([
                    "Choose a region to see the ELO positions from all drivers from a specific region but keep in mind that the region is not available for every driver. Drivers from unknown regions are only displayed when 'World' is selected. ",
                ]),
                dcc.Dropdown(
                    id='driver_region',
                    options=[
                        {'label': 'World', 'value': 'World'},
                        {'label': 'EU', 'value': 'EU'},
                        {'label': 'NA', 'value': 'NA'},
                        {'label': 'SA', 'value': 'SA'}
                    ],
                    value='World'
                ),
                dbc.Alert("This dropdown is for the table on the right!", color="danger", style={"margin-top":"5px", "margin-bottom":"15px"}),
                html.H3("Origin", className="graph_header"), 
                drivers.update_drivers_region_graph(),
                html.H3("Device", className="graph_header"), 
                drivers.update_drivers_device_graph()
            ]),
            dbc.Col([
                html.P([
                    html.Span("Last update: "),
                    html.Span(id="elo_last_updated")
                ], style={"display":"inline"}),
                dt.DataTable(
                    id='driver_elo_table', 
                    style_cell={
                        'whiteSpace': 'pre-line'
                    }
                )
                ]
            )
        ])
])
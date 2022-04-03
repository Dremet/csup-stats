from dash import html
import dash_bootstrap_components as dbc


###############################################
###         HEADER & NAVIGATION             ###
###############################################

header = html.Div([
        dbc.Row(html.H1("Circuit Superstars Statistics Dashboard")),
        dbc.Col(dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4("Notes", className="card-title"),
                        html.P(
                            "This is a community project by Dremet and McVizn. Data is entered manually by hand, which is why there will always be some kind of delay after races are finished.", 
                            className="card-text"
                        )
                    ]
                ),
                dbc.CardFooter("If you have suggestions regarding improvements of this dashboard, feel free to contact Dremet on Discord."),
            ], 
            color="info", 
            #inverse=True,
            style={"margin-bottom": "10px"}
        ))
])

tabs = dbc.CardHeader(
        dbc.Tabs(
            [
                dbc.Tab(label="Season Standings", tab_id="season_standings", className="tab_heading"),
                dbc.Tab(label="Race Results", tab_id="race_results", className="tab_heading"),
                dbc.Tab(label="Drivers", tab_id="drivers", className="tab_heading"),
                dbc.Tab(label="Misc", tab_id="misc", className="tab_heading"),
                dbc.Tab(label="Calendar", tab_id="calendar", className="tab_heading"),
                dbc.Tab(label="Development", tab_id="dev", className="tab_heading"),
            ],
            id="tabs", 
            active_tab="season_standings"
        )
    )



content = html.Div(id="tab-content")

footer = html.Div(
    dbc.Alert("Feel free to use the graphs wherever you like, but please mention https://csup-stats.herokuapp.com/ as the source.", 
    color="dark", 
    style={"margin-top": "10px"})
)

layout = dbc.Container([
    header,
    dbc.Card([
        tabs,
        dbc.CardBody(content)
    ]),
    footer
])
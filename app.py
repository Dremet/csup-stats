from click import style
import dash
from dash import dcc, html, dash_table as dt
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np

from plotly.graph_objs import Layout

from functions import get_df, read_driver_data, get_team_standings_cumulative, get_driver_standings_cumulative, get_race_meta_data_and_race_results

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.LUMEN])
app.config.suppress_callback_exceptions=True

server = app.server
transparent_layout = Layout()
transparent_layout = Layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(225,225,225,100)'
    )
#  bs-light  253,246,227
#  bs-info   38,139,210



###############################################
###         HEADER & NAVIGATION             ###
###############################################

header = html.Div([
        dbc.Row(html.H1("Circuit Superstars Statistics Dashboard")),
        dbc.Card(
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
            inverse=True,
            style={"margin-bottom": "10px"}
        )
])

tabs = dbc.CardHeader(
        dbc.Tabs(
            [
                dbc.Tab(label="Season Standings", tab_id="season_standings"),
                dbc.Tab(label="Race Results", tab_id="race_results"),
                dbc.Tab(label="Drivers", tab_id="drivers")
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

app.layout = dbc.Container([
    header,
    dbc.Card([
        tabs,
        dbc.CardBody(content)
    ]),
    footer
])

@app.callback(
    dash.dependencies.Output("tab-content", "children"),
    dash.dependencies.Input("tabs", "active_tab")
)
def render_tab_content(active_tab):
    if active_tab == "season_standings":
        return html.Div([
                    dbc.Row(
                        [dbc.Col(
                            dcc.Dropdown(
                                id='season_cs',
                                options=[
                                    {'label': 'ICSTC', 'value': 'ICSTC'},
                                    #{'label': 'ICSES', 'value': 'ICSES'}
                                ],
                                value='ICSTC'
                            )
                        ),
                        dbc.Col(
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
                            )
                        ),
                        dbc.Col(
                            dcc.Dropdown(
                                id='season',
                                options=[
                                    {'label': '1', 'value': '1'},
                                    {'label': '2', 'value': '2'}
                                ],
                                value='2'
                            )
                        )]
                    ),
                    dbc.Row([
                        dbc.Col(dcc.Graph(id="team_standings")),
                        dbc.Col(dcc.Graph(id="driver_standings"))
                    ])
                ])
    elif active_tab == "race_results":
        return html.Div([dbc.Row([
                        dbc.Col(
                            dcc.Dropdown(
                                id='race_cs',
                                options=[
                                    {'label': 'ICSTC', 'value': 'ICSTC'},
                                    #{'label': 'ICSES', 'value': 'ICSES'}
                                ],
                                value='ICSTC'
                            )
                        ),
                        dbc.Col(
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
                            )
                        ),
                        dbc.Col(
                            dcc.Dropdown(
                                id='race_season',
                                options=[
                                    #{'label': '1', 'value': '1'},
                                    {'label': '2', 'value': '2'}
                                ],
                                value='2'
                            )
                        ),
                        dbc.Col(
                            dcc.Dropdown(
                                id='race',
                                options=[
                                    {'label': '2022-01-09', 'value': '20220109'},
                                    {'label': '2022-01-16', 'value': '20220116'},
                                    {'label': '2022-01-23', 'value': '20220123'}
                                ],
                                value='20220123'
                            )
                        )
                        ]
                    ),
                    dbc.Row([html.H3("Race Details")], style={"margin-top":"10px"}),
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

                    dbc.Row([html.H3("Race Results")], style={"margin-top":"10px"}),
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
    elif active_tab == "drivers":
        return html.Div([
                    dbc.Row([
                        dbc.Col(update_drivers_region_graph()),
                        dbc.Col(update_drivers_device_graph())
                        ]
                    )
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
                ])
    
    return html.P("No tab selected")
    #misc_tab = dbc.Tab(label = "Misc", children = [])

###############################################
###          Dropdown Callbacks             ###
###############################################

@app.callback(
    [dash.dependencies.Output("season_league", "options"), dash.dependencies.Output("season_league", "value")], 
    dash.dependencies.Input("season_cs", "value")
)
def update_available_leagues(season_cs):
    if season_cs == "ICSTC":
        return [
                {'label': 'Superstars', 'value': 'Superstars'},
                {'label': 'Experts', 'value': 'Experts'},
                {'label': 'Pros', 'value': 'Pros'},
                {'label': 'Semi Pros', 'value': 'Semi Pros'},
                {'label': 'Amateur', 'value': 'Amateur'}
            ], "Superstars"
    elif season_cs == "ICSES":
        return [
                {'label': 'Group A', 'value': 'A'},
                {'label': 'Group B', 'value': 'B'},
                {'label': 'Group C', 'value': 'C'}
            ], "A"
    else:
        return [], None

###############################################
###            Season Standings             ###
###############################################

@app.callback(
    dash.dependencies.Output('team_standings', 'figure'),
    [dash.dependencies.Input('season_cs', 'value'), dash.dependencies.Input('season_league', 'value'), dash.dependencies.Input('season', 'value')],
)
def update_team_standings_graph(season_cs, season_league, season):
    df = get_team_standings_cumulative(cs=season_cs, league=season_league, season=season)
    df["track_car"] = df["r_track"]+"\n"+df["r_car"]

    df.sort_values("e_date", inplace=True, ascending=True)
    #print(df)
    fig = px.line(df, x="track_car", y="points_cum", color="t_name", title='Team Standings')
    fig.layout = transparent_layout

    return fig


@app.callback(
    dash.dependencies.Output('driver_standings', 'figure'),
    [dash.dependencies.Input('season_cs', 'value'), dash.dependencies.Input('season_league', 'value'), dash.dependencies.Input('season', 'value')],
)
def update_driver_standings_graph(season_cs, season_league, season):
    df = get_driver_standings_cumulative(cs=season_cs, league=season_league, season=season)
    df["track_car"] = df["r_track"]+"\n"+df["r_car"]

    df.sort_values("e_date", inplace=True, ascending=True)

    fig = px.line(df, x="track_car", y="points_cum", color="d_name", title='Driver Standings')
    fig.layout = transparent_layout

    return fig


###############################################
###            Race Results                 ###
###############################################

@app.callback(
    [dash.dependencies.Output("driver_race_table", "columns"), dash.dependencies.Output("driver_race_table", "data"),
    dash.dependencies.Output("race_table", "columns"), dash.dependencies.Output("race_table", "data")],
    [
        dash.dependencies.Input('race_cs', 'value'), dash.dependencies.Input('race_league', 'value'), 
        dash.dependencies.Input('race_season', 'value'), dash.dependencies.Input('race', 'value')
    ]
)
def update_drivers_race_table(race_cs, race_league, race_season, race):
    df_meta, df_race = get_race_meta_data_and_race_results(cs=race_cs, league=race_league, season=race_season, event=race)
    
    df_meta.rename(columns={
        "e_date" : "Date", 
        "r_track" : "Track", 
        "r_version" : "Version",
        "r_reversed" : "Reversed", 
        "r_laps" : "Laps", 
        "r_car" : "Car", 
        "r_tire_wear" : "Tire Wear", 
        "r_fuel_consumption" : "Fuel", 
        "r_damage_cars" : "Car Damage", 
        "r_damage_environment" : "Env Damage",
        "r_drafting" : "Drafting",
        "r_has_reversed_grid" : "Reverse Grid",
        "r_details_were_announced" : "Announced"
        }, 
        inplace=True
    )

    df_race.rename(columns={
        "d_name" : "Driver", 
        "t_tag" : "Team Tag", 
        "q_lap_time_seconds" : "Quali Time",
        "quali_points" : "Quali Points", 
        "rr_fastest_lap_seconds" : "Fastest Lap", 
        "fastest_lap_points" : "Points Fastest Lap", 
        "rr_race_time_seconds" : "Race Time", 
        "race_points" : "Race Points", 
        "points" : "Points"
        }, 
        inplace=True
    )

    def sec_to_readable_time(secs):
        if np.isnan(secs):
            return "-"
        secs = float(secs)
        
        str_min = str(int(np.floor(secs/60)))
        str_secs = str(int(np.floor(secs%60))).zfill(2)
        str_msecs = str(int(np.round(secs%1*1000))).zfill(3)

        return f"{str_min}:{str_secs}.{str_msecs}"
    
    df_race["Race Time"] = df_race["Race Time"].apply(sec_to_readable_time)
    
    df_race.sort_values("Race Points", ascending=False, inplace=True)

    results_columns = [{"name": i, "id": i} for i in df_race.columns]
    results_data = df_race.to_dict('records')

    meta_columns = [{"name": i, "id": i} for i in df_meta.columns]
    meta_data = df_meta.to_dict('records')

    return results_columns, results_data, meta_columns, meta_data

# @app.callback(
#     dash.dependencies.Output('lap_table', 'figure'),
#     dash.dependencies.Input('league', 'value')
# )
# def update_lap_table_graph(league):
#     df = get_df(league, "lap_table")
#     fig = px.line(df, x="Lap", y="Pos", color="driver name", title='Track Position')
#     fig.layout = transparent_layout
#     return fig


###############################################
###               Drivers                   ###
###############################################

def update_drivers_region_graph():
    df = read_driver_data()

    df_grouped = df.groupby(['d_two_letter_continent_code', 'd_two_letter_country_code']).size().reset_index(name='counts')

    fig = px.sunburst(df_grouped, path=["d_two_letter_continent_code", "d_two_letter_country_code"], values="counts")

    fig.layout = transparent_layout

    return dcc.Graph(id="region_overview", figure=fig)

def update_drivers_device_graph():
    df = read_driver_data()

    df["d_steering_device"] = df["d_steering_device"].replace(
        {
            "controller" : "Controller",
            "keyboard" : "Keyboard",
            "alternating" : "Both",
            "" : "?"
        }
    )

    df_grouped = df.groupby(['d_steering_device']).size().reset_index(name='counts')

    fig = px.sunburst(df_grouped, path=["d_steering_device"], values="counts")

    fig.layout = transparent_layout

    return dcc.Graph(id="region_overview", figure=fig)



if __name__ == "__main__":
    app.run_server(debug=True)
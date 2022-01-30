from click import style
import dash
from dash import dcc, html, dash_table as dt
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import date

from plotly.graph_objs import Layout

from functions import *

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
                        [dbc.Col([
                            html.H5("Championship", className="dropdown_header"),
                            dcc.Dropdown(
                                id='season_cs',
                                options=[
                                    {'label': 'ICSTC', 'value': 'ICSTC'},
                                    #{'label': 'ICSES', 'value': 'ICSES'}
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
                                    {'label': '1', 'value': '1'},
                                    {'label': '2', 'value': '2'}
                                ],
                                value='2'
                            )]
                        )]
                    ),
                    dbc.Row([
                        dbc.Col([html.H3("Teams", className="graph_header"), dcc.Graph(id="team_standings")]),
                        dbc.Col([html.H3("Drivers", className="graph_header"), dcc.Graph(id="driver_standings")])
                    ])
                ])
    elif active_tab == "race_results":
        return html.Div([dbc.Row([
                        dbc.Col([
                            html.H5("Championship", className="dropdown_header"),
                            dcc.Dropdown(
                                id='race_cs',
                                options=[
                                    {'label': 'ICSTC', 'value': 'ICSTC'},
                                    #{'label': 'ICSES', 'value': 'ICSES'}
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
                                options=[],
                                value=''
                            )]
                        ),
                        dbc.Col([
                            html.H5("Race", className="dropdown_header"),
                            dcc.Dropdown(
                                id='race',
                                options=[],
                                value=''
                            )]
                        )
                        ]
                    ),
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
    elif active_tab == "drivers":
        return html.Div([
                    dbc.Row([
                        dbc.Col([html.H3("Origin", className="graph_header"), update_drivers_region_graph()]),
                        dbc.Col([html.H3("Device", className="graph_header"), update_drivers_device_graph()])
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
    elif active_tab == "misc":
        return html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.H5("Championship", className="dropdown_header"),
                            dcc.Dropdown(
                                id='misc_cs',
                                options=[
                                    {'label': 'ICSTC', 'value': 'ICSTC'}
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
                    ]),
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
                                                "Given a certain skill (=certain sum of race time) one gets less points in higher leagues than in the lower ones. "
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
    elif active_tab == "dev":
        return html.Div([
                    dbc.Row([
                        html.H3("Roadmap", className="table_header"),
                        html.P("The items are roughly ordered in terms of their priority from high to low.")
                    ]),
                    dbc.Row([
                        dbc.Accordion(
                        [
                            dbc.AccordionItem(
                                [
                                    html.P("In order to easier compare points, the season standings will be shown in a table as well. Will be located below the season standing graphs."),
                                    dbc.Alert("Low effort", color="success")
                                ],
                                title="Season Standings as Table",
                            ),
                            dbc.AccordionItem(
                                [
                                    html.P("Within the season standings tab, a table will be added for both drivers as well if teams (if there are teams) that shows the number of achievements per driver/team: #Wins, #Poles, #FastestLaps, #TeamWins, #DoubleWins, ..."),
                                    dbc.Alert("Medium effort", color="primary")
                                ],
                                title="Achievements",
                            ),
                            dbc.AccordionItem(
                                [
                                    html.P("On the drivers tab, a table showing the amount of overall race participations, won races, poles etc. Obviously, this is limited to the championships that are being considered worth adding to the database."),
                                    dbc.Alert("Medium effort", color="primary")
                                ],
                                title="Driver Statistics",
                            ),
                            dbc.AccordionItem(
                                [
                                    html.P("Based on feedback the plots will be improved in terms of their structure/description/colors."),
                                    dbc.Alert("Medium effort", color="primary")
                                ],
                                title="Prettify Graphs",
                            ),
                            dbc.AccordionItem(
                                [
                                    html.P("Add data for ICSES and ICSAS. You will be able to select those championships in the first dropdown menu on all tabs respectively."),
                                    dbc.Alert("High effort", color="warning")
                                ],
                                title="Add ICSES and ICSAS",
                            ),
                            dbc.AccordionItem(
                                [
                                    html.P("Optimize database queries to lower loading times."),
                                    dbc.Alert("Medium effort", color="primary")
                                ],
                                title="Optimize Performance",
                            ),
                            dbc.AccordionItem(
                                [
                                    html.P("For certain races, McVizn puts in the time to create a lap table showing the position of every driver each lap. This can be added to the race results, if available."),
                                    dbc.Alert("Medium effort", color="primary")
                                ],
                                title="Lap Table",
                            ),
                            dbc.AccordionItem(
                                [
                                    html.P("Calculate ELO for all drivers and on the drivers tab, a table with the current ELO ranking of each driver as well as a graph with the historical changes in ELO of each driver will be added. Currently in discussions with Bixon und Muritopin. There is a lot to discuss and code."),
                                    dbc.Alert("Very high effort", color="danger")
                                ],
                                title="ELO Ranking",
                            ),
                            dbc.AccordionItem(
                                [
                                    html.P("Add data from other championships like TDRL or others."),
                                    dbc.Alert("High effort", color="warning")
                                ],
                                title="Add more Championships",
                            ),
                            dbc.AccordionItem(
                                [
                                    html.P("This site is currently hosted on a free tier hosting option on heroku. If it is used regularly, I will upgrade it to a non-free option to increase performance."),
                                    dbc.Alert("Medium effort", color="primary")
                                ],
                                title="Evaluate Hosting Options",
                            ),
                        ],start_collapsed=True
                    ), 
                    ]),
                    dbc.Row([
                        dbc.Col(
                            dbc.Alert("You have more suggestions? Message me (Dremet#7626) on Discord. You also find me on the official Circuit Superstars or ICSTC discord.", color="warning"),
                            style={"margin-top": "15px"}
                        )
                    ])
                ])
    
    return html.P("No tab selected")
    #misc_tab = dbc.Tab(label = "Misc", children = [])

###############################################
###          Dropdown Callbacks             ###
###############################################

# season standings
@app.callback(
    [dash.dependencies.Output("season_league", "options"), dash.dependencies.Output("season_league", "value")], 
    dash.dependencies.Input("season_cs", "value")
)
def update_available_leagues_for_season_standings(season_cs):
    leagues = get_league_by_cs(season_cs)
    options = [{'label': league, 'value': league} for league in leagues]
    default = leagues[0]
    return options, default

@app.callback(
    [dash.dependencies.Output("season", "options"), dash.dependencies.Output("season", "value")], 
    [dash.dependencies.Input("season_cs", "value"), dash.dependencies.Input("season_league", "value")]
)
def update_available_seasons_for_season_standings(season_cs, season_league):
    seasons = get_seasons_by_cs_and_league(season_cs, season_league)
    options = [{'label': season, 'value': season} for season in seasons]
    default = max(seasons)
    return options, default

# race results
@app.callback(
    [dash.dependencies.Output("race_league", "options"), dash.dependencies.Output("race_league", "value")], 
    dash.dependencies.Input("race_cs", "value")
)
def update_available_leagues_for_race_results(race_cs):
    leagues = get_league_by_cs(race_cs)
    options = [{'label': league, 'value': league} for league in leagues]
    default = leagues[0]
    return options, default

@app.callback(
    [dash.dependencies.Output("race_season", "options"), dash.dependencies.Output("race_season", "value")], 
    [dash.dependencies.Input("race_cs", "value"), dash.dependencies.Input("race_league", "value")]
)
def update_available_seasons_for_race_results(race_cs, race_league):
    seasons = get_seasons_by_cs_and_league(race_cs, race_league)
    options = [{'label': season, 'value': season} for season in seasons]
    default = max(seasons)
    return options, default

@app.callback(
    [dash.dependencies.Output("race_event", "options"), dash.dependencies.Output("race_event", "value")], 
    [dash.dependencies.Input("race_cs", "value"), dash.dependencies.Input("race_league", "value"), dash.dependencies.Input("race_season", "value")]
)
def update_available_events_for_race_results(race_cs, race_league, race_season):
    events = get_events_by_cs_league_and_season(race_cs, race_league, race_season)
    
    events = events.loc[events["e_date"] < date.today(), :]
    #events["e_date_str"] = pd.to_datetime(events["e_date"]).dt.strftime("%Y%m%d")
    labels, values = events["e_date"].to_list(), events["e_id"].to_list()
    options = [{'label': label, 'value': value} for label, value in zip(labels, values)]
    default = values[-1]
    return options, default

@app.callback(
    [dash.dependencies.Output("race", "options"), dash.dependencies.Output("race", "value")], 
    dash.dependencies.Input("race_event", "value")
)
def update_available_events_for_race_results(race_event):
    races = get_races_by_event(race_event)
    options = [{'label': race, 'value': race} for race in races]
    default = races[0]
    return options, default


# Misc
@app.callback(
    [dash.dependencies.Output("misc_season", "options"), dash.dependencies.Output("misc_season", "value")], 
    dash.dependencies.Input("misc_cs", "value")
)
def update_available_leagues_for_season_standings(misc_cs):
    seasons = get_seasons_by_cs(misc_cs)
    options = [{'label': season, 'value': season} for season in seasons]
    default = max(seasons)
    return options, default


###############################################
###            Season Standings             ###
###############################################

@app.callback(
    dash.dependencies.Output('team_standings', 'figure'),
    [dash.dependencies.Input('season_cs', 'value'), dash.dependencies.Input('season_league', 'value'), dash.dependencies.Input('season', 'value')],
)
def update_team_standings_graph(season_cs, season_league, season):
    df = get_team_standings_cumulative(cs=season_cs, league=season_league, season=season)
    df["track_car"] = df["r_track"]+" - "+df["r_car"]
    
    df.sort_values("e_date", inplace=True, ascending=True)
    df = df.reset_index()
    
    fig = px.line(df, x="track_car", y="points_cum", color="t_name", title='Team Standings')
    fig.layout = transparent_layout

    fig.update_layout(
        #title="Plot Title",
        #xaxis_title="X Axis Title",
        yaxis_title="Points",
        legend_title="Team",
        # font=dict(
        #     family="Courier New, monospace",
        #     size=18,
        #     color="RebeccaPurple"
        # )
    )

    return fig


@app.callback(
    dash.dependencies.Output('driver_standings', 'figure'),
    [dash.dependencies.Input('season_cs', 'value'), dash.dependencies.Input('season_league', 'value'), dash.dependencies.Input('season', 'value')],
)
def update_driver_standings_graph(season_cs, season_league, season):
    df = get_driver_standings_cumulative(cs=season_cs, league=season_league, season=season)
    df["track_car"] = df["r_track"]+" - "+df["r_car"]

    df.sort_values("e_date", inplace=True, ascending=True)

    fig = px.line(df, x="track_car", y="points_cum", color="d_name", title='Driver Standings')
    fig.layout = transparent_layout

    fig.update_layout(
        #title="Plot Title",
        #xaxis_title="X Axis Title",
        yaxis_title="Points",
        legend_title="Driver",
        # font=dict(
        #     family="Courier New, monospace",
        #     size=18,
        #     color="RebeccaPurple"
        # )
    )

    return fig


###############################################
###            Race Results                 ###
###############################################

@app.callback(
    [dash.dependencies.Output("driver_race_table", "columns"), dash.dependencies.Output("driver_race_table", "data"),
    dash.dependencies.Output("race_table", "columns"), dash.dependencies.Output("race_table", "data")],
    [
        dash.dependencies.Input('race_cs', 'value'), dash.dependencies.Input('race_league', 'value'), 
        dash.dependencies.Input('race_season', 'value'), dash.dependencies.Input('race_event', 'value'),
        dash.dependencies.Input('race', 'value')
    ]
)
def update_drivers_race_table(race_cs, race_league, race_season, race_event, race):
    df_meta, df_race = get_race_meta_data_and_race_results(cs=race_cs, league=race_league, season=race_season, event_id=race_event, race=race)
    
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



###############################################
###                 Misc                    ###
###############################################

@app.callback(
    [
        dash.dependencies.Output("virtual_table", "columns"), dash.dependencies.Output("virtual_table", "data")
    ],
    [
        dash.dependencies.Input('misc_cs', 'value'), dash.dependencies.Input('misc_season', 'value')
    ]
)
def update_virtual_table(misc_cs, misc_season):
    df = get_virtual_table_data(misc_cs, misc_season)

    df["mean_place"] = df["mean_place"].round(1)

    df.rename(columns={
        "d_name" : "Driver", 
        "l_name" : "League", 
        "mean_place" : "Average Overall Place"
        }, 
        inplace=True
    )

    columns = [{"name": i, "id": i} for i in df.columns]
    data = df.to_dict('records')

    return columns, data


@app.callback(
    dash.dependencies.Output('league_clouds', 'figure'),
    [
        dash.dependencies.Input('misc_cs', 'value'), dash.dependencies.Input('misc_season', 'value')
    ]
)
def update_league_clouds(misc_cs, misc_season):
    df = get_league_clouds(misc_cs, misc_season)

    df["sum_race_times"] = df["sum_race_times"]/60.

    df.rename(columns={
        "d_name" : "Driver", 
        "l_name" : "League", 
        "sum_race_times" : "Sum Race Times [min]",
        "points_sum" : "Sum Points"
        }, 
        inplace=True
    )

    fig = px.scatter(df, x="Sum Race Times [min]", y="Sum Points", color="League", hover_data=['Driver'], size = "Sum Points") #,size='petal_length'

    return fig


###############################################
if __name__ == "__main__":
    app.run_server(debug=True)
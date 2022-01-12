import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd

from functions import get_df

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([
    html.H1("Circuit Superstars Statistics Dashboard"),
    html.P("This is a community project. Administration and coding by Dremet and data aggregation by McVizn."),
    dcc.Dropdown(
        id='league',
        options=[
            {'label': 'ICSTC Superstars', 'value': 'superstars'},
            {'label': 'ICSTC Experts', 'value': 'experts'}
        ],
        value='superstars'
    ),
    dcc.Graph(id="driver_race_points"),
    #dcc.Graph(id="team_race_points"),
    dcc.Graph(id="lap_table"),
    html.P("(c)")
])

@app.callback(
    dash.dependencies.Output('driver_race_points', 'figure'),
    dash.dependencies.Input('league', 'value')
)
def update_race_points_graph(league):
    df = get_df(league, "driver_race_points")
    df["color"] = df["racepoints"]
    df.loc[df["color"].isnull(), "color"] = 0
    df["color"] = df["color"].astype(int)
    number_racers = len(df.index)

    standard_colors = []

    for i in range(number_racers-3):
        standard_colors.append("blue")

    colors = ["gold","silver","bronze"]+standard_colors

    color_discrete_map = {}
    for points, color in zip(df["color"].values, colors):
        points_save = points if points >= 0 else 0

        color_discrete_map[int(points_save)] = color

    print(df["color"].astype(int).values)
    print(color_discrete_map)

    fig = px.bar(df, x="driver name", y="racepoints", color="color", title='Race Points', color_discrete_map=color_discrete_map)

    return fig

@app.callback(
    dash.dependencies.Output('lap_table', 'figure'),
    dash.dependencies.Input('league', 'value')
)
def update_lap_table_graph(league):
    df = get_df(league, "lap_table")
    fig = px.line(df, x="Lap", y="Pos", color="driver name", title='Track Position')
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
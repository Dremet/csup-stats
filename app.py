import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd

from functions import get_df

app = dash.Dash()

server = app.server

app.layout = html.Div([
    dcc.Dropdown(
        id='league',
        options=[
            {'label': 'ICSTC Superstars', 'value': 'superstars'},
            {'label': 'ICSTC Experts', 'value': 'experts'}
        ],
        value='superstars'
    ),
    dcc.Graph(id="driver_race_points"),
    dcc.Graph(id="lap_table")
])

@app.callback(
    dash.dependencies.Output('driver_race_points', 'figure'),
    dash.dependencies.Input('league', 'value')
)
def update_race_points_graph(league):
    df = get_df(league, "driver_race_points")

    fig = px.line(df, x="driver name", y="racepoints", title='Race Points')

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
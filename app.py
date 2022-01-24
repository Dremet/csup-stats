import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd

from functions import get_df,read_driver_data

app = dash.Dash(__name__)

server = app.server


###############################################
###               Drivers                   ###
###############################################

def update_drivers_region_graph():
    df = read_driver_data()

    df_grouped = df.groupby(['d_two_letter_continent_code', 'd_two_letter_country_code']).size().reset_index(name='counts')

    fig = px.sunburst(df_grouped, path=["d_two_letter_continent_code", "d_two_letter_country_code"], values="counts")

    fig.update_layout(paper_bgcolor="#D3D3D3")

    return dcc.Graph(id="region_overview", figure=fig)


app.layout = html.Div([
    html.H1("Circuit Superstars Statistics Dashboard"),
    html.P("This is a community project. Administration and coding by Dremet and data aggregation by McVizn."),
    dcc.Tabs([
        dcc.Tab(label = "Race Results", children = [
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
            dcc.Graph(id="lap_table")
        ]),
        dcc.Tab(label = "Drivers", children = [
            update_drivers_region_graph(),
            dcc.Dropdown(
                id='region',
                options=[
                    {'label': 'World', 'value': 'world'},
                    {'label': 'Europe', 'value': 'EU'},
                    {'label': 'North America', 'value': 'NA'},
                    {'label': 'South America', 'value': 'SA'}
                ],
                value='world'
            ),
            dcc.Graph(id="steering_device"),
            dcc.Graph(id="drivers_table")
        ])
    ]),
    html.P("(c)")
])

###############################################
###            Race Results                 ###
###############################################

@app.callback(
    dash.dependencies.Output('driver_race_points', 'figure'),
    dash.dependencies.Input('league', 'value')
)
def update_race_points_graph(league):
    df = get_df(league, "driver_race_points")

    fig = px.bar(df, x="driver name", y="racepoints", title='Race Points')
    return fig

# @app.callback(
#     dash.dependencies.Output('team_race_points', 'figure'),
#     dash.dependencies.Input('league', 'value')
# )
# def update_team_race_points_graph(league):
#     df = get_df(league, "team_race_points")

#     fig = px.bar(df, x="team name", y="racepoints", title='Team Race Points')
#     return fig

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
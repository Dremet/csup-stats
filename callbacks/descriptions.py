import dash
from main import app
from functions import *

###############################################
###        Championship Description         ###
###############################################
@app.callback(
    dash.dependencies.Output('cs_description_standings', 'children'),
    dash.dependencies.Input('season_cs', 'value'),
)
def show_cs_description_standings(season_cs):
    return get_cs_description(season_cs)

@app.callback(
    dash.dependencies.Output('cs_description_race_results', 'children'),
    dash.dependencies.Input('race_cs', 'value'),
)
def show_cs_description_race_results(season_cs):
    return get_cs_description(season_cs)

@app.callback(
    dash.dependencies.Output('cs_description_misc', 'children'),
    dash.dependencies.Input('misc_cs', 'value'),
)
def show_cs_description_misc(season_cs):
    return get_cs_description(season_cs)


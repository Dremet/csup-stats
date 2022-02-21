import dash
from datetime import date
from functions import *
from main import app

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
def update_dropdowns_misc(misc_cs):
    seasons = get_seasons_by_cs(misc_cs)
    print("seasons", seasons)
    options = [{'label': season, 'value': season} for season in seasons]
    default = max(seasons)
    return options, default
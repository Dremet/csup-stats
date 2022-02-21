import dash
from functions import *
from layout_helper import *
from main import app
import numpy as np

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
        "rr_position" : "Pos",
        "rr_fastest_lap_seconds" : "Fastest Lap", 
        "fastest_lap_points" : "Points Fastest Lap", 
        "rr_race_time_seconds" : "Race Time", 
        "rr_penalty_description" : "Penalty", 
        "race_points" : "Race Points", 
        "points" : "Points"
        }, 
        inplace=True
    )

    df_race.sort_values("Pos", ascending=True, inplace=True)

    df_race.loc[df_race["Pos"].isnull(), "Pos"] = 0
    df_race["Pos"] = df_race["Pos"].astype(int).astype(str)
    df_race.loc[df_race["Pos"]=="0", "Pos"] = "DNS"

    def sec_to_readable_time(secs):
        if np.isnan(secs):
            return "-"
        secs = float(secs)
        
        str_min = str(int(np.floor(secs/60)))
        str_secs = str(int(np.floor(secs%60))).zfill(2)
        str_msecs = str(int(np.round(secs%1*1000))).zfill(3)

        return f"{str_min}:{str_secs}.{str_msecs}"
    
    
    df_race["Race Time"] = df_race["Race Time"].apply(sec_to_readable_time)
    
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


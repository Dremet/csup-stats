from math import exp
from typing import List
import pandas as pd 
import numpy as np
from connection import Connection

from pathlib import Path

PATH_SQL_TEMPLATES=Path("sql/")

def read_sql_template(sql_file):
    file_path = PATH_SQL_TEMPLATES / sql_file
    return file_path.read_text().replace('\n', ' ')

def does_cs_contain_teams(cs):
    with Connection() as conn:
        cs = pd.read_sql("select c_has_teams from base.championships where c_name = %(cs)s", 
            params=dict(zip(["cs"],[cs])),
            con=conn)
    
    return cs["c_has_teams"].iloc[0]

def get_cs_description(cs):
    with Connection() as conn:
        cs = pd.read_sql("select c_description from base.championships where c_name = %(cs)s", 
            params=dict(zip(["cs"],[cs])),
            con=conn)
    
    return cs["c_description"].iloc[0]

def get_league_by_cs(cs) -> List:
    with Connection() as conn:
        leagues = pd.read_sql("select l_name from base.leagues l "
            "left join base.championships c on c_name = %(cs)s "
            "where l.c_c_id = c.c_id", 
            params=dict(zip(["cs"],[cs])),
            con=conn)
    
    return leagues["l_name"].to_list()


def get_seasons_by_cs(cs) -> List:
    with Connection() as conn:
        seasons = pd.read_sql("select s_desc from base.seasons s "
            "left join base.leagues l on s.l_l_id = l.l_id "
            "left join base.championships c on l.c_c_id = c.c_id " 
            "where c_name = %(cs)s ", 
            params=dict(zip(["cs"],[cs])),
            con=conn)
    
    return pd.unique(seasons["s_desc"])


def get_seasons_by_cs_and_league(cs, league) -> List:
    with Connection() as conn:
        seasons = pd.read_sql("select s_desc from base.seasons s "
            "left join base.leagues l on l_name = %(league)s "
            "left join base.championships c on c_name = %(cs)s "
            "where s.l_l_id = l.l_id and l.c_c_id = c.c_id", 
            params=dict(zip(["cs", "league"],[cs, league])),
            con=conn)
    
    return seasons["s_desc"].to_list()


def get_events_by_cs_league_and_season(cs, league, season) -> pd.DataFrame:
    with Connection() as conn:
        events = pd.read_sql("select e_date, e_id from base.events e "
            "left join base.seasons s on s_desc = %(season)s "
            "left join base.leagues l on l_name = %(league)s "
            "left join base.championships c on c_name = %(cs)s "
            "where e.s_s_id = s.s_id and s.l_l_id = l.l_id and l.c_c_id = c.c_id", 
            params=dict(zip(["cs", "league", "season"],[cs, league, season])),
            con=conn)
    
    return events


def get_races_by_event(e_id) -> List:
    with Connection() as conn:
        print(e_id)
        races = pd.read_sql("select r_order from base.races r "
            "where r.e_e_id = %(e_id)s", 
            params=dict(zip(["e_id"],[int(e_id)])),
            con=conn)
        print(races)
    
    return races["r_order"].to_list()


def read_driver_data():
    with Connection() as conn:
        df = pd.read_sql("select * from base.drivers", con=conn)
    
    df.loc[df['d_two_letter_continent_code'] == '', 'd_two_letter_continent_code'] = "?"
    df.loc[df['d_two_letter_country_code'] == '', 'd_two_letter_country_code'] = "?"

    return df

def get_current_elo(region):
    with Connection() as conn:
        cur = conn.cursor()

        if region in ["EU", "NA", "SA"]:
            sql = read_sql_template("get_latest_elo_by_region.sql")
            cur.execute(sql, dict(zip(["region"], [region])))
        else:
            sql = read_sql_template("get_latest_elo.sql")
            cur.execute(sql)

        df = pd.DataFrame(cur.fetchall(), columns = ["d_name", "elo_ranking", "elo_date", "d_steering_device"])
    
    df.sort_values("elo_ranking", ascending=False, inplace=True)

    df["rank"] = df["elo_ranking"].rank(method="min", ascending=False)
    
    return df

def get_driver_results(cs, league, season):
    with Connection() as conn:
        sql = read_sql_template("get_results_by_c_l_s.sql")
        cur = conn.cursor()
        
        cur.execute(sql, dict(zip(["cs","league","season"], [cs, league, season])))
        columns = [desc[0] for desc in cur.description]

        df = pd.DataFrame(cur.fetchall(), columns = columns)
        
    # drop rows with r_id = NaN
    # this can happen if future events are in the database f.e.
    df.dropna(subset=["r_id"], inplace=True)
    
    assert len(df.loc[df["e_uses_event_points"],:]) == 0, "Can only calculate points up until now, if e_uses_event_points is False."

    # df = df[['r_id', 'e_e_id', 'r_order', 'r_track', 'r_version', 'r_reversed',
    #     'r_laps', 'r_car', 'r_class', 'r_tire_wear', 'r_fuel_consumption',
    #     'r_damage_cars', 'r_damage_environment', 'r_drafting',
    #     'r_is_ghost_race', 'r_has_reversed_grid', 'r_details_were_announced',
    #     'e_id', 's_s_id', 'e_date', 'e_uses_event_points', 'e_points_pos_1',
    #     'e_points_pos_2', 'e_points_pos_3', 'e_points_pos_4', 'e_points_pos_5',
    #     'e_points_pos_6', 'e_points_pos_7', 'e_points_pos_8', 'e_points_pos_9',
    #     'e_points_pos_10', 'e_points_pos_11', 'e_points_pos_12',
    #     'e_points_for_pole', 'e_points_for_fastest_lap', 's_id', 'l_l_id',
    #     's_desc', 'l_id', 'c_c_id', 'l_name', 'c_id', 'c_name', 'c_has_teams',
    #     'c_region', 'rr_id', 'r_r_id', 'd_d_id', 'rr_position',
    #     'rr_race_time_seconds', 'rr_lappings', 'rr_fastest_lap_seconds', 'q_id',
    #     'r_r_id', 'd_d_id', 'q_position', 'q_lap_time_seconds', 'tm_id',
    #     'd_d_id', 't_t_id', 's_s_id', 't_id', 't_name', 't_tag',
    #     't_primary_color', 't_secondary_color', 't_tertiary_color', 'd_id',
    #     'd_name', 'd_two_letter_country_code', 'd_two_letter_continent_code',
    #     'd_steering_device', 'd_elo', 'points', 'quali_points',
    #     'fastest_lap_points', 'has_fastest_race_lap', 'has_fastest_quali_lap',
    #     'race_points']]

    # we do not need the foreign keys when we have the primary keys
    df.drop(labels=[
        'e_e_id', 'l_l_id','c_c_id', 'r_r_id', 'd_d_id', 't_t_id', 's_s_id'
    ],
        axis="columns", 
        inplace=True
    )

    df = df[['r_id', 'r_order', 'r_track', 'r_version', 'r_reversed',
        'r_laps', 'r_car', 'r_class', 'r_tire_wear', 'r_fuel_consumption',
        'r_damage_cars', 'r_damage_environment', 'r_drafting',
        'r_is_ghost_race', 'r_has_reversed_grid', 'r_details_were_announced',
        'e_id', 'e_date', 'e_uses_event_points', 'e_points_pos_1',
        'e_points_pos_2', 'e_points_pos_3', 'e_points_pos_4', 'e_points_pos_5',
        'e_points_pos_6', 'e_points_pos_7', 'e_points_pos_8', 'e_points_pos_9',
        'e_points_pos_10', 'e_points_pos_11', 'e_points_pos_12',
        'e_points_for_pole', 'e_points_for_fastest_lap', 's_id', 
        's_desc', 'l_id', 'l_name', 'c_id', 'c_name', 'c_has_teams',
        'c_region', 'rr_id', 'rr_position', 'rr_penalty_description',
        'rr_race_time_seconds', 'rr_lappings', 'rr_fastest_lap_seconds', 'q_id',
        'q_position', 'q_lap_time_seconds', 'tm_id',
        't_id', 't_name', 't_tag',
        't_primary_color', 't_secondary_color', 't_tertiary_color', 'd_id',
        'd_name', 'd_two_letter_country_code', 'd_two_letter_continent_code',
        'd_steering_device', 'd_elo']]
    
    
    # fill gaps
    df = fill_race_gaps(df)

    # calculate points for each race attendand 
    df["points"] = 0
    df["race_points"] = 0
    df["quali_points"] = 0
    df["fastest_lap_points"] = 0
    df["has_fastest_race_lap"] = False
    df["has_fastest_quali_lap"] = False
    
    fastest_laps = df.groupby(df.r_id)[["rr_fastest_lap_seconds", "q_lap_time_seconds"]].min()
    
    for r_id, row in fastest_laps.iterrows():
        df.loc[(df.r_id == r_id) & (df.rr_fastest_lap_seconds == row["rr_fastest_lap_seconds"]), "has_fastest_race_lap"] = True
        df.loc[(df.r_id == r_id) & (df.q_lap_time_seconds == row["q_lap_time_seconds"]), "has_fastest_quali_lap"] = True
    
    df.loc[df.has_fastest_race_lap, "fastest_lap_points"] = df.loc[df.has_fastest_race_lap, "e_points_for_fastest_lap"]
    df.loc[df.has_fastest_quali_lap, "quali_points"] = df.loc[df.has_fastest_quali_lap, "e_points_for_pole"]

    #print(df[["rr_fastest_lap_seconds", "q_lap_time_seconds","has_fastest_race_lap", "has_fastest_quali_lap", "points"]])

    # assign race points depending on the e_points_pos_X columns, if a race position is given
    df["race_points"] = df.apply(lambda x: x[f"e_points_pos_{int(x['rr_position'])}"] if not np.isnan(x['rr_position']) else 0, axis=1)
    
    # add race points to previously calculated points from fastest lap and pole
    df["points"] = df["quali_points"] + df["fastest_lap_points"] + df["race_points"]

    # we want to calculate cumulative points in the order in which the races took place
    # so we sort by date ascending
    # group the points by driver and race
    # do magic
    # and then calculate the cumsum and reverse the index         
    df.sort_values("e_date", ascending=True, inplace = True)
    df_points_cum = df[["r_id", "d_id", "points"]].groupby(["d_id", "r_id"], sort=False).sum().groupby(level=0).cumsum().reset_index()
    
    # create points_cum column using a join
    df = df.set_index(["r_id", "d_id"]).join(df_points_cum.set_index(["r_id", "d_id"]), rsuffix="_cum").reset_index()

    # calculate overall sum of points
    df["points_sum"] = df[["d_id", "points"]].groupby(["d_id"]).transform("sum")["points"]
    
    #pd.set_option('display.max_columns', None)
    
    return df


def get_driver_standings_cumulative(cs, league, season):
    df = get_driver_results(cs, league, season)[["d_name", "r_track", "r_car", "e_date", "points_cum"]]

    return df


def get_team_standings_cumulative(cs, league, season):
    df = get_driver_results(cs, league, season)[["t_name", "r_track", "r_car", "e_date", "points_cum", "d_name"]]

    return df.groupby(["e_date","r_track", "r_car","t_name"], sort=False).sum().reset_index().sort_values("e_date", ascending=True)

def get_race_meta_data_and_race_results(cs, league, season, event_id, race):
    df = get_driver_results(cs, league, season)
    df["e_date_str"] = pd.to_datetime(df["e_date"]).dt.strftime("%Y%m%d")
    
    df = df.loc[(df["e_id"]==event_id) & (df["r_order"]==race),:]
    
    df_meta = df[[
        "e_date","r_track", "r_version", "r_reversed", "r_laps", "r_car", "r_tire_wear", "r_fuel_consumption", "r_damage_cars", "r_damage_environment", "r_drafting", "r_has_reversed_grid", "r_details_were_announced"
    ]].iloc[[0],:]

    df_race = df[[
         "rr_position", "d_name", "t_tag", "q_lap_time_seconds", "quali_points","rr_fastest_lap_seconds", "fastest_lap_points", "rr_race_time_seconds", "rr_penalty_description", "race_points", "points"
    ]]

    if not does_cs_contain_teams(cs):
        del df_race["t_tag"]

    return df_meta, df_race

def fill_race_gaps(df):
    df.set_index(["r_id", "d_id"], inplace=True)

    df = df.reindex(pd.MultiIndex.from_product(df.index.levels)).reset_index()
    
    # fill gaps
    for col in ["r_id", "d_id"]:
        cols_same_table = [c for c in df.columns if c.startswith(col.split("_")[0]+"_") and c!=col]

        # we can fill out the team columns, if we know the driver
        if col == "d_id":
            cols_same_table += [c for c in df.columns if c.startswith("t_")]

        # we can fill the event info, if we know the race
        if col == "r_id":
            cols_same_table += [c for c in df.columns if c.startswith("e_")]
        
        df[cols_same_table] = df.groupby(col)[cols_same_table].ffill()
        df[cols_same_table] = df.groupby(col)[cols_same_table].bfill()
    
    return df

def get_league_spanning_data(cs, season):
    with Connection() as conn:
        sql = read_sql_template("get_results_by_c_s.sql")
        cur = conn.cursor()
        
        cur.execute(sql, dict(zip(["cs","season"], [cs, season])))
        columns = [desc[0] for desc in cur.description]

        df = pd.DataFrame(cur.fetchall(), columns = columns)
    
    # drop rows with r_id = NaN
    # this can happen if future events are in the database f.e.
    df.dropna(subset=["r_id"], inplace=True)
    
    # ICSTC, Season 3, Experts were not able to race due to server issues
    # all other four leagues did race and are excluded here
    df.drop(df[df.r_id.isin([268,269,270,271])].index, inplace=True)

    # we do not need the foreign keys when we have the primary keys
    df.drop(labels=[
        'e_e_id', 'l_l_id','c_c_id', 'r_r_id', 'd_d_id', 't_t_id', 's_s_id'
    ],
        axis="columns", 
        inplace=True
    )

    df_leagues = []
    
    for league in pd.unique(df["l_name"]):
        # gap filling functions can only handle races from one league
        # otherwise it would combine drivers from league A with races from league B,
        # which we do not want
        df_leagues.append(fill_race_gaps(df.loc[df["l_name"]==league,:]))
    
    df = pd.concat(df_leagues)

    return df

def get_virtual_table_data(cs, season):
    df = get_league_spanning_data(cs, season)

    # get rid of results with not entries for the race time
    df.dropna(subset=["rr_race_time_seconds"], inplace=True)

    # we need to get rid of the players that missed a race or more
    df["count"] = 1
    max_attendances = df.groupby([df.d_name, df.l_name]).sum()["count"].max()
    df = df.groupby([df.d_name, df.l_name]).filter(lambda x: len(x)==max_attendances)

    # we need to consider the lappings and add seconds to the race time
    df.fillna({"rr_lappings": 0}, inplace=True)

    df["time_added_lappings"] = df["rr_lappings"] * (df["rr_race_time_seconds"] / (df["r_laps"] - df["rr_lappings"]))

    df["virtual_time"] = df["time_added_lappings"] + df["rr_race_time_seconds"]
    
    # group by all race parameters to lower the chance for duplicates that would ruin the result
    df["virtual_place_race"] = df.groupby([
            df.r_order, df.r_track, df.r_version, df.r_reversed, df.r_laps, df.r_car, 
            df.r_class, df.r_tire_wear, df.r_fuel_consumption,
            df.r_damage_cars, df.r_damage_environment, df.r_drafting,
            df.r_is_ghost_race, df.r_has_reversed_grid, df.r_details_were_announced
        ])["virtual_time"].rank()
    
    # from now on, we only need these columns
    df = df[["d_name", "l_name", "virtual_place_race"]]

    df["mean_place"] = df.groupby(df.d_name)["virtual_place_race"].transform("mean")

    df = df[["d_name", "l_name", "mean_place"]]
    df.drop_duplicates(inplace=True)
    
    return df.sort_values("mean_place", ascending = True)


def get_league_clouds(cs, season):
    df = get_league_spanning_data(cs, season)

    # get rid of results with not entries for the race time
    df.dropna(subset=["rr_race_time_seconds"], inplace=True)
    
     # we need to get rid of the players that missed a race or more
    df["count"] = 1
    max_attendances = df.groupby([df.d_name, df.l_name]).sum()["count"].max()
    df = df.groupby([df.d_name, df.l_name]).filter(lambda x: len(x)==max_attendances)

    # we need to consider the lappings and add seconds to the race time
    df.fillna({"rr_lappings": 0}, inplace=True)

    df["time_added_lappings"] = df["rr_lappings"] * (df["rr_race_time_seconds"] / (df["r_laps"] - df["rr_lappings"]))

    df["virtual_time"] = df["time_added_lappings"] + df["rr_race_time_seconds"]
    
    df["sum_race_times"] = df.groupby([df.d_name, df.l_name])["virtual_time"].transform("sum")
    
    
    #print(df.loc[(df["r_track"] == "Maple Ridge"), ["d_name", "sum_race_times"]].sort_values("sum_race_times", ascending = True))
    df = df[["d_id", "d_name", "l_id", "l_name", "sum_race_times"]]
    df.drop_duplicates(inplace=True)

    df_points_list = []
    for league in pd.unique(df["l_name"]):
        df_points_list.append(get_driver_results(cs, league, season)[["d_name", "d_id", "l_id", "points_sum"]])
    
    df_points = pd.concat(df_points_list)

    df = df.set_index(["d_name", "d_id", "l_id"]).join(df_points.set_index(["d_name", "d_id", "l_id"])).reset_index()

    return df[["d_name", "l_name", "sum_race_times", "points_sum"]]


if __name__ == "__main__":
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    #get_df("experts", "team_race_points")
    #print(get_driver_standings("ICSTC","Superstars","2"))
    #print(get_driver_standings_cumulative("ICSTC","Superstars","2"))
    #get_team_standings_cumulative("ICSTC","Pros","1")
    get_league_clouds("ICSTC","2")
    pass
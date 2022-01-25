from math import exp
import pandas as pd 
import numpy as np
from connection import Connection

from pathlib import Path

PATH_SQL_TEMPLATES=Path("sql/")

def read_sql_template(sql_file):
    file_path = PATH_SQL_TEMPLATES / sql_file
    return file_path.read_text().replace('\n', ' ')


def get_df(league, cat=None):

    if cat=="driver_race_points":
        path = f"data/ICSTC/{league}/{cat}.csv"
        return read_driver_race_points(path)
    elif cat=="team_race_points":
        paths = {
            "driver_race_points": f"data/ICSTC/{league}/driver_race_points.csv",
            "teams" : f"data/ICSTC/{league}/teams.csv"
        }
        return read_team_race_points(paths)
    elif cat=="lap_table":
        path = f"data/ICSTC/{league}/{cat}.csv"
        return read_lap_table(path)
    
    raise Exception(f"{cat} not configured!")

def read_driver_race_points(path):
    df = pd.read_csv(path, sep=";")

    return df.sort_values(by="racepoints", ascending=False)

# def read_team_race_points(paths):
#     df_drivers = pd.read_csv(paths["driver_race_points"], sep=";")
#     df_teams = pd.read_csv(paths["teams"], sep=";").astype(str)

#     df_drivers["driver name"] = df_drivers["driver name"].astype(str)

#     print(df_drivers["driver name"])
#     print(df_teams["driver name"])

#     print(df_drivers.join(df_teams, on="driver name", lsuffix='_caller', rsuffix='_other'))

def read_lap_table(path):
    df = pd.read_csv(path, sep=";")
    
    df = pd.melt(df, id_vars="driver name", value_vars=df.columns[1:], var_name="Lap", value_name="Pos")

    df.dropna(how="any", inplace=True)

    return df

def read_driver_data():
    with Connection() as conn:
        df = pd.read_sql("select * from base.drivers", con=conn)
    
    df.loc[df['d_two_letter_continent_code'] == '', 'd_two_letter_continent_code'] = "?"
    df.loc[df['d_two_letter_country_code'] == '', 'd_two_letter_country_code'] = "?"

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

        # calculate points for each race attendand 
        df["points"] = 0
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
        df_points_cum = df.sort_values("e_date", ascending=True)[["r_id", "d_id", "points"]].groupby(["d_id", "r_id"]).sum().groupby(level=0).cumsum().reset_index()

        # create points_cum column using a join
        df = df.set_index(["r_id", "d_id"]).join(df_points_cum.set_index(["r_id", "d_id"]), rsuffix="_cum").reset_index()

        # calculate overall sum of points
        df["points_sum"] = df[["d_id", "points"]].groupby(["d_id"]).transform("sum")["points"]
        
        # return only columns needed for other functions
        return df


def get_driver_standings_cumulative(cs, league, season):
    #print(get_driver_results(cs, league, season)[["d_name", "r_track", "r_car", "points_cum"]])
    return get_driver_results(cs, league, season)[["d_name", "r_track", "r_car", "e_date", "points_cum"]]


def get_team_standings_cumulative(cs, league, season):
    df = get_driver_results(cs, league, season)[["t_name", "r_track", "r_car", "e_date", "points_cum"]]

    return df.groupby(["r_track", "r_car","t_name","e_date"]).sum().reset_index()

def get_race_meta_data_and_race_results(cs, league, season, event):
    df = get_driver_results(cs, league, season)
    df["e_date_str"] = pd.to_datetime(df["e_date"]).dt.strftime("%Y%m%d")
    df = df.loc[df["e_date_str"]==event,:]
    
    df_meta = df[[
        "e_date","r_track", "r_version", "r_reversed", "r_laps", "r_car", "r_tire_wear", "r_fuel_consumption", "r_damage_cars", "r_damage_environment", "r_drafting", "r_has_reversed_grid", "r_details_were_announced"
    ]].iloc[[0],:]

    df_race = df[[
        "d_name", "t_tag", "q_lap_time_seconds", "quali_points", "rr_fastest_lap_seconds", "fastest_lap_points", "rr_race_time_seconds", "race_points", "points"
    ]]

    return df_meta, df_race
    

if __name__ == "__main__":
    #get_df("experts", "team_race_points")
    #print(get_driver_standings("ICSTC","Superstars","2"))
    get_driver_results("ICSTC","Superstars","2")
    pass
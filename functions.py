from math import exp
import pandas as pd 

from connection import Connection

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



if __name__ == "__main__":
    get_df("experts", "team_race_points")
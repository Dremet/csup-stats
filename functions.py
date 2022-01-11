from math import exp
import pandas as pd 

def get_df(league, file):
    path = f"data/ICSTC/{league}/{file}.csv"

    if file=="driver_race_points":
        return read_driver_race_points(path)
    elif file=="lap_table":
        return read_lap_table(path)
    
    raise Exception(f"{file} not configured!")

def read_driver_race_points(path):
    df = pd.read_csv(path, sep=";")

    return df.sort_values(by="racepoints", ascending=False)

def read_lap_table(path):
    df = pd.read_csv(path, sep=";")
    
    df = pd.melt(df, id_vars="driver name", value_vars=df.columns[1:], var_name="Lap", value_name="Pos")

    df.dropna(how="any", inplace=True)

    return df
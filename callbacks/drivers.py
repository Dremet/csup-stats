from lib2to3.pgen2 import driver
from functions import *
from layout_helper import *
import plotly.express as px
import dash
from dash import dcc
from main import app

###############################################
###               Drivers                   ###
###############################################

def update_drivers_region_graph():
    df = read_driver_data()

    df_grouped = df.groupby(['d_two_letter_continent_code', 'd_two_letter_country_code']).size().reset_index(name='counts')

    fig = px.sunburst(df_grouped, path=["d_two_letter_continent_code", "d_two_letter_country_code"], values="counts")

    fig.layout = transparent_layout

    return dcc.Graph(id="region_overview", figure=fig)

def update_drivers_device_graph():
    df = read_driver_data()

    df["d_steering_device"] = df["d_steering_device"].replace(
        {
            "controller" : "Controller",
            "keyboard" : "Keyboard",
            "alternating" : "Both",
            "" : "?"
        }
    )

    df_grouped = df.groupby(['d_steering_device']).size().reset_index(name='counts')

    fig = px.sunburst(df_grouped, path=["d_steering_device"], values="counts")

    fig.layout = transparent_layout

    return dcc.Graph(id="region_overview", figure=fig)


@app.callback(
    [dash.dependencies.Output("driver_elo_table", "columns"), dash.dependencies.Output("driver_elo_table", "data"), dash.dependencies.Output("elo_last_updated", "children")],
    dash.dependencies.Input('driver_region', 'value'),
)
def update_team_standings_graph(driver_region):
    df = get_current_elo(driver_region)

    # data table
    df_table = df[["rank", "d_name", "elo_ranking", "d_steering_device"]]
    
    df_table.rename(columns={
        "d_name" : "Driver", 
        "elo_ranking" : "ELO",
        "rank" : "Position",
        "d_steering_device" : "Device"
        }, 
        inplace=True
    )

    df_table["Device"].replace({
        "controller" : "Controller",
        "keyboard" : "Keyboard",
        "alternating" : "Both",
        "" : "?"
    }, inplace=True)

    columns = [{"name": i, "id": i} for i in df_table.columns]
    data = df_table.to_dict('records')

    last_update = df["elo_date"].max()

    return columns, data, last_update
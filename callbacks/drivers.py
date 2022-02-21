from functions import *
from layout_helper import *
import plotly.express as px
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


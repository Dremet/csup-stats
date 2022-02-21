import dash
from functions import *
from layout_helper import *
from main import app
import plotly.express as px

###############################################
###                 Misc                    ###
###############################################

@app.callback(
    [
        dash.dependencies.Output("virtual_table", "columns"), dash.dependencies.Output("virtual_table", "data")
    ],
    [
        dash.dependencies.Input('misc_cs', 'value'), dash.dependencies.Input('misc_season', 'value')
    ]
)
def update_virtual_table(misc_cs, misc_season):
    df = get_virtual_table_data(misc_cs, misc_season)

    df = df.loc[df["l_name"] != "Final",:]

    df["mean_place"] = df["mean_place"].round(1)

    df.rename(columns={
        "d_name" : "Driver", 
        "l_name" : "League", 
        "mean_place" : "Average Overall Place"
        }, 
        inplace=True
    )

    columns = [{"name": i, "id": i} for i in df.columns]
    data = df.to_dict('records')

    return columns, data


@app.callback(
    dash.dependencies.Output('league_clouds', 'figure'),
    [
        dash.dependencies.Input('misc_cs', 'value'), dash.dependencies.Input('misc_season', 'value')
    ]
)
def update_league_clouds(misc_cs, misc_season):
    df = get_league_clouds(misc_cs, misc_season)

    df = df.loc[df["l_name"] != "Final",:]

    df["sum_race_times"] = df["sum_race_times"]/60.

    df.rename(columns={
        "d_name" : "Driver", 
        "l_name" : "League", 
        "sum_race_times" : "Sum Race Times [min]",
        "points_sum" : "Sum Points"
        }, 
        inplace=True
    )

    fig = px.scatter(df, x="Sum Race Times [min]", y="Sum Points", color="League", hover_data=['Driver'], size = "Sum Points", opacity=0.5) #,size='petal_length'

    return fig
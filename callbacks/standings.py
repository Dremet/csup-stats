import dash
from functions import *
from layout_helper import *
from main import app
import plotly.express as px

###############################################
###          Toogle Team Graphs             ###
###############################################
@app.callback(
    [dash.dependencies.Output('col_team_standings', 'style'), dash.dependencies.Output('col_team_standings_table', 'style')],
    dash.dependencies.Input('season_cs', 'value'),
)
def toggle_team_output(season_cs):
    if does_cs_contain_teams(season_cs):
        return {'display': 'block'}, {'display': 'block'}
    else:
        return {'display': 'none'}, {'display': 'none'}


###############################################
###            Season Standings             ###
###############################################

@app.callback(
    [dash.dependencies.Output('team_standings', 'figure'),dash.dependencies.Output("team_standings_table", "columns"), dash.dependencies.Output("team_standings_table", "data")],
    [dash.dependencies.Input('season_cs', 'value'), dash.dependencies.Input('season_league', 'value'), dash.dependencies.Input('season', 'value')],
)
def update_team_standings_graph(season_cs, season_league, season):
    df = get_team_standings_cumulative(cs=season_cs, league=season_league, season=season)
    df["track_car"] = df["r_track"]+" - "+df["r_car"]
    
    df.sort_values("e_date", inplace=True, ascending=True)
    df = df.reset_index()
    
    fig = px.line(df, x="track_car", y="points_cum", color="t_name", title='Team Standings', markers=True)
    fig.layout = transparent_layout

    fig.update_layout(
        #title="Plot Title",
        #xaxis_title="X Axis Title",
        yaxis_title="Points",
        legend_title="Team",
        # font=dict(
        #     family="Courier New, monospace",
        #     size=18,
        #     color="RebeccaPurple"
        # )
    )

    # data table
    df_table = df[["t_name", "track_car", "points_cum", "e_date"]]
    
    df_table.rename(columns={
        "t_name" : "Team", 
        "track_car" : "Track - Car", 
        "points_cum" : "Points (cumulative)",
        "e_date" : "Date"
        }, 
        inplace=True
    )
    df_table.set_index(["Track - Car", "Date"], inplace =True)
    df_table = df_table.pivot(columns="Team")
    df_table.columns = df_table.columns.droplevel()
    df_table.reset_index(inplace=True)

    teams_order_by_points_last_race = df.loc[df["e_date"]==df["e_date"].max(), :].sort_values("points_cum", ascending=False)["t_name"].to_list()
    print(df_table)
    df_table = df_table.loc[:, ["Track - Car", "Date"]+teams_order_by_points_last_race].sort_values("Date")

    standings_columns = [{"name": i, "id": i} for i in df_table.columns]
    standings_data = df_table.to_dict('records')

    return fig, standings_columns, standings_data



@app.callback(
    dash.dependencies.Output('driver_standings', 'figure'),
    [dash.dependencies.Input('season_cs', 'value'), dash.dependencies.Input('season_league', 'value'), dash.dependencies.Input('season', 'value')],
)
def update_driver_standings_graph(season_cs, season_league, season):
    df = get_driver_standings_cumulative(cs=season_cs, league=season_league, season=season)
    df["track_car"] = df["r_track"]+" - "+df["r_car"]

    df.sort_values("e_date", inplace=True, ascending=True)

    fig = px.line(df, x="track_car", y="points_cum", color="d_name", title='Driver Standings', markers=True)
    fig.layout = transparent_layout

    fig.update_layout(
        #title="Plot Title",
        #xaxis_title="X Axis Title",
        yaxis_title="Points",
        legend_title="Driver",
        # font=dict(
        #     family="Courier New, monospace",
        #     size=18,
        #     color="RebeccaPurple"
        # )
    )

    return fig

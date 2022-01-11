import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd

app = dash.Dash()

server = app.server

df = pd.read_csv(
    "data/lap_table.csv",
    sep=";"
)

df = pd.melt(df, id_vars="Driver", value_vars=df.columns[1:], var_name="Lap", value_name="Pos")

df.dropna(how="any", inplace=True)

fig = px.line(df, x="Lap", y="Pos", color="Driver", title='Track Position')

app.layout = html.Div([dcc.Graph(id="life-exp-vs-gdp", figure=fig)])


if __name__ == "__main__":
    app.run_server(debug=True)
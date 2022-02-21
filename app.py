from main import app, server
from layouts import base
from callbacks import dropdowns as dd, descriptions as desc, standings as stand, results as res, drivers as dri, misc as mi
import dash
from dash import html
import dash_bootstrap_components as dbc


app.layout = base.layout

from layouts import base, standings, results, drivers, misc, dev

@app.callback(
    dash.dependencies.Output("tab-content", "children"),
    dash.dependencies.Input("tabs", "active_tab")
)
def render_tab_content(active_tab):
    if active_tab == "season_standings":
        return standings.layout
    elif active_tab == "race_results":
        return results.layout
    elif active_tab == "drivers":
        #return drivers.layout
        return html.Div([
                dbc.Row([
                    dbc.Col([html.H3("Origin", className="graph_header"), dri.update_drivers_region_graph()]),
                    dbc.Col([html.H3("Device", className="graph_header"), dri.update_drivers_device_graph()])
                    ]
                )
                #,
                # dbc.Row(dcc.Dropdown(
                #     id='region',
                #     options=[
                #         {'label': 'World', 'value': 'world'},
                #         {'label': 'Europe', 'value': 'EU'},
                #         {'label': 'North America', 'value': 'NA'},
                #         {'label': 'South America', 'value': 'SA'}
                #     ],
                #     value='world'
                # )),
                # dbc.Row([
                    
                # ])
            ])
    elif active_tab == "misc":
        return misc.layout
    elif active_tab == "dev":
        return dev.layout
    
    return html.P("No tab selected")

if __name__ == "__main__":
    app.run_server(debug=True)
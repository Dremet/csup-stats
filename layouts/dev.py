from dash import html
import dash_bootstrap_components as dbc


layout = html.Div([
    dbc.Row([
        html.H3("Roadmap", className="table_header"),
        html.P("The items are roughly ordered in terms of their priority from high to low.")
    ]),
    dbc.Row([
        dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    html.P("Change false/true to yes/no in race results table."),
                    dbc.Alert("Low effort", color="success")
                ],
                title="Change false/true to yes/no",
            ),
            dbc.AccordionItem(
                [
                    html.P("As the ELO is now available, it can for example be used to show average ELO rankings in certain leagues. More to come."),
                    dbc.Alert("Medium effort", color="primary")
                ],
                title="ELO Plots",
            ),
            dbc.AccordionItem(
                [
                    html.P("Within the season standings tab, a table will be added for both drivers as well if teams (if there are teams) that shows the number of achievements per driver/team: #Wins, #Poles, #FastestLaps, #TeamWins, #DoubleWins, ..."),
                    dbc.Alert("Medium effort", color="primary")
                ],
                title="Achievements",
            ),
            dbc.AccordionItem(
                [
                    html.P("On the drivers tab, a table showing the amount of overall race participations, won races, poles etc. Obviously, this is limited to the championships that are being considered worth adding to the database."),
                    dbc.Alert("Medium effort", color="primary")
                ],
                title="Driver Statistics",
            ),
            dbc.AccordionItem(
                [
                    html.P("Based on feedback the plots will be improved in terms of their structure/description/colors."),
                    dbc.Alert("Medium effort", color="primary")
                ],
                title="Prettify Graphs",
            ),
            dbc.AccordionItem(
                [
                    html.P("Optimize database queries to lower loading times."),
                    dbc.Alert("Medium effort", color="primary")
                ],
                title="Optimize Performance",
            ),
            dbc.AccordionItem(
                [
                    html.P("For certain races, McVizn puts in the time to create a lap table showing the position of every driver each lap. This can be added to the race results, if available."),
                    dbc.Alert("Medium effort", color="primary")
                ],
                title="Lap Table",
            ),
            dbc.AccordionItem(
                [
                    html.P("Add data from other championships like TDRL or others."),
                    dbc.Alert("High effort", color="warning")
                ],
                title="Add more Championships",
            ),
            dbc.AccordionItem(
                [
                    html.P("This site is currently hosted on a free tier hosting option on heroku. If it is used regularly, I will upgrade it to a non-free option to increase performance."),
                    dbc.Alert("Medium effort", color="primary")
                ],
                title="Evaluate Hosting Options",
            ),
        ],start_collapsed=True
    ), 
    ]),
    dbc.Row([
        dbc.Col(
            dbc.Alert("You have more suggestions? Message me (Dremet#7626) on Discord. You also find me on the official Circuit Superstars or ICSTC discord.", color="warning"),
            style={"margin-top": "15px"}
        )
    ])
])
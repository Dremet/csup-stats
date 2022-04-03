import dash
from dash import html
from main import app

iframe_sources_by_timezone = {
    "utc" : "https://calendar.google.com/calendar/embed?height=600&wkst=2&bgcolor=%23ffffff&ctz=UTC&src=cWhiZXF2czhrcHRlOXJxM2gzYmowdjhmMnNAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ&color=%23D50000",
    "central_eu" : "https://calendar.google.com/calendar/embed?height=600&wkst=2&bgcolor=%23ffffff&ctz=Europe%2FBerlin&src=cWhiZXF2czhrcHRlOXJxM2gzYmowdjhmMnNAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ&color=%23D50000",
    "uk" : "https://calendar.google.com/calendar/embed?height=600&wkst=2&bgcolor=%23ffffff&ctz=Europe%2FLondon&src=cWhiZXF2czhrcHRlOXJxM2gzYmowdjhmMnNAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ&color=%23D50000",
    "us_pacific" : "https://calendar.google.com/calendar/embed?height=600&wkst=2&bgcolor=%23ffffff&ctz=America%2FLos_Angeles&src=cWhiZXF2czhrcHRlOXJxM2gzYmowdjhmMnNAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ&color=%23D50000",
    "us_mountain" : "https://calendar.google.com/calendar/embed?height=600&wkst=2&bgcolor=%23ffffff&ctz=America%2FDenver&src=cWhiZXF2czhrcHRlOXJxM2gzYmowdjhmMnNAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ&color=%23D50000",
    "us_central" : "https://calendar.google.com/calendar/embed?height=600&wkst=2&bgcolor=%23ffffff&ctz=America%2FChicago&src=cWhiZXF2czhrcHRlOXJxM2gzYmowdjhmMnNAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ&color=%23D50000",
    "us_eastern" : "https://calendar.google.com/calendar/embed?height=600&wkst=2&bgcolor=%23ffffff&ctz=America%2FNew_York&src=cWhiZXF2czhrcHRlOXJxM2gzYmowdjhmMnNAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ&color=%23D50000"
}

width = "100%"
height = "700px"


@app.callback(
    dash.dependencies.Output("tz-tab-content", "children"),
    dash.dependencies.Input("tz_tabs", "active_tab")
)
def render_tz_tab_content(active_tab):
    if active_tab in iframe_sources_by_timezone.keys():
        return html.Iframe(
                src=iframe_sources_by_timezone[active_tab],
                width=width, 
                height=height
            )
    else:
        return html.Iframe(
                src=iframe_sources_by_timezone["utc"],
                width=width, 
                height=height
            )
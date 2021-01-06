# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

df_sleep = pd.read_csv("data/sleep.csv")

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

navbar = dbc.NavbarSimple(
    # html.A(
    #     dbc.Row(
    #         [
    #             dbc.Col(dbc.NavbarBrand("health monitor")),
    #             dbc.Col(dbc.NavItem(dbc.NavLink("Stress", href="stress"))),
    #             dbc.Col(dbc.NavItem(dbc.NavLink("Sleep", href="#")))
    #         ]
    #     )
    # ),
    children=[
        dbc.NavItem(dbc.NavLink("Stress", href="stress")),
        dbc.NavItem(dbc.NavLink("Sleep", href="#")),
        dbc.NavItem(dbc.NavLink("Activity", href="activity")),
    ],
    brand="Health monitor",
    color="primary",
    dark=True
)


app.layout = html.Div(children=[
    navbar,


    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    html.Label("Choose person"),
    dcc.RadioItems(
        id='sleep-person-btn-in',
        options=[
            {'label': 'Marysia', 'value': 'Marysia'},
            {'label': 'Marcelina', 'value': 'Marcelina'},
            {'label': 'Michał', 'value': 'Michal'}
        ]
    ),

    html.Label("Show average sleep duration"),
    dcc.RadioItems(
        id="show-average-slp-dur",
        options=[
            {'label': 'show', 'value': 'True'}
        ]
    ),

    html.Br(),

    dcc.Graph(
        id='sleep-chart',
        figure=fig
    ),

    html.Label(id="out")
])


# @app.callback(
#     Output(component_id='sleep-chart', component_property='figure'),
#     Input(component_id='sleep-person-btn-in', component_property='value')
# )
# def update_sleep_chart_person(person):
#     df = df_sleep[df_sleep.user == person]
#     fig = px.bar(x=df.start_time, y=df.sleep_duration)
#     return fig

@app.callback(
    Output(component_id='sleep-chart', component_property='figure'),
    Input(component_id='show-average-slp-dur', component_property='value'),
    Input(component_id='sleep-person-btn-in', component_property='value')
)
def update_sleep_chart_show_average(show, person):
    df = df_sleep[df_sleep.user == person]
    fig = px.bar(df, x='start_time', y='sleep_duration')
    if show == 'True':
        avg_dur = df['sleep_duration'].mean()
        fig.add_hline(y=avg_dur, line_width=3, line_dash="dash", line_color="green", annotation_text="average")
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)

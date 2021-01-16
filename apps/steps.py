import pandas as pd
import plotly.express as px  # (version 4.7.0)

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import datetime as dt
import dash_table_experiments as dte
import dash_table

import plotly.graph_objs as go

from apps.commons import navbar
from app import app

# ----------------------------------------------------------------------------------------------------------------
# import data
steps_marcelina = pd.read_csv("data/steps.csv")
steps_marysia = pd.read_csv("data/steps_marysia.csv")
steps = pd.concat([steps_marcelina, steps_marysia], join="inner", ignore_index=True)

steps_weekly = steps.copy()
date = []
start = dt.datetime(2020, 12, 17).date()  # poniedziałek
end = dt.datetime(2020, 12, 20).date()  # niedziela
prev = dt.datetime(2021, 2, 1).date()
for d in steps_weekly["date"]:
    d = dt.datetime.strptime(d, '%Y-%m-%d').date()
    if d < prev:
        start = dt.datetime(2020, 12, 17).date()  # poniedziałek
        end = dt.datetime(2020, 12, 20).date()  # niedziela
    elif d < start or d > end:
        end += dt.timedelta(7)
        start = end - dt.timedelta(6)
    d = start
    date.append(d.isoformat() + " - " + end.isoformat())
    prev = d
steps_weekly["date"] = date
steps_weekly = steps_weekly.groupby(['date', 'user'], as_index=False).mean()
steps_summary_mean = steps.groupby(['user'], as_index=False).mean().round(2)
steps_summary_max = steps.groupby(['user'], as_index=False).max().round(2)
steps_summary_mean = steps_summary_mean.rename(
    columns={'step_count': 'average step count', 'distance': 'average distance'})
steps_summary_max = steps_summary_max.rename(columns={'step_count': 'max step count', 'distance': 'max distance'})
steps_table = pd.merge(steps_summary_mean, steps_summary_max)
# -----------------------------------------------------------------------------------------------------------------
layout = html.Div([
    navbar,

    dbc.Container([
        dbc.Container([
            dbc.Row([
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader("Average distance"),
                        dbc.CardBody([html.H3(
                            str(steps_summary_mean.iloc[i, 0]) + ": " + str(steps_summary_mean.iloc[i, 2]) + " m\n")
                                      for i in range(len(steps_summary_mean))])
                    ],
                        inverse=True,
                        className="info-card",
                        )
                , width=5),
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader("Maximum distance"),
                        dbc.CardBody([html.H3(
                            str(steps_summary_max.iloc[i, 0]) + ": " + str(steps_summary_max.iloc[i, 3]) + " m\n")
                                      for i in range(len(steps_summary_max))])
                    ],
                        inverse=True,
                        className="info-card")
                , width=5),
            ], style={"margin-top": "40px", "margin-bottom": "40px", "justify-content": "center"})
        ]),

        dbc.Row([
            dbc.Col([
            html.Label('Choose type', style={'font-weight': 'bold'}),
            dcc.RadioItems(
                id="slct_type",
                options=[
                    {'label': '  steps', 'value': 'step_count'},
                    {'label': '  distance', 'value': 'distance'}
                ],
                value='step_count',
                className="radio-items"
            )], width= 3),
            dbc.Col([
            html.Label('Select period', style={'font-weight': 'bold'}),
            dcc.Dropdown(id="slct_period",
                         options=[
                             {"label": "daily", "value": "daily"},
                             {"label": "weekly", "value": "weekly"}],
                         multi=False,
                         value="daily",
                         style={'width': "100%", "color": "black", "text-color": "black"}
                         ),

            dcc.Checklist(id="top3",
                          # options=[
                          #     {'label': '   Show top 3', 'value': 'top'}
                          # ],
                          ),
            ], width= 3),

        ], style={"margin-top": "40px"}),
        dbc.Row(
            dcc.Graph(
                id='barplot',
                style={'width': "100%"}
            ),  style={'margin': '0'})
    ])
])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    Output(component_id='barplot', component_property='figure'),
    [Input(component_id='slct_type', component_property='value'),
     Input(component_id='slct_period', component_property='value'),
     Input(component_id='top3', component_property='value')]
)
def update_graph(option_slctd, period_slctd, top):
    colors_1 = ['#52057b', '#892cdc', '#bc6ff1']

    df = steps.copy()
    if period_slctd == "daily":
        fig = px.bar(df, x="date", y=option_slctd, color="user", barmode="group", labels={'step_count': 'step count'},
                     title="Step count" if str(option_slctd) == "step_count" else "Distance",
                     color_discrete_sequence=colors_1)
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(size=14, color="white"))
        fig.layout.font.family = 'Rubik'
    elif period_slctd == "weekly":
        fig = px.bar(steps_weekly, x="date", y=option_slctd, color="user", barmode="group",
                     labels={'step_count': 'Step count'},
                     title="Step count" if str(option_slctd) == "step_count" else "Distance",
                     color_discrete_sequence=colors_1)

        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(size=14, color="white"))
        fig.layout.font.family = 'Rubik'
    if top == ['top'] and period_slctd == "daily":
        color = []
        for i in range(len(steps)):
            if steps.iloc[i, 2] in list(steps_marcelina.nlargest(3, 'distance').iloc[:, 2]) and steps.iloc[
                i, 3] == "Marcelina":
                color.append("max_1")
            elif steps.iloc[i, 2] in list(steps_marysia.nlargest(3, 'distance').iloc[:, 3]) and steps.iloc[
                i, 3] == "Marysia":
                color.append("max_2")
            elif steps.iloc[i, 3] == "Marcelina":
                color.append("normal_1")
            else:
                color.append("normal_2")

        color = pd.DataFrame(color)
        dff = steps.copy()
        dff['color'] = color

        fig3 = go.Figure(
            data=[
                go.Bar(
                    name="Marcelina",
                    x=dff["date"].loc[dff['color'] == 'normal_1'],
                    y=dff[str(option_slctd)].loc[dff['color'] == 'normal_1'],
                    offsetgroup=0,
                    marker=dict(color=colors_1[0])
                ),
                go.Bar(
                    name="Marysia",
                    x=dff["date"].loc[dff['color'] == 'normal_2'],
                    y=dff[str(option_slctd)].loc[dff['color'] == 'normal_2'],
                    offsetgroup=1,
                    marker=dict(color=colors_1[2])
                ),
                go.Bar(
                    name="Top 3 - Marcelina",
                    x=dff["date"].loc[dff['color'] == 'max_1'],
                    y=dff[str(option_slctd)].loc[dff['color'] == 'max_1'],
                    offsetgroup=0,
                    base=dff["date"].loc[dff['color'] == 'max_1'],
                    marker=dict(color="#EF233C")
                ),
                go.Bar(
                    name="Top 3 - Marysia",
                    x=dff["date"].loc[dff['color'] == 'max_2'],
                    y=dff[str(option_slctd)].loc[dff['color'] == 'max_2'],
                    offsetgroup=1,
                    marker=dict(color="#d80032")
                ),
            ],
            layout=go.Layout(
                yaxis_title="date",
                xaxis_title="Step count" if str(option_slctd) == "step_count" else "Distance",
                title="Step count" if str(option_slctd) == "step_count" else "Distance",
                font = dict(size=14, color="white"),
            )
        )
        fig = fig3
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(size=14))
        fig.layout.font.family = 'Rubik'
        # fig = px.bar(dff, x="date", y=option_slctd, color="color", barmode="group").update_layout(bargap=0.15)

    return fig

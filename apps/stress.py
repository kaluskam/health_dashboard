import dash_html_components as html
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import plotly.graph_objs as go
import plotly.express as px
import plotly.figure_factory as ff

from apps.commons import navbar

external_stylesheets = [
    'assets/style.css'
]

df = pd.read_csv('data/stress_data.csv', sep=';')
df2 = pd.read_csv('data/heartrate_oxygen_data.csv', sep=';')

df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
df2['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

avg_stress_score = df['score'].mean()
avg_heart_rate = df2['heart_rate'].mean()
avg_saturation = df2['oxygen_saturation'].mean()


stress_fig = px.line(df, x="date", y="score",
                     title="Stress score over time",
                     labels={
                         "date": "Date", "score": "Stress score"
                     },
                     template="plotly_dark")
stress_fig.update_traces(line_color="#892cdc", line_width=3, line_shape='spline')
stress_fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(size=14))
stress_fig.layout.font.family = 'Rubik'

hr_fig = px.line(df2, x="date", y="heart_rate",
                 title="Heart rate over time",
                 labels={
                     "date": "Date", "heart_rate": "Heart rate"
                 },
                 template="plotly_dark")
hr_fig.update_traces(line_color="#892cdc", line_width=3, line_shape='spline')
hr_fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(size=14))
hr_fig.layout.font.family = 'Rubik'

oxy_fig = px.line(df2, x="date", y="oxygen_saturation",
                  title="Heart rate over time",
                  labels={
                      "date": "Date", "oxygen_saturation": "Oxygen saturation"
                  },
                  template="plotly_dark")
oxy_fig.update_traces(line_color="#892cdc", line_width=3, line_shape='spline')
oxy_fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(size=14))
oxy_fig.layout.font.family = 'Rubik'


hr_dist_fig = ff.create_distplot([df2['heart_rate']], ['distplot'], show_hist=False, show_rug=False)

layout = html.Div([
    navbar,

    dbc.Container([
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Avg. heart rate"),
                    dbc.CardBody([html.H1(str(int(avg_heart_rate)) + " BPM"),
                                  html.P("hr w normie")])
                ],
                    inverse=True,
                    className="info-card")
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Avg. blood oxygen saturation"),
                    dbc.CardBody(html.H1(str(int(avg_saturation)) + "%"))
                ],
                    inverse=True,
                    className="info-card")
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Avg. stress score"),
                    dbc.CardBody(html.H1(str(int(avg_stress_score))))
                ],
                    inverse=True,
                    className="info-card")
            )
        ], style={"margin-top": "20px"}),


        dbc.Row([
            dbc.Col(dcc.Graph(figure=stress_fig))
        ], style={"margin-top": "20px"}, className='s-row'),

        dbc.Row([

            dbc.Col(dcc.Graph(figure=hr_fig))
        ], style={"margin-top": "20px"}, className='s-row'),

        dbc.Row([
            
            dbc.Col(dcc.Graph(figure=oxy_fig))
        ], style={"margin-top": "20px"}, className='s-row'),

        dbc.Row(
            dcc.Graph(figure=hr_dist_fig)
        )
])])

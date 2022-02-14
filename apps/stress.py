from dash import html
import pandas as pd
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Output, Input

from apps.commons import navbar
from app import app

external_stylesheets = [
    'assets/style.css'
]

df3 = pd.read_csv('data/stressdata.csv', sep=';')

df3['date'] = pd.to_datetime(df3['date'], format='%d.%m.%Y')
outdf = df3[df3.user == "Marysia"]

avg_stress_score = outdf['stress_score'].mean()
avg_heart_rate = outdf['heart_rate'].mean()
avg_saturation = outdf['oxygen_saturation'].mean()

stress_fig = px.line(outdf, x="date", y="stress_score",
                     title="Stress score over time",
                     labels={
                         "date": "Date", "score": "Stress score"
                     },
                     template="plotly_dark")
stress_fig.update_traces(line_color="#892cdc", line_width=3, line_shape='spline')
stress_fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(size=14))
stress_fig.layout.font.family = 'Rubik'

hr_fig = px.line(outdf, x="date", y="heart_rate",
                 title="Heart rate over time",
                 labels={
                     "date": "Date", "heart_rate": "Heart rate"
                 },
                 template="plotly_dark")
hr_fig.update_traces(line_color="#892cdc", line_width=3, line_shape='spline')
hr_fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(size=14))
hr_fig.layout.font.family = 'Rubik'

oxy_fig = px.line(outdf, x="date", y="oxygen_saturation",
                  title="Blood oxygen saturation over time",
                  labels={
                      "date": "Date", "oxygen_saturation": "Oxygen saturation"
                  },
                  template="plotly_dark")
oxy_fig.update_traces(line_color="#892cdc", line_width=3, line_shape='spline')
oxy_fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(size=14))
oxy_fig.layout.font.family = 'Rubik'

#hr_dist_fig = ff.create_distplot([outdf['heart_rate']], ['distplot'], show_hist=False, show_rug=False)

layout = html.Div([
    navbar,

    dbc.Container([
        html.Label(
            className='label',
            children=["Choose user"]),
        dcc.RadioItems(
            id='stress-person-btn-in',
            options=[
                {'label': ' Marysia', 'value': 'Marysia'},
                {'label': ' Marcelina', 'value': 'Marcelina'},
                {'label': ' Michał', 'value': 'Michal'}
            ],
            value='Marysia',
            className='radio-items'
        ),

        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Avg. heart rate"),
                    dbc.CardBody(html.H1(str(int(avg_heart_rate)) + " BPM"), id="hr-card")
                ],
                    inverse=True,
                    className="info-card")
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Avg. blood oxygen saturation"),
                    dbc.CardBody(html.H1(str(int(avg_saturation)) + "%"), id="oxy-card")
                ],
                    inverse=True,
                    className="info-card")
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Avg. stress score"),
                    dbc.CardBody(html.H1(str(int(avg_stress_score))), id="stress-card")
                ],
                    inverse=True,
                    className="info-card")
            )
        ], style={"margin-top": "30px"}),

        dbc.Row([
            dbc.Col(dcc.Graph(figure=hr_fig, id="hr-chart")),], style={"margin-top": "30px"}),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=oxy_fig, id="oxy-chart")),
        ], style={"margin-top": "30px"}),
        dbc.Row([dbc.Col(dcc.Graph(figure=stress_fig, id="stress-chart")),], style={"margin-top": "30px"}),
    ])])


@app.callback(
    Output(component_id='hr-chart', component_property='figure'),
    Output(component_id='stress-chart', component_property='figure'),
    Output(component_id='oxy-chart', component_property='figure'),
    Input(component_id='stress-person-btn-in', component_property='value'),
)
def update_chart(user):
    tmp = df3[df3.user == user]

    avg_stress_score = tmp['stress_score'].mean()
    avg_heart_rate = tmp['heart_rate'].mean()
    avg_saturation = tmp['oxygen_saturation'].mean()

    stress_fig = px.line(tmp, x="date", y="stress_score",
                         title="Stress score over time",
                         labels={
                             "date": "Date", "stress_score": "Stress score"
                         },
                         template="plotly_dark")

    stress_fig.update_traces(line_color="#892cdc", line_width=3, line_shape='spline')
    stress_fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(size=14))
    stress_fig.layout.font.family = 'Rubik'

    hr_fig = px.line(tmp, x="date", y="heart_rate",
                     title="Heart rate over time",
                     labels={
                         "date": "Date", "heart_rate": "Heart rate"
                     },
                     template="plotly_dark")
    hr_fig.update_traces(line_color="#892cdc", line_width=3, line_shape='spline')
    hr_fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(size=14))
    hr_fig.layout.font.family = 'Rubik'

    oxy_fig = px.line(tmp, x="date", y="oxygen_saturation",
                      title="Blood oxygen saturation over time",
                      labels={
                          "date": "Date", "oxygen_saturation": "Oxygen saturation"
                      },
                      template="plotly_dark")
    oxy_fig.update_traces(line_color="#892cdc", line_width=3, line_shape='spline')
    oxy_fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(size=14))
    oxy_fig.layout.font.family = 'Rubik'

    return hr_fig, stress_fig, oxy_fig


@app.callback(
    Output(component_id='hr-card', component_property='children'),
    Output(component_id='stress-card', component_property='children'),
    Output(component_id='oxy-card', component_property='children'),
    Input(component_id='stress-person-btn-in', component_property='value'),
)
def update_card(user):
    tmp = df3[df3.user == user]

    avg_stress = tmp['stress_score'].mean()
    avg_hr = tmp['heart_rate'].mean()
    avg_oxy = tmp["oxygen_saturation"].mean()

    return html.H1(str(int(avg_hr)) + " BPM"), html.H1(str(int(avg_stress))), html.H1(str(int(avg_oxy)) + "%")
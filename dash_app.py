import pandas as pd
import plotly.express as px  # (version 4.7.0)

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import datetime as dt
import dash_table_experiments as dte
import dash_table

import plotly.graph_objs as go

app = dash.Dash(__name__)

# ----------------------------------------------------------------------------------------------------------------
# import data
steps_marcelina = pd.read_csv("steps.csv")
steps_marysia = pd.read_csv("steps_marysia.csv")
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
steps_summary_mean = steps.groupby(['user'], as_index=False).mean()
steps_summary_max = steps.groupby(['user'], as_index=False).max()
steps_summary_mean = steps_summary_mean.rename(columns= {'step_count': 'average step count', 'distance': 'average distance'})
steps_summary_max = steps_summary_max.rename(columns= {'step_count': 'max step count', 'distance': 'max distance'})
steps_table = pd.merge(steps_summary_mean, steps_summary_max)
# -----------------------------------------------------------------------------------------------------------------
app.layout = html.Div([

    html.H1("Steps and distance", style={'text-align': 'center'}),

    html.Label('Choose one'),
    dcc.RadioItems(
        id="slct_type",
        options=[
            {'label': 'steps', 'value': 'step_count'},
            {'label': 'distance', 'value': 'distance'}
        ],
        value='step_count',

    ),

    dcc.Dropdown(id="slct_period",
                 options=[
                     {"label": "daily", "value": "daily"},
                     {"label": "weekly", "value": "weekly"},
                     {"label": "monthly", "value": "monthly"}],
                 multi=False,
                 value="daily",
                 style={'width': "40%"}
                 ),

    dcc.Checklist(id="top3",
                  options=[
                      {'label': 'Show top 3', 'value': 'top'}
                  ],
                  ),

    dcc.Graph(
        id='barplot',
        style={'width': "75%"}
    ),
    dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i}
                    for i in steps_table.columns],
            data=steps_table.to_dict('records'),
            style_cell=dict(textAlign='left'),
            style_header=dict(backgroundColor="paleturquoise"),
            style_data=dict(backgroundColor="lavender")
    )

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
    print(option_slctd)
    print(period_slctd)
    print(top)

    df = steps.copy()
    if period_slctd == "daily":
        fig = px.bar(df, x="date", y=option_slctd, color="user", barmode="group")
    elif period_slctd == "weekly":
        fig = px.bar(steps_weekly, x="date", y=option_slctd, color="user", barmode="group")
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
        fig = px.bar(dff, x="date", y=option_slctd, color="color", barmode="group").update_layout(bargap=0.15)

    return fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)

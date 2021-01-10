import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plot_generator
from dash.dependencies import Input, Output
from apps.commons import navbar

from app import app

external_stylesheets = ['assets/app.css']

df_sleep = pd.read_csv("data/sleep.csv")
df_sleep_summary = pd.read_csv("data/sleep_summary.csv")
df_sleep_regularity = pd.read_csv("data/sleep_regularity.csv")

dates = df_sleep['start_date'].unique()
dates.sort()
date_marks = {i: dates[i] for i in range(0, len(dates))}

fig = plot_generator.sleep_bar_plot_for_person(df_sleep, 'Marysia', date_marks[0], date_marks[len(dates) - 1])
clocks = plot_generator.sleep_clock_dict(df_sleep_summary)
sleep_reg_fig = plot_generator.sleep_regularity_scatter_plot(df_sleep_regularity, 'general')

sleep_clocks = html.Div(
    id='sleep-clocks',
    children=[
        html.Label(
            className='label',
            children=["Check who"]),
        dcc.RadioItems(
            id='sleep-person-comparison',
            options=[
                {'label': ' gets up the earliest', 'value': 'early'},
                {'label': ' goes to sleep late', 'value': 'late'},
                {'label': ' sleeps the longest', 'value': 'long'}
            ],
            className='radio-items'
        ),

        html.Span(id='marysia-span',
                  children=[
                      html.H3(id='marysia-h3',
                              children=['Marysia']),
                      dcc.Graph(
                          id='marysia-clock',
                          figure=clocks['Marysia'],
                          className='clock-graph'),
                  ],
                  style={'display': 'inline-block', 'margin': '5vh'}),
        html.Span(id='marcelina-span',
                  children=[
                      html.H3(id='marcelina-h3',
                              children=['Marcelina']),
                      dcc.Graph(
                          id='marcelina-clock',
                          figure=clocks['Marcelina'],
                          className='clock-graph'),
                  ],
                  style={'display': 'inline-block', 'margin': '5vh'}),
        html.Span(id='michal-span',
                  children=[
                      html.H3(id='michal-h3',
                              children=['Michal']),
                      dcc.Graph(
                          id='michal-clock',
                          figure=clocks['Michal'],
                          className='clock-graph')
                  ],
                  style={'display': 'inline-block', 'margin': '5vh'})

    ])

sleep_regularity_section = html.Div(
    children=[
        html.Label(
            className='label',
            children=["Select time period"]),
        dcc.RadioItems(
            id='sleep-reg-period',
            options=[
                {'label': ' winter break', 'value': 'holidays'},
                {'label': ' studying time', 'value': 'studying'},
                {'label': ' all', 'value': 'general'}
            ],
            value='general',
            className='radio-items'
        ),
        dcc.Graph(
            id='sleep-regularity-plot',
            figure=sleep_reg_fig
        )
    ]
)

layout = html.Div(
    className='page',
    children=[
        navbar,
        html.H1('SLEEP'),

        html.Label(
            className='label',
            children=["Choose person"]),
        dcc.RadioItems(
            id='sleep-person-btn-in',
            options=[
                {'label': ' Marysia', 'value': 'Marysia'},
                {'label': ' Marcelina', 'value': 'Marcelina'},
                {'label': ' Michał', 'value': 'Michal'}
            ],
            value='Marysia',
            className='radio-items'
        ),

        html.Label(
            className='label',
            children=["Time interval"]),
        dcc.RangeSlider(
            id='sleep-date-slider',
            marks=date_marks,
            min=0,
            max=len(dates) - 1,
            value=[0, len(dates) - 1]
        ),

        html.Label(
            className='label',
            children=["Show average sleep duration"]),
        dcc.Checklist(
            id="sleep-show-avg",
            className='check-list',
            options=[
                {'label': ' show', 'value': 'True'}
            ],
        ),

        html.Br(),

        dcc.Graph(
            id='sleep-chart',
            figure=fig
        ),

        sleep_clocks,

        sleep_regularity_section
    ])


@app.callback(
    Output(component_id='sleep-chart', component_property='figure'),
    Input(component_id='sleep-show-avg', component_property='value'),
    Input(component_id='sleep-person-btn-in', component_property='value'),
    Input(component_id='sleep-date-slider', component_property='value')
)
def update_sleep_bar_chart(show, person, time_interval):
    df = df_sleep[df_sleep.user == person]
    fig = plot_generator.sleep_bar_plot_for_person(df_sleep, person, date_marks[time_interval[0]],
                                                   date_marks[time_interval[1]])
    if show and show[0] == 'True':
        avg_dur = df['sleep_duration'].mean()
        fig.add_hline(y=avg_dur, line_width=5, line_dash="dash", line_color="green", annotation_text="average")
    return fig


@app.callback(
    Output(component_id='marysia-h3', component_property='children'),
    Output(component_id='marcelina-h3', component_property='children'),
    Output(component_id='michal-h3', component_property='children'),
    Input(component_id='sleep-person-comparison', component_property='value')
)
def compare_person_sleep_clocks(option):
    user = ''
    if option == 'early':
        user = df_sleep_summary.loc[df_sleep_summary.mean_start_time_rank == 0, 'user'].values[0]
    elif option == 'late':
        user = df_sleep_summary.loc[df_sleep_summary.mean_end_time_rank == 2, 'user'].values[0]
    elif option == 'long':
        user = df_sleep_summary.loc[df_sleep_summary['sleep_duration'].argmax(), 'user']
        print(user)
    h_1 = 'Marysia'
    h_2 = 'Marcelina'
    h_3 = 'Michal'
    if user == 'Marysia':
        h_1 = html.H3(
            children=['Marysia'],
            className='name-label'
        )
    elif user == 'Marcelina':
        h_2 = html.H3(
            children=['Marcelina'],
            className='name-label'
        )
    elif user == 'Michal':
        h_3 = html.H3(
            children=['Michal'],
            className='name-label'
        )

    return h_1, h_2, h_3


@app.callback(
    Output(component_id='sleep-regularity-plot', component_property='figure'),
    Input(component_id='sleep-reg-period', component_property='value')
)
def show_reg_for_selected_period(period):
    return plot_generator.sleep_regularity_scatter_plot(df_sleep_regularity, period)


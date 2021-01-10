import plotly.express as px
import plotly.graph_objects as go
from data import func_utils

colors_1 = ['#004fa3', '#007bff', '#3da5d9']
clock_colors = ['#004fa3', '#3da5d9']


def sleep_bar_plot_for_person(df, person, start, end):
    df['quality'] = df['quality'].astype('str')
    df = df[(df.start_date > start) & (df.start_date < end)]

    fig = px.bar(df[df.user == person], x='start_time', y='sleep_duration',
                 labels={
                     'start_time': '',
                     'sleep_duration': 'Sleep duration'
                 },
                 color_discrete_sequence=colors_1,
                 color='quality'
                 )
    fig.update_layout(
        hoverlabel=dict(
            font_size=16
        )
    )
    fig.update_traces(hovertemplate="Bed time: %{x}<br>Sleep duration: %{y}<br>")
    return fig


def sleep_clock_dict(df):
    layout = go.Layout(
        margin=go.layout.Margin(
            l=0,  # left margin
            r=0,  # right margin
            b=0,  # bottom margin
            t=0  # top margin
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=16),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    clocks = dict()
    for id, row in df.iterrows():
        angle, duration, rest = func_utils.time_angles(row['mean_start_time'], row['mean_end_time'])
        clock_fig = go.Figure(data=[go.Pie(values=[duration, rest], labels=['Asleep', 'Awake'], textinfo="none",
                                           direction='clockwise', rotation=angle, showlegend=False,
                                           hovertemplate="<b>%{label}</b><br>Bed time: " + row['mean_start_time']
                                                         + "<br>Wake up time: " + row['mean_end_time']
                                                         + "<br>Average sleep duration: " + str(
                                               round(row['sleep_duration'],
                                                     2)) + 'h')])
        clock_fig.update_layout(layout)
        clock_fig.update_traces(marker=dict(colors=clock_colors), hoverinfo='skip')
        clock_fig.add_hline(y=1, annotation_text='6:00', annotation_font_color='black', line_color='black')
        clock_fig.add_hline(y=1, annotation_text='12:00', annotation_font_color='black', line_color='black',
                            annotation_position='top left')
        clock_fig.add_vline(x=1, annotation_text='24:00', annotation_font_color='black', line_color='black')
        clock_fig.add_vline(x=1, annotation_text='18:00', annotation_font_color='black',
                            annotation_position='bottom right', line_color='black')
        clock_fig.update_xaxes(side='top', type='category')
        clock_fig.update_yaxes(side='right', type='category')
        clocks[row['user']] = clock_fig
    return clocks


def sleep_regularity_scatter_plot(df, period):
    df = df[df['period'] == period]
    fig = px.scatter(df, x='user', y='std_min', size=[3, 3, 3],
                     labels={
                         'std_min': 'Standard deviation [min]',
                         'user': ''
                     })

    fig.update_traces(marker=dict(color=['#007bff', '#007bff', '#007bff']), hoverinfo='skip',
                      hovertemplate="%{x}<br>Standard deviation: %{y}min")
    return fig

import pandas as pd
from cmath import rect, phase
from math import radians, degrees
from functools import cmp_to_key

HOLIDAYS = [pd.to_datetime('2020-12-24'), pd.to_datetime('2021-01-06')]


def mean_angle(deg):
    if len(deg) == 0:
        return 0
    return degrees(phase(sum(rect(1, radians(d)) for d in deg) / len(deg)))


def mean_time(times):
    t = (time.split(':') for time in times)
    seconds = ((int(m) * 60 + int(h) * 3600)
               for h, m in t)
    day = 24 * 60 * 60
    to_angles = [s * 360. / day for s in seconds]
    mean_as_angle = mean_angle(to_angles)
    mean_seconds = mean_as_angle * day / 360.
    if mean_seconds < 0:
        mean_seconds += day
    h, m = divmod(mean_seconds, 3600)
    m, s = divmod(m, 60)
    return '%02i:%02i' % (h, m)


def time_to_seconds(start, end):
    t_s = start.split(':')
    t_e = end.split(':')
    if int(t_s[0]) < 12:
        seconds_start = int(t_s[0]) * 3600 + int(t_s[1]) * 60
    else:
        seconds_start = int(24 - int(t_s[0])) * 3600 + int(t_s[1]) * 60
    seconds_end = int(t_e[0]) * 3600 + int(t_e[1]) * 60
    return seconds_start, seconds_end


def time_angles(start, end):
    t_s = start.split(':')
    t_e = end.split(':')

    total_num_of_sec = 24 * 3600
    end_sec = int(t_e[0]) * 3600 + int(t_e[1]) * 60

    end_angle = end_sec / total_num_of_sec * 360
    if int(t_s[0]) < 12:
        start_sec = int(t_s[0]) * 3600 + int(t_s[1]) * 60
        duration = end_sec - start_sec
    else:
        if int(t_s[1]) == 0:
            start_sec = int(24 - int(t_s[0])) * 3600 + int(t_s[1]) * 60
        else:
            start_sec = int(24 - int(t_s[0]) - 1) * 3600 + (60 - int(t_s[1])) * 60
        duration = end_sec + start_sec
    return end_angle, duration, total_num_of_sec - duration


def extract_hour_and_minute(row, name):
    return row[name][11:16]


def compare_times(time1, time2):
    h, m = time1.split(':')
    h_2, m_2 = time2.split(':')

    h = int(h)
    m = int(m)
    h_2 = int(h_2)
    m_2 = int(m_2)

    if h < 12 and h_2 > 12:
        return 1
    if h > 12 and h_2 < 12:
        return -1
    if h == h_2:
        if m == m_2:
            return 0
        if m < m_2:
            return -1
        return 1
    if h < h_2:
        return -1
    return 1


def create_sleep_summary():
    df_sleep = pd.read_csv("sleep.csv")
    df_sleep_summary = pd.DataFrame({'user': ['Marysia', 'Marcelina', 'Michal'],
                                     'mean_start_time': [
                                         mean_time(df_sleep[df_sleep['user'] == 'Marysia']['start_time_hour']),
                                         mean_time(df_sleep[df_sleep['user'] == 'Marcelina']['start_time_hour']),
                                         mean_time(df_sleep[df_sleep['user'] == 'Michal']['start_time_hour'])],
                                     'mean_end_time': [
                                         mean_time(df_sleep[df_sleep['user'] == 'Marysia']['end_time_hour']),
                                         mean_time(df_sleep[df_sleep['user'] == 'Marcelina']['end_time_hour']),
                                         mean_time(df_sleep[df_sleep['user'] == 'Michal']['end_time_hour'])
                                     ]})

    start_times = list(df_sleep_summary['mean_start_time'])
    start_times.sort(key=cmp_to_key(compare_times))
    start_hour_order = dict()
    for i in range(0, len(start_times)):
        start_hour_order[start_times[i]] = i
    df_sleep_summary['mean_start_time_rank'] = df_sleep_summary['mean_start_time'].map(start_hour_order)

    end_times = list(df_sleep_summary['mean_end_time'])
    end_times.sort(key=cmp_to_key(compare_times))
    end_hour_order = dict()
    for i in range(0, len(end_times)):
        end_hour_order[end_times[i]] = i
    df_sleep_summary['mean_end_time_rank'] = df_sleep_summary['mean_end_time'].map(end_hour_order)

    sleep_avg = df_sleep.groupby('user')['sleep_duration'].mean()
    df_sleep_summary = pd.merge(df_sleep_summary, sleep_avg, on='user')
    df_sleep_summary.to_csv('sleep_summary.csv', index=False)


def create_sleep_regularity_data():
    df_sleep = pd.read_csv("sleep.csv")
    df_sleep['start_time'] = pd.to_datetime(df_sleep['start_time'])

    df_1 = df_sleep[(df_sleep['start_time'] >= HOLIDAYS[0]) & (df_sleep['start_time'] <= HOLIDAYS[1])] \
             .groupby('user')['sleep_duration'].std().to_frame()
    df_1 = df_1.rename(columns={'sleep_duration': 'std'})
    df_1 = pd.merge(pd.DataFrame({'user': ['Marysia', 'Michal', 'Marcelina']}), df_1, on='user')
    df_1['period'] = ['holidays', 'holidays', 'holidays']

    df_2 = df_sleep.groupby('user')['sleep_duration'].std().to_frame()
    df_2 = df_2.rename(columns={'sleep_duration': 'std'})
    df_2 = pd.merge(pd.DataFrame({'user': ['Marysia', 'Michal', 'Marcelina']}), df_2, on='user')
    df_2['period'] = ['general', 'general', 'general']

    df_3 = df_sleep[(df_sleep['start_time'] < HOLIDAYS[0]) | (df_sleep['start_time'] > HOLIDAYS[1])] \
        .groupby('user')['sleep_duration'].std().to_frame()
    df_3 = df_3.rename(columns={'sleep_duration': 'std'})
    df_3 = pd.merge(pd.DataFrame({'user': ['Marysia', 'Michal', 'Marcelina']}), df_3, on='user')
    df_3['period'] = ['studying', 'studying', 'studying']

    df_sleep_regularity = pd.concat([df_1, df_2, df_3])
    df_sleep_regularity['std_min'] = df_sleep_regularity['std'].apply(lambda x: round(x * 60, 0))
    df_sleep_regularity['std'] = df_sleep_regularity['std'].apply(lambda x: round(x, 2))
    df_sleep_regularity.to_csv('sleep_regularity.csv', index=False)


# if __name__ == '__main__':
#     # create_sleep_summary()
#     # create_sleep_regularity_data()

import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime as dt

from pandas import Series

from extras.db_manager import decorator


@decorator
def get_requests_info():
    return """
    SELECT *, end_time-start_time as duration FROM request 
    WHERE path NOT LIKE '%json%' AND path NOT LIKE '%docs%'
    """


def import_data():
    columns = ['id', 'path', 'verb', 'status_code', 'start_time', 'end_time', 'duration']
    return pd.DataFrame(get_requests_info(fetchall=True), columns=columns)


def format_dates(fields, df):
    for field in fields:
        df[field] = df[field].apply(dt.fromtimestamp)
    return df


def format_primitives(fields, df, type):
    for field in fields:
        df[field] = df[field].astype(type)
    return df


def response_time_boxplot(df):
    df.duration.plot(kind='box')
    plt.ylabel('Time (s)')
    plt.show()


def server_usage_bargraph(df):
    request_dt = df.start_time
    request_dt.groupby([request_dt.dt.year, request_dt.dt.month, request_dt.dt.day]) \
        .count() \
        .plot(kind='bar')

    plt.gcf().autofmt_xdate()
    plt.xlabel('Date (yyyy, mm, dd)')
    plt.ylabel('Number of requests')
    plt.show()


def status_codes_frequencies(df):
    request_dt = df.status_code
    request_dt.index = df.start_time
    codes = request_dt.unique()

    for code in codes:
        temp = request_dt[request_dt == code]
        temp.name = code
        data = temp.groupby([temp.index.year, temp.index.month, temp.index.day]).count()
        data.plot()
        Series.plot(data=data, kind='scatter')

    plt.gcf().autofmt_xdate()
    plt.xlabel('Date (yyyy, mm, dd)')
    plt.ylabel('Number of requests')
    plt.legend()
    plt.show()


def analyze_data(df):
    response_time_boxplot(df)
    server_usage_bargraph(df)
    status_codes_frequencies(df)


df = import_data()
format_dates(['start_time', 'end_time'], df)
format_primitives(['status_code'], df, 'int')
format_primitives(['duration'], df, 'float')
analyze_data(df)

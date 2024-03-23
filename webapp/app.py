import streamlit as st
import pandas as pd
from datetime import datetime
import time
import requests

from src import resources
from postgres import TasksDbController, IntervalsDbController, WeekdaysDbController
from _pages import record


def create_msg(interval_df, weekday_df):
    send_messages = ['[開発中]']
    dt_now = datetime.now()
    success = False

    try:
        for _, row in interval_df.iterrows():
            if row['interval'] == 1:
                send_messages.append(f'実行タスク: {row["name"]} 毎日行うタスクです')
            else:
                pass

        for _, row in weekday_df.iterrows():
            if resources.weekday_dict[row['day_of_week']] == dt_now.weekday():
                send_messages.append(f'実行タスク: {row["name"]} 今日は{row["day_of_week"]}曜日です')
        success = True
    except:
        success = False
        
    return success, send_messages

def merge_dataframes(tasks, intervals, weekdays):
    merged_df = pd.merge(tasks, intervals, on='task_id', how='left')
    merged_df = pd.merge(merged_df, weekdays, on='task_id', how='left')

    return merged_df

def send_message(message:str):
    headers = {'Authorization': f'Bearer {resources.LINE_TOKEN}'}
    data = {'message': f'{message}'}
    r = requests.post(resources.LINE_API, headers=headers, data=data)

    return r


# Call db controller
tasks_db_controller = TasksDbController()
intervals_db_controller = IntervalsDbController()
weekdays_db_controller = WeekdaysDbController()

# UI
st.set_page_config(page_title='Top page')
st.markdown('# タスク通知アプリ')
st.markdown('- タスク一覧')

tasks = tasks_db_controller.read()
intervals = intervals_db_controller.read()
weekdays = weekdays_db_controller.read()

st.write(tasks)

interval_df = pd.merge(tasks, intervals, on='task_id', how='inner')
weekday_df =  pd.merge(tasks, weekdays, on='task_id', how='inner')

msgs = []
if st.button('今日のタスクを取得します'):
    success, msgs = create_msg(interval_df, weekday_df)

    try:
        if success:
            st.success('本日のタスクの取得に成功しました')
            st.info('5秒後にLINE通知を開始します')
            is_cancel = st.button('LINE通知を中止する')
            time.sleep(5)

            if not is_cancel:
                for msg in msgs:
                    send_message(msg)
                    st.success(f'通知が完了しました: {msg}')
                    time.sleep(1)
            else:
                st.warning('LINE通知を中止しました')
        else:
            st.warning('本日のタスクの取得に失敗しました')
    except Exception as e:
        st.error(f'エラーが発生しました: {e}')

record.record()
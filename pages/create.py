import psycopg2
import streamlit as st
import pandas as pd
from postgres import TasksDbController, IntervalsDbController, WeekdaysDbController
from src import resources

tasks_db_controller = TasksDbController()
intervals_db_controller = IntervalsDbController()
weekdays_db_controller = WeekdaysDbController()
current_task_id = None

st.markdown('## タスク作成')

have_interval = st.checkbox('n日おきに行うタスクであればチェックを入れてください')
# register_process = st.checkbox('プロセスを定義しますか?')

with st.form('create_task', clear_on_submit=False):
    name = st.text_input('タスク名を入力してください')
    major_class = st.text_input('大分類を入力してください')
    minor_class = st.text_input('中分類を入力してください')

    if have_interval:
        interval = st.number_input('タスク実行間隔を入力してください', min_value=1, max_value=366, value=1)
    else:
        days_of_week = st.multiselect(
            label='タスクを実行する曜日を選択してください',
            options=['月', '火', '水', '木', '金', '土', '日'],
        )
    
    #if register_process:
    #    # TODO
    #    pass
    
    do_save = st.form_submit_button('タスクを保存する')

if do_save:
    try:
        current_task_id = tasks_db_controller.create(name, major_class, minor_class, have_interval)
    
        if have_interval:
            intervals_db_controller.create(current_task_id, interval)
        else:
            for day in days_of_week:
                weekdays_db_controller.create(current_task_id, day)
    
        st.info('DBへの登録が完了しました')
    except:
        st.error('DBへの登録に失敗しました')
    finally:
        st.info('処理を完了します')

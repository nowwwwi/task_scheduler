import streamlit as st
from postgres import TasksDbController, HistoriesDbController
import pandas as pd

# Call db controllers
tasks_db_controller = TasksDbController()
histories_db_controller = HistoriesDbController()

# UI
st.markdown('## タスク記録')
tasks = tasks_db_controller.read()

st.markdown('- 実行履歴一覧')
histories = histories_db_controller.read()
merged = pd.merge(tasks, histories, on='task_id', how='inner')
st.write(merged.head(5))

st.markdown('### 記録するタスクを選択してください')
task_id = st.selectbox('タスクを選択', tasks['task_id'])
selected_task = tasks_db_controller.get_entity(task_id)

with st.form('create_record', clear_on_submit=False):
    st.markdown(f'- {selected_task[1]} の実行結果を記録します')

    created_by = st.selectbox(
        label='タスクの実行者を選択してください',
        options=['mari', 'kohei']
    )

    do_save = st.form_submit_button('記録を保存する')

if do_save:
    try:
        histories_db_controller.create(selected_task[0], created_by)
        st.info('DBへの登録が完了しました')
    except:
        st.error('DBへの登録に失敗しました')
    finally:
        st.info('処理を完了します')

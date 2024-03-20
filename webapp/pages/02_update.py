import streamlit as st
from postgres import TasksDbController


tasks_db_controller = TasksDbController()

st.set_page_config(page_title='Update task')
st.markdown('## タスク更新')
st.markdown('- タスク一覧')

tasks = tasks_db_controller.read()
tasks

st.markdown('### 更新するタスクを選択します')


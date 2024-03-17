import streamlit as st
from postgres import TasksDbController


tasks_db_controller = TasksDbController()

st.markdown('## タスク更新')
st.markdown('- タスク一覧')

tasks = tasks_db_controller.read()
tasks

st.markdown('### 更新するタスクを選択します')


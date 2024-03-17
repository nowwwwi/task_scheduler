import streamlit as st
from postgres import TasksDbController

tasks_db_controller = TasksDbController()


st.markdown('## タスク削除')
st.markdown('- タスク一覧')

tasks = tasks_db_controller.read()
tasks
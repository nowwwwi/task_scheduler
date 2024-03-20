import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from postgres import TasksDbController, HistoriesDbController


def display_pie_each_user(df):
    labels = df['executed_by'].unique()
    sizes = []

    for name in labels:
        df_by = (df['executed_by'] == name)
        sizes.append(df_by.sum())

    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.legend()
    st.pyplot()

def display_pie_major_class(df):
    labels = df['majorClass'].unique()
    sizes = []

    for major_class in labels:
        df_class = (df['majorClass'] == major_class)
        sizes.append(df_class.sum())

    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.legend()
    st.pyplot()

def display_pie_minor_class(df):
    labels = df['minorClass'].unique()
    sizes = []

    for minor_class in labels:
        df_class = (df['minorClass'] == minor_class)
        sizes.append(df_class.sum())

    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.legend()
    st.pyplot()

# Call db controllers
tasks_db_controller = TasksDbController()
histories_db_controller = HistoriesDbController()

# UI
st.set_page_config(page_title='View statictics')
st.set_option('deprecation.showPyplotGlobalUse', False)
st.markdown('## 統計情報')
st.markdown('### タスク実行状況')

tasks = tasks_db_controller.read()
histories = histories_db_controller.read()
merged_df = pd.merge(tasks, histories, on='task_id', how='inner')

merged_df

pie_1, pie_2 = st.columns(2)

with pie_1:
    st.markdown('- ユーザ別実行状況')
    display_pie_each_user(merged_df)

with pie_2:
    st.markdown('- 大分類別タスク実行状況')
    display_pie_major_class(merged_df)

pie_3, pie_4 = st.columns(2)

with pie_3:
    st.markdown('- 中分類別タスク実行状況')
    display_pie_minor_class(merged_df)

with pie_4:
    st.markdown('- 実行時間別タスク実行状況')
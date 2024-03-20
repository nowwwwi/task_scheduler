import streamlit as st


st.set_page_config(page_title='[β] Change Options')
st.markdown('## 設定変更')

st.markdown('### LINE Notify')
with st.form('line_notify_settings', clear_on_submit=False):
    token = st.text_input('LINE notifyで発行したAPI tokenを入力してください')
    api_addr = st.text_input('API接続先を入力してください', 'https://notify-api.line.me/api/notify')
    do_update_line = st.form_submit_button('設定変更')

st.markdown('### PostgresDB')
with st.form('postgres_settings', clear_on_submit=False):
    host = st.text_input('ホスト名')
    port = st.number_input('ポート番号',value=5432)
    db_name = st.text_input('DB名')
    user = st.text_input('ユーザ名', 'postgres')
    password = st.text_input('パスワード', 'postgres')
    do_update_db = st.form_submit_button('設定変更')

st.markdown('### アプリケーションの設定')
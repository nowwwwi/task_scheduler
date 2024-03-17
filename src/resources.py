LINE_TOKEN = 'QGLSfegDJD85gOhW7wjgEXDltnQ8ELo6VjYeW6mbNvt'
LINE_TOKEN_PRD = 'SHuarL2gtDPVcC27alcbbDVdSCOfnE0tNCVnpf5011Y'
LINE_API = 'https://notify-api.line.me/api/notify'
POSTGRES_CONNECTIONSTRING = 'host=localhost port=5433 dbname=task_scheduler user=postgres password=postgres'

add_csv_message = '追加タスクをアップロードしてください。'
csv_help_txt = '''
        追加できるCSVフォーマットは以下です

        | 列名 | 説明 | 
        |:-----|:-----|
        | name | タスク名称 |
        | majorClass | 大分類（タスク実行場所） | 
        | minorClass | 中分類（タスクのジャンル） | 
        | interval | タスク実行間隔 |
        | weekDay | 特定の曜日にタスクを実行する場合、入力します | 
        | latestDate | 最終実行日 | 
        '''
weekday_dict = {'月':0, '火':1, '水':2, '木':3, '金':4, '土':5, '日':6}
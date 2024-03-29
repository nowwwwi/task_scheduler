import psycopg2
import pandas as pd
from src import resources
from datetime import datetime
import json

COLUMNS = ['id', 'name', 'majorClass', 'minorClass', 'interval', 'weekDays', 'lastDate']
CREATE = 'INSERT INTO tasks (name,majorClass,minorClass,interval,weekDay,latestDate) VALUES (%s, %s, %s, %s, %s, %s)'
READ = "SELECT * FROM %s"
UPDATE = 'UPDATE tasks SET latestDate = CURRENT_DATE WHERE id = %s'
DELETE = 'DELETE FROM tasks WHERE id = %s'
CONNECTIONSTRING = 'host=%s port=%s dbname=%s user=%s password=%s'

class BaseDbController:
    def __init__(self) -> None:
        # Get settings from json file.
        file = open('webapp/settings.json', 'r')
        self.settings = json.load(file)

        # Create db connection string.
        if self.settings["IsProduction"]:
            connections = self.settings["ConnectionStrings"]["Heroku"]
        else:
            connections = self.settings["ConnectionStrings"]["Docker"]
        
        self.connection_string = f'host={connections["Host"]} port={connections["Port"]} dbname={connections["DbName"]} user={connections["User"]} password={connections["Password"]}'
    
    def create(self, **kwargs):
        pass

    def read(self, **kwargs):
        pass

    def update(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass


class TasksDbController(BaseDbController):
    def __init__(self):
        super().__init__()
        self.db_name = 'tasks'
        self.columns = ['task_id', 'name', 'majorClass', 'minorClass', 'have_interval', 'created_at', 'updated_at']
    
    def create(self, name, majorClass, minorClass, have_interval):
        super.create()
        try:
            self.connection = psycopg2.connect(self.connection_string)
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                'INSERT INTO tasks (name,majorClass,minorClass,have_interval,created_at) VALUES (%s, %s, %s, %s, %s) RETURNING task_id',
                (name, majorClass, minorClass, have_interval, datetime.now()))
            task_id = self.cursor.fetchone()[0]
            self.connection.commit()
            return task_id
        finally:
            self.cursor.close()
            self.connection.close()

    def read(self):
        super().read()
        try:
            self.connection = psycopg2.connect(self.connection_string)
            self.cursor = self.connection.cursor()
            self.cursor.execute(f"SELECT * FROM {self.db_name}")
            rows = self.cursor.fetchall()
            df = pd.DataFrame(rows, columns=self.columns)
            self.connection.close()
            return df.sort_values('task_id')
        finally:
            self.cursor.close()
            self.connection.close()
    
    def get_entity(self, id):
        try:
            self.connection = psycopg2.connect(resources.POSTGRES_CONNECTIONSTRING)
            self.cursor = self.connection.cursor()
            self.cursor.execute(f"SELECT * FROM {self.db_name} WHERE task_id = {id}")
            result = self.cursor.fetchone()
            return result if result else None
        finally:
            self.cursor.close()
            self.connection.close()
    
    def update(self, id):
        super().update()
        self.cursor.execute(UPDATE, f'{id}')
        self.connection.commit()
        self.connection.close()

    def delete(self, id):
        super().delete()
        self.cursor.execute(DELETE, f'{id}')
        self.connection.commit()
        self.connection.close()

class IntervalsDbController(BaseDbController):
    def __init__(self):
        super().__init__()
        self.db_name = 'intervals'
        self.columns = ['interval_id', 'task_id', 'interval']
    
    def create(self, task_id, interval):
        super().create()
        try:
            self.connection = psycopg2.connect(self.connection_string)
            self.cursor = self.connection.cursor()
            self.cursor.execute(
            'INSERT INTO intervals (task_id, interval) VALUES (%s, %s)',
            (task_id, interval)
            )
            self.connection.commit()
        finally:
            self.cursor.close()
            self.connection.close()
    
    def read(self):
        super().create()
        try:
            self.connection = psycopg2.connect(self.connection_string)
            self.cursor = self.connection.cursor()
            self.cursor.execute(f"SELECT * FROM {self.db_name}")
            rows = self.cursor.fetchall()
            df = pd.DataFrame(rows, columns=self.columns)
            return df.sort_values('interval_id')
        finally:
            self.cursor.close()
            self.connection.close()

class WeekdaysDbController(BaseDbController):
    def __init__(self):
        super().__init__()
        self.db_name = 'weekdays'
        self.columns = ['weekday_id', 'task_id', 'day_of_week']
    
    def create(self, task_id, day):
        super().create()
        try:
            self.connection = psycopg2.connect(self.connection_string)
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                'INSERT INTO weekdays (task_id, day_of_week) VALUES (%s, %s)',
                (task_id, day)
            )
            self.connection.commit()
        finally:
            self.cursor.close()
            self.connection.close()
    
    def read(self):
        super().read()
        try:
            self.connection = psycopg2.connect(resources.POSTGRES_CONNECTIONSTRING)
            self.cursor = self.connection.cursor()
            self.cursor.execute(f"SELECT * FROM {self.db_name}")
            rows = self.cursor.fetchall()
            df = pd.DataFrame(rows, columns=self.columns)
            return df.sort_values('weekday_id')
        except:
            self.cursor.close()
            self.connection.close()

class HistoriesDbController(BaseDbController):
    def __init__(self):
        super().__init__()
        self.db_name = 'histories'
        self.columns = ['history_id', 'task_id', 'executed_by', 'executed_at']
    
    def create(self, task_id, updated_by):
        super().create()
        try:
            self.connection = psycopg2.connect(self.connection_string)
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                    'INSERT INTO histories (task_id,updated_by,updated_at) VALUES (%s, %s, %s)',
                    (task_id, updated_by, datetime.now()))
            self.connection.commit()
        finally:
            self.cursor.close()
            self.connection.close()
    
    def read(self):
        super().read()
        try:
            self.connection = psycopg2.connect(self.connection_string)
            self.cursor = self.connection.cursor()
            self.cursor.execute(f"SELECT * FROM {self.db_name}")
            rows = self.cursor.fetchall()
            df = pd.DataFrame(rows, columns=self.columns)
            self.connection.close()
            return df.sort_values('history_id')
        finally:
            self.cursor.close()
            self.connection.close()
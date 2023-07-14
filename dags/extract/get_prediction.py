from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.models.variable import Variable
import pendulum

KST = pendulum.timezone("Asia/Seoul")

default_args = {
    'owner': 'i_am_scouter:v1.0.0',
    'depends_on_past': True,
    'start_date': datetime(2023,1,1, tzinfo=KST)
}

dag = DAG('load_prediction_data',default_args=default_args, tags=['Extract','predictions'], max_active_runs=1, schedule_interval='0 0 * * *')

start = EmptyOperator(
	task_id = 'start_task',
	dag = dag
)

finish = EmptyOperator(
	task_id = 'finish_task',
	dag = dag
)

start >> finish
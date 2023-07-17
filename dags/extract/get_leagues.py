from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
# from airflow.operators.python_operator import PythonOperator
from airflow.operators.empty import EmptyOperator
# from airflow.models.variable import Variable
import pendulum
import sys
sys.path.append("/opt/airflow")

# PARAMETERS
# KST = pendulum.timezone("Asia/Seoul")

default_args = {
    'owner': 'i_am_scouter:v1.0.0',
    'depends_on_past': True,
    'start_date': datetime(2022,1,1)#, tzinfo=KST)
}

# DAG SETTINGS
dag = DAG('load_leagues_data',
		  default_args=default_args,
		  tags=['Extract','leagues'],
		  max_active_runs=1,
		  schedule_interval='0 0 * * *')

# START
start_task = EmptyOperator(
	task_id = 'start.task',
	dag=dag
)

# CHECK DONE
check_DONE = BashOperator(
	task_id='check.dir',
	bash_command="""
	if ls /opt/airflow/flag/leagues-DONE; then rm /opt/airflow/flag/leagues-DONE exit 0
	else exit 1 fi
	""",
	dag=dag
)

# SEND URI
send_uri = BashOperator(
	task_id='send.uri',
	bash_command="""
	python3 /opt/airflow/src/uri/make_uri_leagues.py
	""",
	dag=dag
)

# MAKE DONE FLAG
make_DONE = BashOperator(
	task_id='make.DONE',
	bash_command="""
	touch /opt/airflow/flag/leagues-DONE
	""",
	dag=dag
)

# MAKE ERROR FLAG
make_ERROR = BashOperator(
	task_id='make.ERROR',
	bash_command="""
	touch /opt/airflow/flag/leagues-ERROR
	""",
	dag=dag,
	trigger_rule='one_failed'
)

# FINISH TASK
finish_task = EmptyOperator(
	task_id = 'finish.task',
	dag = dag
)

# OPERATOR PROCEDURE
start_task >> check_DONE >> send_uri >> [make_DONE, make_ERROR]
make_DONE >> finish_task
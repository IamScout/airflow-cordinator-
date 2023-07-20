from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.empty import EmptyOperator
import pendulum, os

os.chdir('/opt/airflow')
main_dir = os.getcwd()

default_args = {
    'owner': 'i_am_scouter:v1.0.0',
    'depends_on_past': True,
    'start_date': datetime(2022,1,20)#, tzinfo=KST)
}

# DAG SETTINGS
dag = DAG('load_players_data',
		  default_args=default_args,
		  tags=['Extract','players'],
		  max_active_runs=1,
		  schedule_interval='0 0 * * *')

# START
start_task = EmptyOperator(
	task_id = 'start_task',
	dag=dag
)

send_uri = BashOperator(
	task_id='load_players_data',
	bash_command=f"""
	python3 {main_dir}/src/uri/make_uri_players.py {date}
	""",
	dag=dag
)

# MAKE DONE FLAG
make_DONE = BashOperator(
	task_id='check_flag_data',
	bash_command=f"""
	curl 34.64.254.93:3000/check/players/?cnt=4455
	""",
	dag=dag
)

def get_done_response(url):
    import subprocess
    command = f"curl '{url}'"
    output = subprocess.check_output(command, shell=True).decode('utf-8').strip()
    if output == "true":
        return "blob_players_data_DL"
    else:
        return "send_nontification"

# BRANCH
branch_check_DONE = BranchPythonOperator(
	task_id="check_flag_players_data",
	python_callable=get_done_response,
	provide_context=True,
	op_kwargs={"url":"34.64.254.93:3000/done-flag/?target_dir=/api/app/datas/json/season_22/players/"},
	dag=dag
)

# CHECK DONE FLAG
blob_job = BashOperator(
    task_id='blob_players_data_DL',
    bash_command=f'''
	curl 34.64.254.93:3000/blob-data/?target_dir=/api/app/datas/json/season_22/players
	''',
    dag=dag
)

# DELETE
clensing_data = BashOperator(
    task_id='clensing_players_data',
    bash_command='''
	curl 34.64.254.93:3000/delete/players/
	''',
    dag=dag
)

# SEND NOTI
# SEND NOTIFICATION
send_noti = BashOperator(
    task_id='send_nontification',
    bash_command='''
    curl -X POST -H 'Authorization: Bearer fxANtArqOzDWxjissz34JryOGhwONGhC1uMN8qc59Z3'
                 -F 'Something is wrong with today's players data' https://notify-api.line.me/api/notify
    ''',
    dag=dag
)

# FINISH TASK
finish_task = EmptyOperator(
	task_id = 'finish.task',
	dag = dag,
    trigger_rule='all_done'
)

# OPERATOR PROCEDURE
start_task >> send_uri >> make_DONE >> branch_check_DONE >> [blob_job, send_noti] 
blob_job >> clensing_data >> finish_task
send_noti >> finish_task
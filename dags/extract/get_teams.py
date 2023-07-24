# CHANGE MAIN DIR
import os
# os.chdir('/Users/kimdohoon/git/IamScout/airflow-cordinator-')
os.chdir('/opt/airflow')
main_dir = os.getcwd()

from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator
import pendulum

# PARAMETERS
date = "{{execution_date.strftime('%Y-%m-%d')}}"

# ARGUMENTS
default_args = {
    'owner': 'i_am_scouter:v1.0.0',
    'depends_on_past': True,
    'start_date': datetime(2022,1,20)
}

# DAG SETTINGS
dag = DAG('load_teams_data',
		  default_args=default_args,
		  tags=['Extract','teams'],
		  max_active_runs=1,
		  schedule_interval='0 0 * * *')

# START
start_task = EmptyOperator(
	task_id = 'start.task',
	dag=dag
)

# SEND URI
# SEND URI CURL TO API SERVER
send_uri = BashOperator(
	task_id='send.uri',
	bash_command=f"""
	python3 {main_dir}/src/uri/make_uri_teams.py
	""",
	dag=dag
)

# MAKE DONE
# CHECK NUMBERS OF FILES > MAKE DONE FLAG TO LOCAL DIR
make_DONE = BashOperator(
	task_id='make.DONE',
	bash_command=f"""
	curl '34.64.254.93:3000/check/teams/?cnt=55'
	""",
	dag=dag
)


def get_done_response(url):
    import subprocess
    command = f"curl '{url}'"
    output = subprocess.check_output(command, shell=True).decode('utf-8').strip()
    if output == "true":
        return "blob.job"
    else:
        return "send.noti"


# BRANCH
branch_check_DONE = BranchPythonOperator(
	task_id="branch.check.DONE",
	python_callable=get_done_response,
	provide_context=True,
	op_kwargs={"url":"34.64.254.93:3000/done-flag/?target_dir=/api/app/datas/json/season_22/teams/"},
	dag=dag
)


# CHECK DONE FLAG
blob_job = BashOperator(
    task_id='blob.job',
    bash_command=f'''
	curl "34.64.254.93:3000/blob-data/?target_dir=/api/app/datas/json/season_22/teams"
	''',
    dag=dag
)

# DELETE
clensing_data = BashOperator(
    task_id='clensing.data',
    bash_command='''
	curl "34.64.254.93:3000/delete/teams/"
	''',
    dag=dag
)

# SEND NOTI
# SEND NOTIFICATION
send_noti = BashOperator(
    task_id='send.noti',
    bash_command='''
    curl -X POST -H 'Authorization: Bearer fxANtArqOzDWxjissz34JryOGhwONGhC1uMN8qc59Z3'
                 -F 'Something is wrong with today's teams data' https://notify-api.line.me/api/notify
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
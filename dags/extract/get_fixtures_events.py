import os, pendulum
os.chdir('/opt/airflow')
main_dir = os.getcwd()
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator

date = "{{execution_date.strftime('%Y-%m-%d')}}"

default_args = {
    'owner': 'i_am_scouter:v1.0.0',
    'depends_on_past': True,
    'start_date': datetime(2022,1,20)
}

# DAG SETTINGS
dag = DAG('load_fixtures_events_data',
		  default_args=default_args,
		  tags=['Extract','fixtures-events', 'fixtures_id'],
		  max_active_runs=1,
		  schedule_interval='0 0 * * *')

start_task = EmptyOperator(
	task_id = 'start_task',
	dag=dag
)

send_uri = BashOperator(
	task_id='get_data_fixtures_events',
	bash_command=f"""
	python3 {main_dir}/src/uri/make_uri_fixtures_events.py {date}
	""",
	dag=dag
)

make_DONE = BashOperator(
	task_id='drop_flag',
	bash_command=f"""
	curl '34.64.254.93:3000/check/fixtures-events/?cnt=55'
	""",
	dag=dag
)

def get_done_response(url):
    import subprocess
    command = f"curl '{url}'"
    output = subprocess.check_output(command, shell=True).decode('utf-8').strip()
    if output == "true":
        return "blob_data_DL"
    else:
        return "send_notification"

branch_check_DONE = BranchPythonOperator(
	task_id="branch_check_flag",
	python_callable=get_done_response,
	provide_context=True,
	op_kwargs={"url":"34.64.254.93:3000/done-flag/?target_dir=/api/app/datas/json/season_22/fixtures_events/"},
	dag=dag
)

# CHECK DONE FLAG
blob_job = BashOperator(
    task_id='blob_data_DL',
    bash_command=f'''
	curl '34.64.254.93:3000/blob-data/?target_dir=/api/app/datas/json/season_22/fixtures_events'
	''',
    dag=dag
)

# DELETE
clensing_data = BashOperator(
    task_id='clensing_fixtures_events',
    bash_command='''
	curl '34.64.254.93:3000/delete/fixtures-events/'
	''',
    dag=dag
)

# SEND NOTI
# SEND NOTIFICATION
send_noti = BashOperator(
    task_id='send_notification',
    bash_command='''
    curl -X POST -H 'Authorization: Bearer fxANtArqOzDWxjissz34JryOGhwONGhC1uMN8qc59Z3'
                 -F 'Something is wrong with today's fixtures/events data' https://notify-api.line.me/api/notify
    ''',
    dag=dag
)

# FINISH TASK
finish_task = EmptyOperator(
	task_id = 'finish_task',
	dag = dag,
    trigger_rule='all_done'
)

# OPERATOR PROCEDURE
start_task >> send_uri >> make_DONE >> branch_check_DONE >> [blob_job, send_noti] 
blob_job >> clensing_data >> finish_task
send_noti >> finish_task

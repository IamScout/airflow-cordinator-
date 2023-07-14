
def gen_noti(name: str, stats: str, role:str):
	#line noti 생성기
	# 날짜로 붙일것인가?
	# noti에 오는 예시 DAG이름 : dag_이름 "stat"
	cmd = """
 		curl -X POST -H 'Authorization: Bearer {{var.value.BEARER_TOKEN_YODA}}' \
 		-F 'message= \n DAG이름 : {{dag.dag_id}} stat!' \
 		https://notify-api.line.me/api/notify
 	"""
	
	cmd = cmd.replace("stat", stats)

	# noti 생성 operator 
	bash_task = BashOperator(
		task_id=name,
 		bash_command=cmd,
 		trigger_rule=role,
 		dag=dag
  	)

	return bash_task

def gen_bash_curl(name: str, url : str, role:str):
	#curl 싸개 생성기

	curl_cmd = "curl link"

	curl_cmd = curl_cmd.replace("link", url)

	# getData 생성 func.
	bash_task = BashOperator(
		task_id=name,
 		bash_command=curl_cmd,
 		trigger_rule=role,
 		dag=dag
  	)

	return bash_task


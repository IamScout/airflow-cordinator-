'''
- FILE COUNT : FIXTURE (fixture_number/day)
'''

# CHANGE MAIN DIR
import os
# os.chdir('/Users/kimdohoon/git/IamScout/airflow-cordinator-')
os.chdir('/opt/airflow')
main_dir = os.getcwd()

# MODULE IMPORT
from datetime import datetime, timedelta
import sys
sys.path.append(f'{main_dir}/lib')
import football_lib as lib

# READ *
date = sys.argv[1]
params_before = lib.read_Params("*", "pipe_round", {"date" : f'"{date}"'})

# MAKE URI LIST
uri_list = []
for count in range(len(params_before)):
    # PARAMS : h2h, date, timezone
    params = {
        "h2h" : f"{params_before[count][2]}-{params_before[count][3]}",
        "date" : date,
        "timezone" : "Europe/London"
    }
    uri = lib.make_uri(params)
    uri_list.append(uri)

# SEND CURL
for uri in uri_list:
    lib.send_curl(uri, "fixtures-headtohead")

# TEST
if __name__ == "__main__":
    pass
    # print(params_before)
    # print(uri_list[:5])
    # data = lib.API_get_infos(uri_list[0])
    # print(data)
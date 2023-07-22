'''
- FILE COUNT : LEAGUE (55/day)
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

# READ LEAGUE ID
params_before = lib.read_Params("api_league_id", "pipe_league")

# MAKE URI LIST
# date = sys.argv[1]
date = "2022-01-20"
uri_list = []
for count in range(len(params_before)):
    params = {
        "league" : params_before[count][0],
        "season" : 2022,
        "date" : date,
        "timezone" : "Europe/London"
    }
    uri = lib.make_uri(params)
    uri_list.append(uri)

# SEND CURL
for uri in uri_list:
    lib.send_curl(uri, "fixtures")

# TEST
if __name__ == "__main__":
    # pass
    print(uri_list[:5])
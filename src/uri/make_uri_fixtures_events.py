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

# READ FIXTURE ID
date = sys.argv[1]
params_before = lib.read_Params("api_fixture_id", "pipe_round", {"date" : f'"{date}"'})
print(params_before)

# MAKE URI LIST
uri_list = []
for count in range(len(params_before)):
    params = {
        "fixture" : params_before[count][0]
    }
    uri = lib.make_uri(params)
    uri_list.append(uri)
    print(uri_list)

# SEND CURL
for uri in uri_list:
    lib.send_curl(uri, "fixtures-events")

# TEST
# NEED TO FIX TABLES
if __name__ == "__main__":
    pass
    # print(uri_list[:5])
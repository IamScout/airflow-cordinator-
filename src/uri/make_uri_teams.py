'''
- FILE COUNT : TEAM (895/day)
'''

# CHANGE MAIN DIR
import os
# os.chdir('/Users/kimdohoon/git/IamScout/airflow-cordinator-')
os.chdir('/opt/airflow')
main_dir = os.getcwd()

# MODULE IMPORT
import sys
sys.path.append(f'{main_dir}/lib')
import football_lib as lib

# READ LEAGUE ID
params_before = lib.read_Params("api_league_id", "pipe_league")

# MAKE URI LIST
uri_list = []
for count in range(len(params_before)):
    params = {
        "league" : params_before[count][0],
        "season" : 2023
    }
    uri = lib.make_uri(params)
    uri_list.append(uri)

# SEND CURL
for uri in uri_list:
    lib.send_curl(uri, "teams")

# TEST
if __name__ == "__main__":
    pass
    # print(uri_list[:5])
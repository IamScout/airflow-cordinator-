'''
- FILE COUNT : TEAM (895/day)
'''

# CHANGE MAIN DIR
import os
os.chdir('/Users/kimdohoon/git/IamScout/airflow-cordinator-')
# os.chdir('/etc/airflow')
main_dir = os.getcwd()

# MODULE IMPORT
import sys
sys.path.append(f'{main_dir}/lib')
import football_lib as lib

# READ *
date = sys.argv[1]
params_before = lib.read_Params("*", "pipe_team")
print(params_before)

# MAKE URI LIST
uri_list = []
for count in range(len(params_before)):
    params = {
        "league" : params_before[count][1],
        "team" : params_before[count][2],
        "season" : 2022,
        "date" :  date
    }
    uri = lib.make_uri(params)
    uri_list.append(uri)

# SEND CURL
for uri in uri_list:
    lib.send_curl(uri, "teams-statistics")

# TEST
if __name__ == "__main__":
    pass
    # print(uri_list[:5])

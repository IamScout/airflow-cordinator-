# MODULE IMPORT
import sys
from datetime import datetime, timedelta
sys.path.append('/Users/kimdohoon/git/airflow-cordinator-/lib/football_lib.py')
import football_lib as lib

# READ TEAM ID
params_before = lib.read_Params("api_team_id", "pipe_team")

uri_list = []
for count in range(len(params_before)):
    params = {
        "team" : params_before[count][0]
    }
    uri = lib.make_uri("players/squads", params)
    uri_list.append(uri)

# SEND CURL
for uri in uri_list:
    lib.send_curl(uri, "players-squads")

# TEST
if __name__ == "__main__":
    print(params_before)
    print(uri_list[:5])
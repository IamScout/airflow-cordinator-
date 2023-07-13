# MODULE IMPORT
from datetime import datetime, timedelta
import sys
sys.path.append('../../lib')
import football_lib as lib

# DATE parameter needs FORM : YYYY-mm-dd
date = (datetime.now() - timedelta(days=100)).strftime("%Y-%m-%d")
# date = {{ds}}

# READ *
params_before = lib.read_Params("*", "pipe_team")

uri_list = []
for count in range(len(params_before)):
    # PARAMS : league, team, season, date
    params = {
        "league" : params_before[count][3],
        "team" : params_before[count][2],
        "season" : 2022,
        "date" :  date
    }
    # MAKE URI
    uri = lib.make_uri("teams/statistics", params)
    uri_list.append(uri)

# SEND CURL
# for uri in uri_list:
#     lib.send_curl(uri, "teams-statistics")

# TEST
if __name__ == "__main__":
    print(params_before)
    print(uri_list[:5])

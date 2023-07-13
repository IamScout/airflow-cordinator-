# MODULE IMPORT
from datetime import datetime, timedelta
import sys
sys.path.append('../../lib')
import football_lib as lib

# DATE parameter needs FORM : YYYY-mm-dd
date = (datetime.now() - timedelta(days=100)).strftime("%Y-%m-%d")
# date = {{ds}}

# READ LEAGUE ID
params_before = lib.read_Params("api_league_id", "pipe_league")

# URI LIST
uri_list = []
for count in range(len(params_before)):
    # PARAMS : league, season, date, timezone
    params = {
        "league" : params_before[count][0],
        "season" : 2022,
        "date" : date,
        "timezone" : "Europe/London"
    }
    # MAKE URI
    uri = lib.make_uri("fixtures", params)
    uri_list.append(uri)

# SEND CURL
for uri in uri_list:
    lib.send_curl(uri, "fixtures")

# TEST
if __name__ == "__main__":
    print(params_before)
    print(uri_list[:5])
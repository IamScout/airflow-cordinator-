# MODULE IMPORT
from datetime import datetime, timedelta
import sys, os
current_dir = os.path.dirname(os.path.abspath(__file__))
relative_path = os.path.join(current_dir, '../../lib')
sys.path.append(relative_path)
import football_lib as lib

# DATE parameter needs FORM : YYYY-mm-dd
date = (datetime.now() - timedelta(days=80)).strftime("%Y-%m-%d")
# date = {{ds}}

# READ FIXTURE ID
params_before = lib.read_Params("api_fixture_id", "pipe_round", {"date" : date})

uri_list = []
for count in range(len(params_before)):
    # PARAMS : fixture
    params = {
        "fixture" : params_before[count][0]
    }
    uri = lib.make_uri("fixtures/players", params)
    uri_list.append(uri)

# SEND CURL
for uri in uri_list:
    lib.send_curl(uri, "fixtures-lineups")

# TEST
# NEED TO FIX TABLES
if __name__ == "__main__":
    print(params_before)
    print(uri_list[:5])
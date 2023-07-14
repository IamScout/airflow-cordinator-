# MODULE IMPORT
from datetime import datetime, timedelta
import sys
sys.path.append('../../lib')
import football_lib as lib

# DATE parameter needs FORM : YYYY-mm-dd
date = (datetime.now() - timedelta(days=80)).strftime("%Y-%m-%d")
# date = {{ds}}

# READ FIXTURE ID
params_before = lib.read_Params("api_fixture_id", "pipe_round", {"date" :  f"'{date}'"})

uri_list = []
for count in range(len(params_before)):
    # PARAMS : fixture
    params = {
        "fixture" : params_before[count][0]
    }
    uri = lib.make_uri(params)
    uri_list.append(uri)

# SEND CURL
for uri in uri_list:
    lib.send_curl(uri, "fixtures-lineups")

# TEST
# NEED TO FIX TABLES
if __name__ == "__main__":
    print(params_before)
    print(uri_list[:5])
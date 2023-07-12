# MODULE IMPORT
import sys, os
current_dir = os.path.dirname(os.path.abspath(__file__))
relative_path = os.path.join(current_dir, '../../lib')
sys.path.append(relative_path)
import football_lib as lib

# READ LEAGUE ID
params_before = lib.read_Params("api_league_id", "pipe_league")

uri_list = []
for count in range(len(params_before)):
    # PARAMS: league, season
    params = {
        "league" : params_before[count][0],
        "season" : 2023
    }
    # MAKE URI
    uri = lib.make_uri("teams", params)
    uri_list.append(uri)

# SEND CURL
for uri in uri_list:
    lib.send_curl(uri, "teams")

# TEST
if __name__ == "__main__":
    print(params_before)
    print(uri_list[:5])
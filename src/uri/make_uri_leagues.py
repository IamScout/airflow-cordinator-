# MODULE IMPORT
import sys
sys.path.append('/Users/kimdohoon/git/football-data-pipeline/lib')
import football_lib as lib

# READ LEAGUE ID
params_before = lib.read_Params("api_league_id", "pipe_league")

uri_list = []
for count in range(len(params_before)):
    params = {
        "id" : params_before[count][0],
        "season" : 2022
    }
    uri = lib.make_uri("leagues", params)
    uri_list.append(uri)

# SEND CURL
for uri in uri_list:
    lib.send_curl(uri, "leagues")

# TEST
if __name__ == "__main__":
    print(params_before)
    print(uri_list[:5])
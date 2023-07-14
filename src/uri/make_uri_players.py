# MODULE IMPORT
import sys
sys.path.append('../../lib')
import football_lib as lib

# READ LEAGUE ID
params_before = lib.read_Params("api_league_id", "pipe_league")

uri_list = []
for values in params_before:
    # READ TEAM ID
    params_origin = lib.read_Params("*", "pipe_team", {"api_league_id" : values[0]})

    for count in range(len(params_origin)):
        for page in range(5):
            league_id = params_origin[count][1]
            team_id = params_origin[count][2]
            # PARAMS : league, team, season, page
            params = {"league" : league_id,
                      "team" : team_id,
                      "season" : 2023,
                      "page" : page + 1}
            # MAKE URI
            uri = lib.make_uri(params)
            uri_list.append(uri)

# SEND CURL
for uri in uri_list:
    lib.send_curl(uri, "players")

# TEST
if __name__ == "__main__":
    print(params_before)
    print(uri_list[:5])
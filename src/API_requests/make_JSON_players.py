# MODULES IMPORT
import sys
sys.path.append('/football-data-pipeline/lib')
import football_lib as lib

# VARIABLES
DIRECTORY = '/Users/kimdohoon/git/football-data-pipeline/datas/JSON/season_22/players'

# REQUEST INFOS
# api_keys = sys.argv[1]
api_keys = "e6b9fb7ce7a7ad7b239595f76e546384"
headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': api_keys
}

# LIB : READ LEAGUE ID
params_before = lib.read_Params("api_league_id", "pipe_league")

# MAKE URI LIST {URI, FILENAME}
uri_list = []
for values in params_before:
    # LIB : READ TEAM ID
    params = lib.read_Params("*", "pipe_team", {"api_league_id" : values[0]})
    # MAKE URI
    for count in range(len(params)):
        for page in range(5):
            league_id = params[count][3]
            team_id = params[count][2]
            params_dict = {"league" : league_id,
                           "team" : team_id,
                           "season" : "2022",
                           "page" : page+1}
            # LIB : MAKE URI
            uri = lib.make_uri("players", params_dict)
            # DEFINE FILENAME
            filename = "players"
            filename += "_" + "_".join(str(value) for value in params_dict.values())
            filename += ".json"
            uri_list.append({"uri" : uri, "filename" : filename})

# LIB : MAKE JSON
lib.make_JSON(uri_list, DIRECTORY, api_keys)
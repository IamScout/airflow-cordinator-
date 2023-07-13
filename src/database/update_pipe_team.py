# MODULE IMPORT
import sys
sys.path.append("../../lib")
import football_lib as lib

# GET LEAGUE_ID [(39,), ..]
league_id = lib.read_Params("api_league_id", "pipe_league")
print(league_id)

cnt = 0
QUERY = []
for league in league_id:
    cnt += 1
    id = cnt # PARAMETER
    api_league_id = league[0] # PARAMETER
    uri = f"https://v3.football.api-sports.io/teams?season=2022&league={api_league_id}"
    response = lib.API_get_infos(uri)['response']
    for index in response:
        api_team_id = index['team']['id'] # PARAMETER
        team_name = index['team']['name'] # PARAMETER
        QUERY_EACH = f'INSERT INTO pipe_team (api_league_id, api_team_id, team_name) \
                VALUES ({api_league_id}, {api_team_id}, \"{team_name}\")'
        QUERY.append(QUERY_EACH)

lib.MySQL_Update(QUERY)
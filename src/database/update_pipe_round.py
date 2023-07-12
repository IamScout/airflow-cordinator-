# MODULE IMPORT
import sys, os
current_dir = os.path.dirname(os.path.abspath(__file__))
relative_path = os.path.join(current_dir, '../../lib')
sys.path.append(relative_path)
import football_lib as lib

# GET LEAGUE_ID [(39,), ..]
league_id = lib.read_Params("api_league_id", "pipe_league")
print(league_id)

QUERY = []
for league in league_id:
    api_league_id = league[0]
    uri = f"https://v3.football.api-sports.io/fixtures?season=2023&league={api_league_id}"
    response = lib.API_get_infos(uri)['response']

    # NEED api_fixture_id, home_team_id, away_team_id, date, start_time
    for index in response:
        api_fixture_id = index['fixture']['id']
        datetime = index['fixture']['date']
        date, start_time = datetime.split("T")
        home_team_id = index['teams']['home']['id']
        away_team_id = index['teams']['away']['id']
        QUERY_EACH = f'INSERT INTO pipe_round (api_fixture_id, home_team_id, away_team_id, date, start_time) \
                     VALUES ({api_fixture_id}, {home_team_id}, {away_team_id}, \"{date}\", \"{start_time}\")'
        # print(QUERY_EACH)
        QUERY.append(QUERY_EACH)

lib.MySQL_Update(QUERY)
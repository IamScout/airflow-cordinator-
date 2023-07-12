# MODULE IMPORT
import sys, os, csv
current_dir = os.path.dirname(os.path.abspath(__file__))
relative_path = os.path.join(current_dir, '../../lib')
sys.path.append(relative_path)
import football_lib as lib

PATH = '/Users/kimdohoon/git/airflow-cordinator-/src/database/pipe_league.csv'

datas = []
with open(PATH, 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        datas.append(row)

QUERY = []
for data in datas:
    id = data[0]
    api_league_id = data[2]
    league_name = data[1]
    league_nation = data[3]
    QUERY_EACH = f"INSERT INTO pipe_league (id, api_league_id, league_name, league_nation) \
            VALUES ({id}, {api_league_id}, '{league_name}', '{league_nation}')"
    print(QUERY_EACH)
    QUERY.append(QUERY_EACH)

lib.MySQL_Update(QUERY)

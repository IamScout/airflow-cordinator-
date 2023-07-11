# MODULE IMPORT
import sys, csv
from datetime import datetime, timedelta
sys.path.append('/Users/kimdohoon/git/football-data-pipeline/lib')
import football_lib as lib

PATH = '/Users/kimdohoon/git/airflow-cordinator-/src/database/pipe_league.csv'

datas = []
with open(PATH, 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        datas.append(row)

cursor = lib.MySQL_Connection()
for data in datas:
    id = data[0]
    api_league_id = data[2]
    league_name = data[1]
    league_nation = data[3]
    QUERY_EACH = f"INSERT INTO pipe_league (id, api_league_id, league_name, league_nation) \
            VALUES ({id}, {api_league_id}, '{league_name}', '{league_nation}')"
    print(QUERY_EACH)
    cursor.execute(QUERY_EACH)

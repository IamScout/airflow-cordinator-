import csv

data = []
PATH = '/Users/kimdohoon/git/airflow-cordinator-/src/database/pipe_league.csv'

with open(PATH, 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        data.append(row)

print(data)
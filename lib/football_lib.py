import mysql.connector as mc
import requests, json, csv, subprocess

# CSV File Located At Local
PATH_DB = '/Users/kimdohoon/src/google/scout_sql.csv'
with open(PATH_DB, 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        db_data = row

PATH_API = '/Users/kimdohoon/src/API/football.csv'
with open(PATH_API, 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        api_data = row

def MySQL_Connection():
    conn = mc.connect(user=db_data[1], \
                      password=db_data[2], \
	                  host=db_data[0], \
	                  database = 'pipeline_scout', \
	                  port = '3306')
    print("Hi! SQL")
    return conn

def MySQL_Update(QUERY:list):
    conn = MySQL_Connection()
    cursor = conn.cursor()
    for que in QUERY:
        cursor.execute(que)
        conn.commit()
        print(f"update finished : {que}")

def read_Params(keyword, table, external: dict = None):
    conn = MySQL_Connection()
    cursor = conn.cursor()
    QUERY = f"SELECT {keyword} FROM {table} "
    if external != None:
        QUERY += "WHERE "
        QUERY += " AND ".join([f"{key}={value}" for key, value in external.items()])
        QUERY = QUERY.rstrip("AND")
    print(QUERY) # > TEST
    cursor.execute(QUERY)
    fetched = cursor.fetchall()
    return fetched

# SEND AND ERASE
def read_FIXTURES(date):
    conn = mc.connect(user=db_data[1], \
                      password=db_data[2], \
                      host=db_data[0], \
                      database='pipeline_scout', \
                      port='3306')
    cursor = conn.cursor()
    QUERY = f"SELECT COUNT(api_fixture_id) FROM pipe_round WHERE date = '{date}'"
    cursor.execute(QUERY)
    fetched = cursor.fetchall()
    return fetched[0]

def make_uri_past(keyword, params: dict):
    base = f"https://v3.football.api-sports.io/{keyword}?"
    for key, value in params.items():
        base += key + "=" + str(value) + "&"
        uri = base.rstrip("&")
    return uri

def make_uri(params: dict):
    base = ""
    for key, value in params.items():
        base += key + "=" + str(value) + "&"
        uri = base.rstrip("&")
    return uri

def API_get_infos(uri):
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': api_data[0]
    }
    response = requests.request("GET", uri, headers=headers).json()
    return response

def make_json(uri, DIRECTORY):
    start_index = uri.find("io/") + 3
    end_index = uri.find("?")

    if start_index != -1 and end_index != -1:
        words = uri[start_index:end_index].split("/")
        english_words = [word for word in words if word.isalpha()]
        FILENAME = "-".join(english_words)

    params = uri.split("&")
    for param in params:
        key, value = param.split("=")
        if key != "season":
            FILENAME += f"-{value}"

    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': api_data[0]
    }
    # GET RESPONSE
    response = requests.request("GET", uri, headers=headers).json()
    # FILE WRITE
    with open(f"{DIRECTORY}/{FILENAME}.json", "w") as file:
        json.dump(response, file, indent=4)
    return(FILENAME + " load is done")

def send_curl(uri, endpoint):
    command = f"curl 34.64.254.93:3000/{endpoint}/?{uri}"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    print(command) ## > TEST
    if error:
        print("ERROR appeared while sending CURL:")
        print(error.decode("utf-8"))

# TEST - players with 1 team id
if __name__ == "__main__":
    url = "https://v3.football.api-sports.io/teams/statistics?league=39&team=33&season=2022&date=2023-03-26"
    DIR = "/Users/kimdohoon/Desktop/"
    make_json(url, DIR)
import mysql.connector as mc
import requests, json, subprocess


def MySQL_Connection_Old():
    conn = mc.connect(user='root', \
                      password= 'tmzkdnxj1', \
	                  host='34.64.214.96', \
	                  database = 'scout', \
	                  port = '3306')
    print("Hi! SQL")
    return conn

def MySQL_Connection():
    conn = mc.connect(user='root', \
                      password= 'tmzkdnxj1', \
	                  host='34.64.214.96', \
	                  database = 'scout', \
	                  port = '3306')
    print("Hi! SQL")
    return conn

def read_Params(keyword, table, external: dict = None):
    conn = MySQL_Connection()
    cursor = conn.cursor()
    QUERY = f"SELECT {keyword} FROM {table} "
    if external != None:
        QUERY += "WHERE "
        QUERY += " AND ".join([f"{key}={value}" for key, value in external.items()])
        QUERY = QUERY.rstrip("AND")
    # TEST
    print(QUERY)
    cursor.execute(QUERY)
    fetched = cursor.fetchall()
    return fetched

def make_uri(keyword, params: dict):
    base = f"https://v3.football.api-sports.io/{keyword}?"
    for key, value in params.items():
        base += key + "=" + str(value) + "&"
        uri = base.rstrip("&")
    return uri

def db_update(uri):
    pass



def make_json_local(uri_list, DIRECTORY, api_keys):
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': api_keys
    }
    for values in uri_list:
        uri = values["uri"]
        filename = values["filename"]
        # GET RESPONSE
        response = requests.request("GET", uri, headers=headers).json()
        # FILE WRITE
        with open(f"{DIRECTORY}/{filename}", "w") as file:
            json.dump(response, file, indent=4)
            print(filename + " load is done")


# https://v3.football.api-sports.io/teams/statistics?league=39&team=33&season=2022&date=2023-03-27


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
        'x-rapidapi-key': "e6b9fb7ce7a7ad7b239595f76e546384"
    }
    # GET RESPONSE
    response = requests.request("GET", uri, headers=headers).json()
    # FILE WRITE
    with open(f"{DIRECTORY}/{FILENAME}", "w") as file:
        json.dump(response, file, indent=4)
    return(FILENAME + " load is done")

def send_curl(uri, endpoint):
    command = f"curl 35.216.48.93:3333/{endpoint}/url={uri}"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        print("ERROR appeared while sending CURL:")
        print(error.decode("utf-8"))


# TEST - players with 1 team id
if __name__ == "__main__":
    # params = read_Params("api_league_id", "pipe_league")
    # params_2 = read_Params("*", "pipe_team", {"api_league_id": params[0][0]})
    # for cnt in range(5):
    #     test_dict = {"league": params_2[0][3], "team": params_2[0][2], "season": "2023", "page": cnt}
    #     print(test_dict)
    #     uri = make_uri("players", test_dict)
    #     print(uri)
    uri = "https://v3.football.api-sports.io/teams/statistics?league=39&team=33&season=2022&date=2023-03-27"
    DIRECTORY = "/Users/kimdohoon/desktop"
    message = make_json(uri, DIRECTORY)
    print(message)
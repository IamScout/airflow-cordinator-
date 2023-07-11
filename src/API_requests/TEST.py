import requests, json
headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': "e6b9fb7ce7a7ad7b239595f76e546384"
}

uri = 'https://v3.football.api-sports.io/teams/statistics?league=39&season=2022&date=2023-03-23'
# GET RESPONSE
response = requests.request("GET", uri, headers=headers).json()
# FILE WRITE
print(response)
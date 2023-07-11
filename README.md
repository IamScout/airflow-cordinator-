# Airflow [Cordinator]
 축구 데이터 적재를 위해 API-SPORTS(https://api-sports.io)에 보낼 request url을 생성하는 Airflow 기반의 배치 파이프라인
 
## Usage
 1. 참조용 파라미터가 적재된 MySQL 데이터베이스 갱신
 2. 당일 갱신되는 데이터들을 요청하기 위한 url 일별 생성
 3. 주간 갱신되는 데이터들을 요청하기 위한 url 주별 생성
 4. 생성된 url을 FAST API 서버로 curl
 
## Tools
 1. Apache Airflow - v2.6.1
 2. Google Cloud Service : MySQL 

## Structure
#### MySQL Database - 23.07.07
<img width="936" alt="스크린샷 2023-07-08 오전 9 31 45" src="https://github.com/IamScout/airflow-cordinator-/assets/130134750/ffd30525-2fb5-4914-8bae-7e9181334435">

#### Airflow
```
코드 블럭 지우고 structure 이미지 혹은 airflow dag 조직도 입력
```
 
## Get Started
```
$ pip install mysql-connector
```
``` 
# 로컬 또는 컨테이너 환경에서 airflow를 실행 중일 경우 아래의 명령어로 시작
$ airflow standalone
```

## Tree - 23.07.06
```
├── README.md
├── dags
│   └── extract
│       └── extract_players.py
├── datas
│   ├── JSON
│   │   └── season_22
│   │       ├── fixtures
│   │       ├── fixtures_events
│   │       ├── fixtures_headtohead
│   │       ├── fixtures_lineups
│   │       ├── fixtures_players
│   │       ├── fixtures_statistics
│   │       ├── leagues
│   │       ├── players
│   │       ├── players_squads
│   │       ├── players_topscorers
│   │       ├── predictions
│   │       ├── standings
│   │       ├── teams
│   │       └── teams_statistics
│   └── README.MD
├── lib
│   ├── __pycache__
│   │   └── football_lib.cpython-37.pyc
│   └── football_lib.py
├── sh
├── src
│   ├── API_requests
│   │   ├── TEST.py
│   │   └── make_JSON_players.py
│   └── uri
│       ├── make_uri_fixtures.py
│       ├── make_uri_fixtures_events.py
│       ├── make_uri_fixtures_headtohead.py
│       ├── make_uri_fixtures_lineups.py
│       ├── make_uri_fixtures_players.py
│       ├── make_uri_fixtures_statistics.py
│       ├── make_uri_leagues.py
│       ├── make_uri_players.py
│       ├── make_uri_players_squads.py
│       ├── make_uri_players_topscorers.py
│       ├── make_uri_predictions.py
│       ├── make_uri_standings.py
│       ├── make_uri_teams.py
│       └── make_uri_teams_statistics.py
└── tree.log

```

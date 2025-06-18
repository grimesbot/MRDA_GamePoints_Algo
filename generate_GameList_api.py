# This script generates a list of games from the MRDA sanctioning API
# and formats them for use in a GameList_api.py file.

import requests
from datetime import datetime, timedelta
import os

team_map = {
    'Austin Anarchy - primary': 'AUA',
    'Casco Bay Roller Derby - primary': 'CBRD',
    'Casco Bay Roller Derby - secondary': 'CBRD(B)',
    'Chicago Bruise Brothers - primary': 'CBB',
    'Chicago Bruise Brothers - secondary': 'CBB(B)',
#hiatus    'Capital City Hooligans - primary':'CCH',
    'Chinook City Roller Derby - primary': 'ChCRD',
    'Cleveland Guardians Roller Derby - primary': 'CGRD',
#hiatus    'Collision Roller Derby - primary': 'COL',
    'Concussion Roller Derby - primary': 'CRD',
    'Concussion Roller Derby - secondary': 'CRD(B)',
    'Carolina Wreckingballs - primary': 'CWB',
    'Dallas Derby Devils - primary': 'DDD',
    'Detroit Mens Roller Derby - primary': 'DMRD',
    'Denver Ground Control - primary': 'DGC',
    'Disorder - primary': 'DIS',
    'Flour City Roller Derby - primary': 'FCF',
    'Magic City Misfits - primary': 'MCM',
    'Philadelphia Hooligans - primary': 'PHH',
    'Philadelphia Hooligans - secondary': 'PHH(B)',
    'Pittsburgh Roller Derby - primary': 'PIT',
    'Pittsburgh Roller Derby - secondary': 'PIT(B)',
    'Puget Sound Outcast Derby - primary': 'PSOD',
    'Race City Rebels - primary': 'RCR',
    'San Diego Aftershocks - primary': 'SDA',
    'San Diego Aftershocks - secondary': 'SDA(B)',
    'Saint Louis Gatekeepers - primary': 'SLGK',
    'Saint Louis Gatekeepers - secondary': 'SLGK(B)',
    'Tampa Roller Derby - primary': 'TMP',
    'Terminus Roller Derby - primary': 'TRD',
    'Toronto Mens Roller Derby - primary': 'TMRD',
    'Wisconsin United Roller Derby - primary': 'WURD',

    'Borderland Bandits Roller Derby - primary': 'BBRD',
    'Crash Test Brummies - primary': 'CTB',
    'D.H.R. Mens Roller Derby - primary': 'DHR',
    'Kent Mens Roller Derby - primary': 'KMRD',
    'Manchester Roller Derby - primary': 'MRD',
    'Manchester Roller Derby - secondary': 'MRD(B)',
    'Nordicks de Touraine - primary': 'NDT',
    'Orcet Roller Derby - primary': 'ORD',
    'Panam Squad - primary': 'PAN',
    'Roller Derby Nantes Atlantique - primary': 'RDNA',
    'Roller Derby Toulouse - primary': 'RDT',
    'Southern Discomfort Roller Derby - primary': 'SDRD',
    'South Wales Silures - primary': 'SWS',
    'The Inhuman League - primary': 'TIL',
    'Tyne and Fear Roller Derby - primary': 'TNF',
    'Tyne and Fear Roller Derby - secondary': 'TNF(B)',
    'Wirral Roller Derby - primary': 'WRD',
    
    '15 Ronins Roller Derby - primary': '15RRD',
}

class SanctionedGame:
    def __init__(self, event_data):
        self.game_datetime = event_data['game_datetime']
        self.home_team = team_map[event_data['home_league_name'] + ' - ' + event_data['home_league_charter']]
        self.away_team = team_map[event_data['away_league_name'] + ' - ' + event_data['away_league_charter']]
        self.validated = event_data['status'] == '7'
        self.forfeit = event_data['forfeit'] == 1
        if self.forfeit and event_data['forfeit_league'] == event_data['home_league']:
            self.home_score = 0
            self.away_score = 100
        elif self.forfeit and event_data['forfeit_league'] == event_data['away_league']:
            self.home_score = 100
            self.away_score = 0
        else:
            self.home_score = event_data['home_league_score']
            self.away_score = event_data['away_league_score']
        

class SanctioningEvent:
    def __init__(self, data):
        self.event_name = data['sanctioning']['event_name']
        self.games = [SanctionedGame(data['event'])]

#call sanctioning API to get validated scores from Jan 2024 to today
url = "https://api.mrda.org/v1-public/sanctioning/algorithm"
params = {
    "start-date": "01/01/2024",
    "end-date": datetime.now().strftime("%m/%d/%Y")
}

response = requests.get(url, params=params)
response.raise_for_status()  # Raises an error for bad responses

data = response.json()
payload = data.get('payload', [])
if not payload or not data["success"]:
    print("No data found in the payload.")
    exit()

#call again to get unvalidated scores from last 30 days, expect to be validated in good faith
url_unvalidated = "https://api.mrda.org/v1-public/sanctioning/algorithm"
params_unvalidated = {
    "start-date": (datetime.now() - timedelta(days=30)).strftime("%m/%d/%Y"),
    "end-date": datetime.now().strftime("%m/%d/%Y"),
    "status": 4
}

response_unvalidated = requests.get(url_unvalidated, params=params_unvalidated)
response_unvalidated.raise_for_status()  # Raises an error for bad responses

data_unvalidated = response_unvalidated.json()
payload_unvalidated = data_unvalidated.get('payload', [])
if not payload_unvalidated or not data_unvalidated["success"]:
    print("No data found in the payload.")
    exit()

#combine validated and unvalidated games
payload.extend(payload_unvalidated)

sanctioningEvent_dict = {}

#sort by game_datetime
def game_datetime(sanctioning_event_data):
  return sanctioning_event_data['event']['game_datetime']

#group games by sanctioning_id
for item in sorted(payload, key=game_datetime):
    sanctioning_id = item['event']['sanctioning_id']
    if sanctioning_id not in sanctioningEvent_dict:
        sanctioningEvent_dict[sanctioning_id] = SanctioningEvent(item)
    else: 
        sanctioningEvent_dict[sanctioning_id].games.append(SanctionedGame(item['event']))

#write to GamesList_api.py, delete if exists
gameslist_filename = "GamesList_api.py"
if os.path.exists(gameslist_filename):
    os.remove(gameslist_filename)

#write header and games to GamesList_api.py
with open(gameslist_filename, "w", encoding="utf-8") as f:
    f.write("#Generated by generate_GameList_api.py on {}\n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    f.write("games_api = [\n")
    for sanctioning_id, event in sanctioningEvent_dict.items():
        if event.event_name:
            f.write(f"    [   #{event.event_name}\n")
        else: 
            f.write(f"    [\n")
        for game in event.games:
            game_datetime = datetime.strptime(game.game_datetime, "%Y-%m-%d %H:%M:%S")
            comment = ""
            if game.forfeit:
                comment += " #forfeit"
            if not game.validated:
                comment += " #not yet validated"
            f.write(f"        ('{game_datetime.strftime('%Y-%m-%d')}', '{game.home_team}', {game.home_score}, '{game.away_team}', {game.away_score}),{comment}\n")
        f.write("    ],\n")
    f.write("]\n")
    
print(f"Games list generated in {gameslist_filename}")
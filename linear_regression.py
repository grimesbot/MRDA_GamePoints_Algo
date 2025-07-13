import statsmodels.api as sm
import math

from datetime import datetime
from datetime import date

from GameList_history import games
from GamesList_api import games_api

RANKING_SCALE = 100 # add scale since we are not using seeds here
RATIO_CAP = 4

#2023 games 
flattened_games = [ game for gameday in games for game in gameday]

teams = []

for game in flattened_games:
    team_1 = game[1]
    team_2 = game[3]
    if not team_1 in teams:
        teams.append(team_1)
    if not team_2 in teams:
        teams.append(team_2)

Y = []
X = []
W = []

for game in flattened_games:
    team_1 = game[1]
    score_1 = game[2]
    team_2 = game[3]
    score_2 = game[4]

    if (score_1 == 0 or score_2 == 0):
        continue
    
    Y.append(math.log(score_1/score_2))
    
    x_col = []
    for team in teams:
        if (team == team_1):
            x_col.append(1)
        elif (team == team_2):
            x_col.append(-1)
        else:
            x_col.append(0)
    X.append(x_col)

    score_ratio = score_1/score_2 if score_1 > score_2 else score_2/score_1 
    if (score_ratio > RATIO_CAP):
        W.append(max(3 ** ((4 - score_ratio)/2), 1/1000000))
    else:
        W.append(1)

result = sm.WLS(Y, X, W).fit().params
rankings = [ math.exp(log_result) * RANKING_SCALE for log_result in result ]

team_rankings_2023 = []

for i, team in enumerate(teams):
    team_rankings_2023.append([ team, rankings[i] ])

def rank(team_ranking):
    return team_ranking[1]     

print("2023 Rankings:")

for team_ranking in sorted(team_rankings_2023, key=rank, reverse=True):
    print(team_ranking[0] + ": " + str(team_ranking[1]))

print("")

#2024 Rankings with 2023 seed data

flattened_games = [ game for gameday in games_api for game in gameday]

teams = []

for game in flattened_games:
    if (datetime.strptime(game[0],'%Y-%m-%d').date().year == 2024 and game[2] > 0 and game[4] > 0):    
        team_1 = game[1]
        team_2 = game[3]
        if not team_1 in teams:
            teams.append(team_1)
        if not team_2 in teams:
            teams.append(team_2)

Y = []
X = []
W = []

for game in flattened_games:
    if (datetime.strptime(game[0],'%Y-%m-%d').date().year == 2024):
        team_1 = game[1]
        score_1 = game[2]
        team_2 = game[3]
        score_2 = game[4]

        if (score_1 == 0 or score_2 == 0):
            continue
        
        Y.append(math.log(score_1/score_2))
        
        x_col = []
        for team in teams:
            if (team == team_1):
                x_col.append(1)
            elif (team == team_2):
                x_col.append(-1)
            else:
                x_col.append(0)
        X.append(x_col)

        score_ratio = score_1/score_2 if score_1 > score_2 else score_2/score_1 
        if (score_ratio > RATIO_CAP):
            W.append(max(3 ** ((4 - score_ratio)/2), 1/1000000))
        else:
            W.append(1)

for team in teams:
    initial_ranking = -1
    for team_ranking in team_rankings_2023:
        if team_ranking[0] == team:
            initial_ranking = team_ranking[1]
            continue
    #existing team, create virtual game
    if (initial_ranking > -1):
        Y.append(math.log(initial_ranking/1.00))

        x_col = []
        for t in teams:
            if (t == team):
                x_col.append(1)
            else:
                x_col.append(0)
        X.append(x_col)
        
        close_games_count = 0

        for g in flattened_games:
            if (datetime.strptime(g[0],'%Y-%m-%d').date().year == 2024):
                if ((g[1] == team or g[3] == team) and g[2] > 0 and g[4] > 0 and g[2]/g[4] < RATIO_CAP and g[4]/g[2] < RATIO_CAP):
                    close_games_count+=1

        if (close_games_count >= 5):
            W.append(1/1000000)
        else:
            W.append(1)

result = sm.WLS(Y, X, W).fit().params
rankings = [ math.exp(log_result) for log_result in result ]

team_rankings_2024 = []

for i, team in enumerate(teams):
    team_rankings_2024.append([ team, rankings[i] ])

print("2024 Rankings:")

for team_ranking in sorted(team_rankings_2024, key=rank, reverse=True):
    print(team_ranking[0] + ": " + str(team_ranking[1]))

print("")

#2025 Rankings with 2024 seed data

teams = []

for game in flattened_games:
    if (datetime.strptime(game[0],'%Y-%m-%d').date().year == 2025 and game[2] > 0 and game[4] > 0):
        team_1 = game[1]
        team_2 = game[3]
        if not team_1 in teams:
            teams.append(team_1)
        if not team_2 in teams:
            teams.append(team_2)

Y = []
X = []
W = []

for game in flattened_games:
    if (datetime.strptime(game[0],'%Y-%m-%d').date().year == 2025):
        team_1 = game[1]
        score_1 = game[2]
        team_2 = game[3]
        score_2 = game[4]

        if (score_1 == 0 or score_2 == 0):
            continue
        
        Y.append(math.log(score_1/score_2))
        
        x_col = []
        for team in teams:
            if (team == team_1):
                x_col.append(1)
            elif (team == team_2):
                x_col.append(-1)
            else:
                x_col.append(0)
        X.append(x_col)

        score_ratio = score_1/score_2 if score_1 > score_2 else score_2/score_1 
        if (score_ratio > RATIO_CAP):
            W.append(max(3 ** ((4 - score_ratio)/2), 1/1000000))
        else:
            W.append(1)

for team in teams:
    initial_ranking = -1
    for team_ranking in team_rankings_2024:
        if team_ranking[0] == team:
            initial_ranking = team_ranking[1]
            continue
    #existing team, create virtual game
    if (initial_ranking > -1):
        Y.append(math.log(initial_ranking/1.00))

        x_col = []
        for t in teams:
            if (t == team):
                x_col.append(1)
            else:
                x_col.append(0)
        X.append(x_col)
        
        close_games_count = 0

        for g in flattened_games:
            if (datetime.strptime(g[0],'%Y-%m-%d').date().year == 2025):
                if ((g[1] == team or g[3] == team) and g[2] > 0 and g[4] > 0 and g[2]/g[4] < RATIO_CAP and g[4]/g[2] < RATIO_CAP):
                    close_games_count+=1

        if (close_games_count >= 5):
            W.append(1/1000000)
        else:
            W.append(1)

result = sm.WLS(Y, X, W).fit().params
rankings = [ math.exp(log_result) for log_result in result ]


team_rankings_2025 = []

for i, team in enumerate(teams):
    team_rankings_2025.append([ team, rankings[i] ])

print("2025 Rankings:")

for team_ranking in sorted(team_rankings_2025, key=rank, reverse=True):
    print(team_ranking[0] + ": " + str(team_ranking[1]))
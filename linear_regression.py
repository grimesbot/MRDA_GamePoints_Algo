import statsmodels.api as sm
import math
RANKING_SCALE = 100 # add scale since we are not using seeds here
RATIO_CAP = 4
from GameList_history import games

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

    if (score_1/score_2 > RATIO_CAP or score_2/score_1 > RATIO_CAP):
        W.append(max(3 ** ((4 - score_1/score_2)/2), 1/1000000))
    else:
        W.append(1)

result = sm.WLS(Y, X, W).fit().params
rankings = [ math.exp(log_result) * RANKING_SCALE for log_result in result ]

team_rankings = []

for i, team in enumerate(teams):
    team_rankings.append([ team, rankings[i] ])

def rank(team_ranking):
    return team_ranking[1]     

for team_ranking in sorted(team_rankings, key=rank, reverse=True):
    print(team_ranking[0] + ": " + str(team_ranking[1]))

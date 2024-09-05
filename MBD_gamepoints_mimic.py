# -*- coding: utf-8 -*-
"""
Created on Wed May  1 08:42:51 2024

@author: shender
"""
from datetime import datetime
# from datetime import date
from dateutil.relativedelta import relativedelta
import tkinter as tk
from tkinter import simpledialog
from tkcalendar import Calendar
from GameList import games_e
from GameList import games_w
from dicts import initial_ratings_e
from dicts import initial_ratings_w
from dicts import team_names
from dicts import gamecount_active

class RollerDerbyRanks:

    def __init__(self, initial_ratings=None):
        self.ratings = initial_ratings if initial_ratings else {}
        self.gamecount = gamecount_active
        print("set to intial rank")

    def add_team(self, team_name, initial_rating=400):
        if team_name not in self.ratings:
            self.ratings[team_name] = initial_rating

    def set_rating(self, team_name, rating):
        self.ratings[team_name] = rating

    def set_gcount(self, team_name, gcount):
        self.gamecount_active[team_name] = gcount

    def update_ratings(self, g):
        for game in g:
            gdate, team_a, score_a, team_b, score_b = game
            self.add_team(team_a)
            self.add_team(team_b)
            
            game_d = datetime.strptime(gdate,'%Y-%m-%d').date()
            
            if game_d > dateQuery:
                #print("skip this gameday")
                continue             

            ra = self.ratings[team_a]
            rb = self.ratings[team_b]

            # Calculate expected scores
            ea = ra/rb
            if ea < 0.33:
                ea = 0.33
            if ea > 3:
                ea = 3
            
            eb = rb/ra
            if eb < 0.33:
                eb = 0.33
            if eb > 3:
                eb = 3
        
            # Determine actual scores
            if score_a == 0:
                score_a = 1
            if score_b == 0:
                score_b = 1
            sa = score_a/score_b
            if sa < 0.33:
                sa = 0.33
            if sa > 3:
                sa = 3
            sb = score_b/score_a
            if sb < 0.33:
                sb = 0.33
            if sb > 3:
                sb = 3
                
            #Game points:
            gpa = ra * (sa/ea)
            gpb = rb * (sb/eb)
            
            #Add game points to game list for each teams.
            for x in team_gp_list:
                if x[0] == team_a:
                    x.append((game_d,gpa))
            for x in team_gp_list:
                if x[0] == team_b:
                    x.append((game_d,gpb))
            print(game_d,team_a,ra,f"{gpa:.2f}",team_b,rb,f"{gpb:.2f}")       #Uncomment for game point details
        print('\n')   
        #compute new team score
        for team in team_gp_list:
            gp = 1
            gcount = 0
            if len(team) > 1:
                exp = 0
                for x in team[1:]:
                    if x[0] < (game_d + relativedelta(months=-12)):
                        #print("game too old")
                        continue
                    elif x[0] < (game_d + relativedelta(months=-9)):
                        wt = 0.25
                    elif x[0] < (game_d + relativedelta(months=-6)):
                        wt = 0.5
                    else:
                        wt = 1

                    gp_weighted = x[1]**wt
                    gp *= gp_weighted
                    exp += wt
                    
                    power = 1/(exp)
                    gpf = pow(gp,power)
                    self.ratings[team[0]] = gpf
                    # if(team[0]=='CRD'):     #Enter a team to track their gpf for troubleshooting
                    #     print(game_d,x[0],wt,"current gpf = ",gpf)
                    
                    #ADD GAME COUNT WITH DATE CHECK VS DATEQUERY HERE
                    gcount += 1
                self.gamecount[team[0]] = gcount
                    
        
    def get_rating(self, team_name):
        return self.ratings.get(team_name, "Team not found")


ROOT = tk.Tk()
ROOT.withdraw()
dateQuery = simpledialog.askstring(title="test", prompt='Enter ranking date in YYY-MM-DD format:')
dateQuery = datetime.strptime(dateQuery,'%Y-%m-%d').date()
print(dateQuery)

print('\n')

rank_e = RollerDerbyRanks(initial_ratings_e)
rank_w = RollerDerbyRanks(initial_ratings_w)

team_gp_list = [['BOR'],['CTB'],['KEM'],
                ['MRD'],['MRD(B)'],['SWS'],['TIL'],['TNF'],['TNF(B)']]

for gameday_e in games_e:
    if datetime.strptime(gameday_e[0][0],'%Y-%m-%d').date() < dateQuery:
        rank_e.update_ratings(gameday_e)

print("\n")
print("Game count")
t = 0
for team in team_gp_list:
    print(team[0] , len(team_gp_list[t])-1)
    t += 1

team_gp_list = [['AUA'],['CAB'],['CAB(B)'],['CBB'],['CBB(B)'],['CHK'],['CLG'],['CWB'],
                ['DEM'],['DGC'],['DIS'],
                ['FLC'],['CRD'],['CRD(B)'],['PHH'],['PHH(B)'],['PIT'],['PIT(B)'],['PSO'],['MCM'],
                ['RCR'],['SLG'],['SLG(B)'],['SDA'],['SDA(B)'],
                ['TOM'],['TRD']]

for gameday_w in games_w:
    if datetime.strptime(gameday_w[0][0],'%Y-%m-%d').date() < dateQuery:
        rank_w.update_ratings(gameday_w)

ratings_e = {team: rank_e.get_rating(team) for team in
             ['BOR', 'CTB', 'KEM', 'MRD', 'MRD(B)', 'TIL', 'TNF', 'TNF(B)', 'SWS']}

ratings_w = {team: rank_w.get_rating(team) for team in
             ['AUA', 'CWB', 'CAB', 'CBB', 'CHK', 'CLG', 'DGC', 'DEM', 'DIS', 'FLC', 'CRD', 'MCM', 'PHH', 'PHH(B)', 'PIT', 'PIT(B)',
              'PSO', 'RCR', 'SDA', 'SLG', 'TRD', 'TOM']}

sorted_ratings_e = sorted(rank_e.ratings.items(), key=lambda item: item[1], reverse=True)
sorted_ratings_w = sorted(rank_w.ratings.items(), key=lambda item: item[1], reverse=True)

print("\n")
print(f"Rankings as of {dateQuery}")
# Print the ratings in a formatted table
print("MRDA West")
print("Position\tTeam\tGPA")
position = 1
for code, rating in sorted_ratings_w:
    if gamecount_active[code] > 2:
        full_name = team_names.get(code, "Unknown Team")
#        print(f"{position}\t{code}\t{rating:.2f}")
        print(f"{position}\t{full_name}\t{rating:.2f}") if (gamecount_active[code] > 4 or (code in ['CRD','CRD(B)','DIS','PSO','SDA','SDA(B)'] and gamecount_active[code] > 2)) else print(f"{position}\t{full_name}*\t{rating:.2f}")
        position += 1
print("\n")
print("MRDA East")
print("Position\tTeam\tGPA")
position = 1
for code, rating in sorted_ratings_e:
    if gamecount_active[code] > 2:
        full_name = team_names.get(code, "Unknown Team")
        print(f"{position}\t{full_name}\t{rating:.2f}") if gamecount_active[code] > 4 else print(f"{position}\t{full_name}*\t{rating:.2f}")
        position += 1


# -*- coding: utf-8 -*-
"""
Created on Wed May  1 08:42:51 2024

@author: shender
"""
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
import tkinter as tk
from tkinter import simpledialog

class RollerDerbyRanks:

    def __init__(self, initial_ratings=None):
        self.ratings = initial_ratings if initial_ratings else {}
        print("set to intial rank")

    def add_team(self, team_name, initial_rating=400):
        if team_name not in self.ratings:
            self.ratings[team_name] = initial_rating

    def set_rating(self, team_name, rating):
        self.ratings[team_name] = rating
        print("set to new rank")

    def update_ratings(self, g):
        for game in g:
            gdate, team_a, score_a, team_b, score_b = game
            self.add_team(team_a)
            self.add_team(team_b)
            
            #could add the ability to enter a defined date to be able to run past Q results more accurately
            # six_mo = date.today() + relativedelta(months=-6)
            # twelve_mo = date.today() + relativedelta(months=-12)
            twelve_mo = dateQuery + relativedelta(months=-12)            
            six_mo = dateQuery + relativedelta(months=-6)
            three_mo = dateQuery + relativedelta(months=-3)
            game_d = datetime.strptime(gdate,'%Y-%m-%d').date()
            
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
            
            if game_d > dateQuery:
                continue             
            if game_d < twelve_mo:
                continue
                #wt = 0
            elif game_d < six_mo:
                wt = 0.25
            elif game_d < three_mo:
                wt = 0.5
            else:
                wt = 1
            
            #Add game points to game list for each teams.
            for x in team_gp_list:
                if x[0] == team_a: # "['" + team_a + "']":
                    x.append((game_d,gpa,wt))
            for x in team_gp_list:
                if x[0] == team_b: # "['" + team_a + "']":
                    x.append((game_d,gpb,wt))
            print(game_d,team_a,ra,f"{gpa:.2f}",team_b,rb,f"{gpb:.2f}",wt)       #Uncomment for game point details
        print('\n')   
        #compute new team score
        for team in team_gp_list:
            gp = 1
            if len(team) > 1:
                exp = 0
                for x in team[1:]:
                    gp_weighted = x[1]**x[2]
                    gp *= gp_weighted
                    exp += x[2]
                power = 1/(exp)
                gpf = pow(gp,power)
                
                self.ratings[team[0]] = gpf
        
    def get_rating(self, team_name):
        return self.ratings.get(team_name, "Team not found")

initial_ratings_e = {'BOR': 700, 
                      'CTB': 300, 
                      'DHR': 200, 
                      'KEM': 450,
                      'MRD': 900, 
                      'MRD(B)': 200, 
                      'PAN': 250,  
                      'TIL': 600,
                      'TNF': 700, 
                      'TNF(B)': 200, 
                      'SWS': 350,
                      }


initial_ratings_w = {
                      'DGC': 1000,
                      'SLG': 1200,
                      'SDA': 650,
                      'MCM': 900,
                      'LCC': 450,
                      'DIS': 450,
                      'PSO': 350,
                      'CWB': 425,
                      'RCR': 425,
                      'PIT': 300,
                      'CBB': 400,
                      'PHH': 250,
                      'AUA': 200,
                      'TOM': 300,
                      'CAB': 300,
                      'FLC': 100,
                      'CHC': 250,
                      'DEM': 80,
                      'TRD': 50,
                      'CLM': 50,
                      'PIT(B)': 20,
                      'CBB(B)': 40,
                      'SDA(B)': 132,
                      'SLG(B)': 204,
                      'CAB(B)': 40,
                      'LCC(B)': 100,
}


#Games have been updated with dates.
games_e = [
    [
        ('2023-05-06','KEM', 81, 'TIL', 197),
        ('2023-05-06','SWS', 66, 'TIL', 250),
        ('2023-05-06','CTB', 109, 'SWS', 108),
        ('2023-05-06','CTB', 107, 'KEM', 210),
        ('2023-05-07','CTB', 70, 'TIL', 279),
        ('2023-05-07','KEM', 224, 'SWS', 128)
    ],

    [
        ('2023-06-24','MRD', 274, 'TNF', 261)
    ],
    
    [
        ('2023-07-22','TIL', 217, 'TNF', 299)
    ],
    
    [
        ('2023-07-29','MRD', 300, 'TNF', 147)
    ],
    [
        ('2023-09-09','TIL', 193, 'KEM', 106)
    ],
    [   #ACE Autumn Clash
        ('2023-11-18','DHR', 82, 'BOR', 256),
        ('2023-11-18','PAN', 111, 'BOR', 193),
        ('2023-11-18','DHR', 103, 'PAN', 158)
    ],
    [
        ('2023-11-25','TIL', 91, 'MRD', 219)
    ],
#2024
    [
        ('2024-02-10','BOR', 197, 'TIL', 193),
        ('2024-02-10','TNF', 484, 'KEM', 103),
    ],
    [
        ('2024-02-24','SWS', 257, 'TNF(B)', 165),
        ('2024-02-24','MRD(B)', 129, 'SWS', 219),
        ('2024-02-25','MRD', 239, 'TNF', 249),
        ('2024-02-25','TNF', 291, 'TIL', 246)
    ],
    [
        ('2024-03-16','CTB', 300, 'TNF(B)', 246),
    ],
    [
         ('2024-04-13','BOR', 521, 'KEM', 66),
         ('2024-04-13','MRD', 264, 'TIL', 116),
    ],
    [
        ('2024-04-20','CTB', 262, 'SWS', 158),
        ('2024-04-20','MRD(B)', 299, 'TNF(B)', 181),
    ],
    [
        ('2024-05-19','BOR', 213, 'TNF', 253),
        ('2024-05-19','KEM', 21, 'MRD', 308)
    ],
    [
        ('2024-06-23','TIL', 338, 'KEM', 117),
        ('2024-06-23','BOR', 271, 'MRD', 101)
    ],
    [
        ('2024-07-06','TNF', 429, 'TIL', 203),
#        ('2024-07-07','CTB', 1, 'MRD', 1)
    ],
]

games_w = [

    [
        ('2023-04-22', 'PHH', 152, 'PIT', 172),
    ],
    [
        ('2023-05-12','TOM', 168, 'CHC', 176),
    ],
    [
        ('2023-05-13','CHC', 148, 'TOM', 173),
#        ('2023-05-13','RCR', 100, 'SLG', 0),
        ('2023-05-13','TRD', 66, 'PIT', 533),
    ],
    [
        ('2023-05-14','TRD', 169, 'CLM', 115),
    ],
    [
        ('2023-05-20','CAB', 353, 'DEM', 56),
        ('2023-05-20','CAB', 334, 'CLM', 46),
        ('2023-05-20','CLM', 137, 'DEM', 206),
    ],
    [
        ('2023-06-03','CLM', 37, 'PHH', 208),
        ('2023-06-03','PHH', 96, 'TOM', 91),
        ('2023-06-04','CLM', 51, 'TOM', 364),
    ],
    [
        ('2023-06-10','DEM', 59, 'RCR', 339),
    ],
    [   #Sibling Rivalry
        ('2023-06-16','CAB', 113, 'SDA', 236),
        ('2023-06-17','DGC', 230, 'SDA', 120),
        ('2023-06-17','DGC', 113, 'SLG', 168),
        ('2023-06-17','SLG', 284, 'CAB', 77),
        ('2023-06-18','CAB', 55, 'DGC', 413),
        ('2023-06-18','SDA', 75, 'SLG', 290),
    ],
    [   #DOTD
        ('2023-06-24','AUA', 135, 'PIT', 121),
        ('2023-06-24','AUA', 43, 'CBB', 173),
        ('2023-06-24','CWB', 172, 'DIS', 175),
        ('2023-06-24','CWB', 147, 'LCC', 136),
        ('2023-06-24','CBB', 124, 'PIT', 135),
        ('2023-06-24','DIS', 180, 'LCC', 96),
        ('2023-06-25','CWB', 232, 'AUA', 91),
        ('2023-06-25','CBB', 102, 'DIS', 142),
        ('2023-06-25','PIT', 122, 'LCC', 115),
    ],
    [
        ('2023-07-08','CWB', 386, 'CLM', 85),
        ('2023-07-08','CWB', 200, 'PHH', 147),
        ('2023-07-09','CLM', 72, 'PHH', 252),
    ],
    [
        ('2023-07-15','CHC', 173, 'PSO', 163),
        ('2023-07-15','CHC', 81, 'LCC', 208),
        ('2023-07-15','LCC', 176, 'PSO', 175),
        ('2023-07-15','RCR', 145, 'CBB', 132),
    ],
    [
        ('2023-07-29','CLM', 35, 'RCR', 313),
    ],
    [   #WHC
        ('2023-10-21','CWB', 167, 'RCR', 134),
        ('2023-10-21','CBB', 154, 'PHH', 44),
        ('2023-10-21','CBB', 49, 'SLG', 278),
        ('2023-10-21','DGC', 228, 'LCC', 118),
        ('2023-10-21','DIS', 130, 'SDA', 169),
        ('2023-10-21','LCC', 201, 'PIT', 79),
        ('2023-10-22','DIS', 162, 'PHH', 92),
        ('2023-10-22','CWB', 123, 'SDA', 279),
        ('2023-10-22','CWB', 43, 'SLG', 291),
        ('2023-10-22','DGC', 151, 'SLG', 130),
        ('2023-10-22','DGC', 243, 'SDA', 128),
        ('2023-10-22','PIT', 115, 'RCR', 191),
    ],
    #2024
    [   #Dumpster Fire
        ('2024-02-24','CWB', 213, 'PIT', 132),
        ('2024-02-24','CWB', 97, 'MCM', 230),
        ('2024-02-24','LCC', 202, 'PSO', 106),
        ('2024-02-24','LCC', 120, 'MCM', 197),
        ('2024-02-24','PIT', 169, 'PSO', 175),
        ('2024-02-25','CWB', 171, 'PSO', 239),
        ('2024-02-25','CWB', 149, 'LCC', 161),
        ('2024-02-25','LCC', 228, 'PIT', 77),
        #('2024-02-25','MCM', 100, 'PIT', 0), #forfeit
        ('2024-02-25','MCM', 331, 'PSO', 85),
    ],
    [
        ('2024-03-02','CLM', 287, 'PIT(B)', 73),
    ],
    [
        ('2024-03-16','CLM', 125, 'DEM', 226),
        ('2024-03-16','CLM', 123, 'TRD', 208),
        ('2024-03-16','DEM', 192, 'TRD', 160),
    ],
    [
        ('2024-03-23','FLC', 53, 'TOM', 234)
    ],
    [   #BoBH
        ('2024-04-13','PHH', 130, 'CAB', 156),
        ('2024-04-13','CAB', 162, 'AUA', 106),
        ('2024-04-14','PHH', 166, 'TOM', 173),
        ('2024-04-14','TOM', 138, 'AUA', 107),
        ('2024-04-14','CAB', 133, 'TOM', 118),
        ('2024-04-14','PHH', 195, 'AUA', 104),
    ],
    [
        ('2024-04-20','CAB(B)', 124, 'FLC', 227)
    ],
    [   #Salem Slam
        ('2024-04-26','LCC', 135, 'SDA', 110),
        ('2024-04-27','PSO', 133, 'SDA', 176),
        ('2024-04-27','LCC', 334, 'CHC', 101),
        ('2024-04-27','CHC', 105, 'PSO', 241),
        ('2024-04-28','LCC', 187, 'PSO', 111),
        ('2024-04-28','SDA', 312, 'CHC', 95),
    ],
    
    [   #Flat Track Fever
        ('2024-05-10','CHC', 187, 'TOM', 183),
        ('2024-05-11','CHC', 257, 'PSO', 113),
        ('2024-05-12','TOM', 265, 'PSO', 161),        
        ('2024-05-12','CHC', 204, 'TOM', 171),      
    ],
    [   #DOTD
        ('2024-05-11','RCR', 204, 'CBB', 87),
        ('2024-05-11','CWB', 210, 'PIT', 82),
        ('2024-05-11','MCM', 399, 'CBB', 3),
        ('2024-05-11','PIT', 116, 'PHH', 101),
        ('2024-05-11','MCM', 237, 'RCR', 45),
        ('2024-05-11','CWB', 273, 'PHH', 64),
        ('2024-05-12','MCM', 242, 'CWB', 85),
        ('2024-05-12','RCR', 160, 'PIT', 87),
        ('2024-05-12','CBB', 131, 'PHH', 114),
    ],  
    [
        ('2024-06-01','CLM', 159, 'CBB(B)', 152)
    ],
    [   #IHOD-Pt2
        ('2024-06-07','SLG(B)', 212, 'SDA(B)', 159),
#        ('2024-06-07','DGC', 100, 'DIS', 0),
        ('2024-06-07','SLG', 214, 'SDA', 65),
        
        ('2024-06-08','SLG(B)', 149, 'CAB', 233),
        ('2024-06-08','RCR', 120, 'SDA', 240),
        ('2024-06-08','SLG', 179, 'DGC', 115),
        ('2024-06-08','SDA(B)', 110, 'CAB', 266),
        ('2024-06-08','RCR', 169, 'DIS', 151),        
        
        ('2024-06-09','CAB', 122, 'RCR', 233),
        ('2024-06-09','SLG', 323, 'DIS', 57),
        ('2024-06-09','DGC', 287, 'SDA', 88),
    ],
    [
        ('2024-06-15','FLC', 233, 'CLM', 79)
    ],
    [
        ('2024-06-15','RCR', 49, 'SLG', 277)
    ],
    [
        ('2024-06-29','PHH', 186, 'FLC', 124)
    ],
    [
        ('2024-07-06','TRD', 165, 'CLM', 123)
    ],
    
]

team_names = {
    'AUA': 'Austin Anarchy',
    'CWB': 'Carolina Wreckingballs',
    'CAB': 'Casco Bay Roller Derby',
    'CAB(B)': 'Casco Bay B Team',
    'CBB': 'Chicago Bruise Brothers',
    'CBB(B)': 'Chicago B Team',
    'CHC': 'Chinook City Roller Derby',
    'CLM': 'Cleveland Men\'s Roller Derby',
    'DGC': 'Denver Ground Control',
    'DEM': 'Detroit Men\'s Roller Derby',
    'DIS': 'Disorder',
    'FLC': 'Flour City Roller Derby',
    'LCC': 'Lane County Concussion',
    'LCC(B)': 'Lane County B Team',
    'MCM': 'Magic City Misfits',
    'PHH': 'Philadelphia Hooligans',
    'PIT': 'Pittsburgh Roller Derby',
    'PIT(B)': 'Pittsburgh ZomBees',
    'PSO': 'Puget Sound Outcast Derby',
    'RCR': 'Race City Rebels',
    'SDA': 'San Diego Aftershocks',
    'SDA(B)': 'San Diego Tremors',
    'SLG': 'St. Louis Gatekeepers',
    'SLG(B)': 'St. Louis B-Keepers',
    'TRD': 'Terminus Roller Derby',
    'TOM': 'Toronto Men\'s Roller Derby',
    'BOR': 'Borderland Bandits Roller Derby',
    'CTB': 'Crash Test Brummies',
    'DHR': 'DHR Men\'s Roller Derby',
    'KEM': 'Kent Men\'s Roller Derby',
    'MRD': 'Manchester Roller Derby',
    'MRD(B)': 'Manchester B Team',
    'PAN': 'Panam Squad',
    'TIL': 'The Inhuman League',
    'TNF': 'Tyne and Fear Roller Derby',
    'TNF(B)': 'Tyne and Fear B Team',
    'SWS': 'South Wales Silures',
}

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

#for gameday_e in games_e:
#    rank_e.update_ratings(gameday_e)

print("\n")
print("Game count")
t = 0
for team in team_gp_list:
    print(team[0] , len(team_gp_list[t])-1)
    t += 1

team_gp_list = [['AUA'],['CAB'],['CAB(B)'],['CBB'],['CBB(B)'],['CHC'],['CLM'],['CWB'],
                ['DEM'],['DGC'],['DIS'],
                ['FLC'],['LCC'],['LCC(B)'],['PHH'],['PIT'],['PIT(B)'],['PSO'],['MCM'],
                ['RCR'],['SLG'],['SLG(B)'],['SDA'],['SDA(B)'],
                ['TOM'],['TRD']]

for gameday_w in games_w:
    rank_w.update_ratings(gameday_w)

print("\n")
print("Game count")
t = 0
for team in team_gp_list:
    print(team[0] , len(team_gp_list[t])-1)
    t += 1

ratings_e = {team: rank_e.get_rating(team) for team in
             ['BOR', 'CTB', 'KEM', 'MRD', 'MRD(B)', 'TIL', 'TNF', 'TNF(B)', 'SWS']}

ratings_w = {team: rank_w.get_rating(team) for team in
             ['AUA', 'CWB', 'CAB', 'CBB', 'CHC', 'CLM', 'DGC', 'DEM', 'DIS', 'FLC', 'LCC', 'MCM', 'PHH', 'PIT', 'PIT(B)',
              'PSO', 'RCR', 'SDA', 'SLG', 'TRD', 'TOM']}

sorted_ratings_e = sorted(rank_e.ratings.items(), key=lambda item: item[1], reverse=True)
sorted_ratings_w = sorted(rank_w.ratings.items(), key=lambda item: item[1], reverse=True)

print("\n")
print(f"Rankings as of {dateQuery}")
# Print the ratings in a formatted table
print("MRDA West")
print("Position\tTeam\tRating")
position = 1
for code, rating in sorted_ratings_w:
    full_name = team_names.get(code, "Unknown Team")
    print(f"{position}\t{code}\t{rating:.2f}")
    position += 1
print("\n")
print("MRDA East")
print("Position\tTeam\tRating")
position = 1
for code, rating in sorted_ratings_e:
    full_name = team_names.get(code, "Unknown Team")
    print(f"{position}\t{code}\t{rating:.2f}")
    position += 1




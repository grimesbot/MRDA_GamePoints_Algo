# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 10:13:34 2024

@author: shender
"""

from datetime import datetime
from dateutil.relativedelta import relativedelta
import tkinter as tk
from tkinter import simpledialog, ttk
import pprint

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

    def add_team(self, team_name, initial_rating=400):
        if team_name not in self.ratings:
            self.ratings[team_name] = initial_rating

    def set_rating(self, team_name, rating):
        self.ratings[team_name] = rating

    def set_gcount(self, team_name, gcount):
        self.gamecount_active[team_name] = gcount
        
    def compute_gpf(self, team_gp_list, game_d):
        for team in team_gp_list:
            gp = 1
            gcount = 0
            if len(team) > 1:
                exp = 0
                for x in team[1:]:
                    if x[0] < (game_d + relativedelta(months=-12)):
                        continue
                    elif x[0] < (game_d + relativedelta(months=-9)):
                        wt = 0.25
                    else:
                        wt = 1
                    
                    if x[1] != 1:
                        gp_weighted = x[1]**wt
                        gp *= gp_weighted
                        exp += wt
                    
                    power = 1/(exp)
                    gpf = pow(gp, power)
                    self.ratings[team[0]] = gpf
                    
                    gcount += 1
                self.gamecount[team[0]] = gcount

    def update_ratings(self, g):
        for game in g:
            gdate, team_a, score_a, team_b, score_b = game
            self.add_team(team_a)
            self.add_team(team_b)
            
            game_d = datetime.strptime(gdate, '%Y-%m-%d').date()
            
            if game_d > dateQuery:
                continue             

            ra = self.ratings[team_a]
            rb = self.ratings[team_b]

            # Calculate expected scores
            ea = ra/rb
            ea = max(0.33, min(3, ea))
            eb = rb/ra
            eb = max(0.33, min(3, eb))

            if score_a == 0 or score_b == 0:
                # Handle forfeits
                if score_a == 0:
                    for x in team_gp_list:
                        if x[0] == team_b:
                            x.append((game_d, 1))
                if score_b == 0:
                    for x in team_gp_list:
                        if x[0] == team_a:
                            x.append((game_d, 1))
                continue
            
            sa = score_a/score_b
            sa = max(0.33, min(3, sa))
            sb = score_b/score_a
            sb = max(0.33, min(3, sb))
            
            gpa = ra * (sa/ea)
            gpb = rb * (sb/eb)

            for x in team_gp_list:
                if x[0] == team_a:
                    x.append((game_d, gpa))
            for x in team_gp_list:
                if x[0] == team_b:
                    x.append((game_d, gpb))
        
        self.compute_gpf(team_gp_list, game_d)
        
    def get_rating(self, team_name):
        return self.ratings.get(team_name, "Team not found")


def show_team_stats(selected_team):
    team_games = [game for game in games_w if game[1] == selected_team or game[3] == selected_team]
    filtered_games = [game for game in team_games if datetime.strptime(game[0], '%Y-%m-%d').date() >= dateQuery + relativedelta(months=-12)]
    
    # Create a new window for displaying stats
    stats_window = tk.Toplevel()
    stats_window.title(f"{selected_team} Game Stats")

    subtitle = tk.Label(stats_window, text=f"{selected_team} - Number of games in last 12 months: {len(filtered_games)}")
    subtitle.pack()

    # Create the table
    table_frame = ttk.Frame(stats_window)
    table_frame.pack()

    columns = ("Game Date", "GP", "Score A", "Team B", "Score B")
    tree = ttk.Treeview(table_frame, columns=columns, show='headings')
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    for game in filtered_games:
        game_date = game[0]
        team_a = game[1]
        score_a = game[2]
        team_b = game[3]
        score_b = game[4]
        gp = rank_w.gamecount[team_a]  # Adjust this to get the GP as needed

        # Highlight games within the last 9 months
        if datetime.strptime(game_date, '%Y-%m-%d').date() >= dateQuery + relativedelta(months=-9):
            tree.insert("", "end", values=(game_date, gp, score_a, team_b, score_b), tags=("highlight",))
        else:
            tree.insert("", "end", values=(game_date, gp, score_a, team_b, score_b))

    tree.pack()

    # Define a tag for highlighting
    tree.tag_configure("highlight", background="lightgreen")


ROOT = tk.Tk()
ROOT.withdraw()
dateQuery = simpledialog.askstring(title="Date Entry", prompt='Enter ranking date in YYYY-MM-DD format:')
dateQuery = datetime.strptime(dateQuery, '%Y-%m-%d').date()

rank_w = RollerDerbyRanks(initial_ratings_w)

team_gp_list = [['AUA'], ['CAB'], ['CAB(B)'], ['CBB'], ['CBB(B)'], ['CHK'], ['CLG'], ['CWB'],
                ['DEM'], ['DGC'], ['DIS'], ['FLC'], ['CRD'], ['CRD(B)'], ['PHH'], ['PHH(B)'], ['PIT'], ['PIT(B)'], 
                ['PSO'], ['MCM'], ['RCR'], ['SLG'], ['SLG(B)'], ['SDA'], ['SDA(B)'], ['TOM'], ['TRD']]

# Roll through gamedays and compute scores and gpf's as it goes
for gameday_w in games_w:
    if datetime.strptime(gameday_w[0][0], '%Y-%m-%d').date() < dateQuery:
        rank_w.update_ratings(gameday_w)

rank_w.compute_gpf(team_gp_list, dateQuery)

print("\nActive Game count")
pprint.pprint(gamecount_active)

ratings_w = {team: rank_w.get_rating(team) for team in
             ['AUA', 'CWB', 'CAB', 'CBB', 'CHK', 'CLG', 'DGC', 'DEM', 'DIS', 'FLC', 'CRD', 'MCM', 'PHH', 'PHH(B)', 'PIT', 'PIT(B)',
              'PSO', 'RCR', 'SDA', 'SLG', 'TRD', 'TOM']}

sorted_ratings_w = sorted(rank_w.ratings.items(), key=lambda item: item[1], reverse=True)

print("\nRankings as of", dateQuery)
print("MRDA West")
print("Position\tTeam\tGPA")
position = 1
for code, rating in sorted_ratings_w:
    if gamecount_active[code] > 2:
        full_name = team_names.get(code, "Unknown Team")
        print(f"{position}\t{full_name}\t{rating:.2f}") if (gamecount_active[code] > 4 or (code in ['CRD', 'CRD(B)', 'DIS', 'PSO', 'SDA', 'SDA(B)'] and gamecount_active[code] > 2)) else print(f"{position}\t{full_name}*\t{rating:.2f}")
        position += 1
print("\n")

# Team selection window
team_selection_window = tk.Tk()
team_selection_window.title("Select Team")

team_var = tk.StringVar(value="Select a team")
team_dropdown = ttk.Combobox(team_selection_window, textvariable=team_var)
team_dropdown['values'] = team_names.keys()
team_dropdown.pack(padx=20, pady=20)

def on_team_select(event):
    selected_team = team_var.get()
    if selected_team in team_names:
        show_team_stats(selected_team)

team_dropdown.bind("<<ComboboxSelected>>", on_team_select)

team_selection_window.mainloop()
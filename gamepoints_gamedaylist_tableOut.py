# -*- coding: utf-8 -*-
"""
Created on Wed May  1 08:42:51 2024

@author: shender
"""
from datetime import datetime
from dateutil.relativedelta import relativedelta
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import Calendar
import pprint

from GameList import games
from dicts import initial_ratings
from dicts import team_names
from dicts import gamecount_active
from dicts import team_gp_dict

class RollerDerbyRanks:

    def __init__(self, initial_ratings=None):
        self.ratings = initial_ratings if initial_ratings else {}
        self.gamecount = gamecount_active
        #print("set to intial rank")

    def add_team(self, team_name, initial_rating=400):
        if team_name not in self.ratings:
            self.ratings[team_name] = initial_rating

    def set_rating(self, team_name, rating):
        self.ratings[team_name] = rating

    def set_gcount(self, team_name, gcount):
        self.gamecount_active[team_name] = gcount
        
        
    def compute_gpf(self, team_gp_dict, game_d):
        #compute new team score
        for team in team_gp_dict:
            gp = 1
            gcount = 0
            
            if len(team_gp_dict[team]) > 0:
                exp = 0
                for x in team_gp_dict[team]:
                    #print(date_query)
                    delta = (game_d - x[0]).days
                    # print(delta)
                    if delta >= 365: #if x[0][0] < (game_d + relativedelta(months=-12)):
                        #print(game_d, ": game too old")
                        continue
                    elif 183 <= delta < 270: #elif x[0][0] < (game_d + relativedelta(months=-9)):
                        #print(game_d, ": games weighted to 0.25")
                        wt = 0.5
                    elif 271 <= delta < 365: #elif x[0][0] < (game_d + relativedelta(months=-9)):
                        #print(game_d, ": games weighted to 0.25")
                        wt = 0.25
                    #elif x[0] < (game_d + relativedelta(months=-6)):
                    #    wt = 0.5
                    else:
                        wt = 1
                    
                    if x[4] != 1:
                        gp_weighted = x[4]**wt
                        gp *= gp_weighted
                        exp += wt
                    
                    try:
                        power = 1/(exp)
                    except ZeroDivisionError:
                        print(team, "problem with gpf exponent")
                        power = 0
                    
                    gpf = pow(gp,power)
                    #print(game_d,gpf)
                    self.ratings[team] = gpf
                    #if(team=='CAB'):     #Enter a team to track their gpf for troubleshooting. Here it's computed for on every gameday, for each of the games played by THIS team.
                    #     print(x[0],x[4],wt,"current gpf = ",gpf)
                    
                    gcount += 1

                # if(team[0]=='DGC'):     #Enter a team to track their gpf at the end of each gameday (regardless if they played)
                #     print(game_d,x[0],wt,"current gpf = ",gpf)
                self.gamecount[team] = gcount


    def update_ratings(self, g):
        for game in g:
            gdate, team_a, score_a, team_b, score_b = game
            self.add_team(team_a)
            self.add_team(team_b)
            
            game_d = datetime.strptime(gdate,'%Y-%m-%d').date()
            
            if game_d > date_query:
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
        
            # Deal with forfeits. Giving game credit to non-forfeiting team. Not using 100-0 score for now.
            if score_a == 0 or score_b == 0:
                if score_a == 0:
                    # for x in team_gp_list:
                    #     if x[0] == team_b:
                    #         x.append((game_d,1))
                    team_gp_dict[team_b].append((game_d,f"forfeit by {score_a} {team_a}", eb, "-", 1))
                    print(game_d,team_a,ra,"forfeit",team_b,rb,"1")
                if score_b == 0:
                    # for x in team_gp_list:
                    #     if x[0] == team_a:
                    #         x.append((game_d,1))
                    team_gp_dict[team_a].append((game_d,f"forfeit by {team_b}", ea, "-", 1))
                    print(game_d,team_a,ra,"1",team_b,rb,"forfeit")
                continue
            
            # Determine actual scores
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
            gpa = ra * min(3, (sa/ea))
            gpb = rb * min(3, (sb/eb))
            
            #Add game points to game list for each teams.
            # for x in team_gp_list:
            #     if x[0] == team_a:
            #         x.append((game_d,gpa))
            # for x in team_gp_list:
            #     if x[0] == team_b:
            #         x.append((game_d,gpb))
            team_gp_dict[team_a].append((game_d,f"{score_a} vs {score_b} {team_b}", ea, sa, gpa))
            team_gp_dict[team_b].append((game_d,f"{score_b} vs {score_a} {team_a}", eb, sb, gpb))

            if team_a =='BOR' or team_b == 'BOR': #game_d > datetime.strptime("2024-10-07",'%Y-%m-%d').date():
                print(game_d,team_a,score_a, "gpa = ", gpa,team_b,score_b,"gpb = ", gpb)       #Uncomment for game point details
        #print('\n')   
        
        #computescore function!!!
        self.compute_gpf(team_gp_dict, game_d)
        
    def get_rating(self, team_name):
        return self.ratings.get(team_name, "Team not found")

def set_today():
    today = datetime.today().date()
    date_query_var.set(today.strftime('%Y/%m/%d'))

def select_date(event):
    selected_date = cal.get_date()  # Returns a string in 'YYYY-MM-DD'
    date_obj = datetime.strptime(selected_date, '%m/%d/%y')
    formatted_date = date_obj.strftime('%Y/%m/%d')
    date_query_var.set(formatted_date)

def submit_date():
    """Submit the date_query for processing."""
    date_str = date_query_var.get()
    try:
        global date_query
        date_query = datetime.strptime(date_str, '%Y/%m/%d').date()
        root.quit()  # Close the window after submission
        root.destroy()
    except ValueError:
        messagebox.showerror("Invalid Date", "Please select a valid date in YYYY/MM/DD format.")



# Create the main application window
root = tk.Tk()
root.title("Date Selector")

# Create a StringVar to hold the date query
date_query_var = tk.StringVar()

# Create a label to display the date query
date_label = tk.Label(root, textvariable=date_query_var)
date_label.pack(pady=10)

# Create a calendar widget
cal = Calendar(root, selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
cal.pack(pady=10)

# Bind the calendar's date selection to the select_date function
cal.bind("<<CalendarSelected>>", select_date)

# Create a buttons
today_button = tk.Button(root, text="Today", command=set_today)
today_button.pack(pady=5)
submit_button = tk.Button(root, text="Submit", command=submit_date)
submit_button.pack(pady=5)

# Start the main loop
root.mainloop()

print('Date Selected:')
print(date_query)

rank = RollerDerbyRanks(initial_ratings)

#create a list to store the computed gp's. Probably a better way to do this...    
# team_gp_list = [[code] for code in team_names.keys()]

#Roll through gamedays and compute scores and gpf's as it goes
for gameday in games:
    if datetime.strptime(gameday[0][0],'%Y-%m-%d').date() < date_query:
        #print(datetime.strptime(gameday[0][0],'%Y-%m-%d').date())
        rank.update_ratings(gameday)
#compute final gpf for the desired date
rank.compute_gpf(team_gp_dict, date_query)

# print("\n")
# print("Active Game count")
# pprint.pprint(gamecount_active)

ratings = {team: rank.get_rating(team) for team in team_names}

sorted_ratings = sorted(rank.ratings.items(), key=lambda item: item[1], reverse=True)

print("\n")
print(f"Rankings as of {date_query}")
# Print the ratings in a formatted table
print("Position\tTeam\tGPA")
position = 1
for code, rating in sorted_ratings:
    if gamecount_active[code] > 2:
        full_name = team_names.get(code, "Unknown Team")
#        print(f"{position}\t{code}\t{rating:.2f}")
        print(f"{position}\t{full_name}\t{rating:.2f}") if (gamecount_active[code] > 4 or (code in ['CRD','CRD(B)','DIS','PSO','SDA','SDA(B)'] and gamecount_active[code] > 2)) else print(f"{position}\t{full_name}*\t{rating:.2f}")
        position += 1

# Function to populate table based on selected team
def populate_table(selected_team):
    # Clear the table
    for row in tree.get_children():
        tree.delete(row)
    subtitle_label.config(text="")
    count_last_12_months = 0
    
    if selected_team in team_gp_dict:
        for game in team_gp_dict[selected_team]:
            date, summary, expected, actual, gamescore = game
            
            # Determine row color based on date relative to date_query
            delta = (date_query - date).days
            
            if 0 <= delta < 182:  # Within the last 6 months
                color = 'green'
                count_last_12_months += 1
            elif 183 <= delta < 269:  # From 6 to 9 months ago
                color = 'yellow'
                count_last_12_months += 1    
            elif 270 <= delta < 365:  # From 9 to 12 months ago
                color = 'orange'
                count_last_12_months += 1
            elif delta >= 365:  # Older than 12 months
                color = 'red'
            else:
                color = ''  # No highlight

            # Insert row with tag for color
            tree.insert("", "end", values=(date, summary, gamescore), tags=(color,))

    # Apply color styling
    tree.tag_configure('green', background='lightgreen')
    tree.tag_configure('yellow', background='lightyellow')
    tree.tag_configure('orange', background='goldenrod')
    tree.tag_configure('red', background='lightcoral')

    # Update subtitle with the count of games within the last 12 months
    subtitle_label.config(text=f"Number of games within the last 12 months: {count_last_12_months}")
    if gamecount_active[selected_team] != count_last_12_months:
        print("Discrepancy in gamecount for ",selected_team)

# Function to handle dropdown selection
def on_select(event):
    selected_team = team_combobox.get()
    populate_table(selected_team)

# Function to handle window close
def on_close():
    root.quit()
    root.destroy()
    
# Create main application window
root = tk.Tk()
root.title("Team GP Scores")

# Create a dropdown menu for team selection
team_combobox = ttk.Combobox(root, values=list(team_gp_dict.keys()))
team_combobox.set("Select Team")  # Set default value
team_combobox.bind("<<ComboboxSelected>>", on_select)
team_combobox.pack(pady=10)

# Create a label for subtitle
subtitle_label = tk.Label(root, text="", font=("Arial", 12))
subtitle_label.pack(pady=5)

# Create a table to display game scores
tree = ttk.Treeview(root, columns=("Date", "Summary", "GP"), show="headings")
tree.heading("Date", text="Date")
tree.heading("Summary", text="Game Summary")
tree.heading("GP", text="Game Points")
tree.pack(pady=20)

# Set the protocol for window close
root.protocol("WM_DELETE_WINDOW", on_close)

# Start the application
root.mainloop()



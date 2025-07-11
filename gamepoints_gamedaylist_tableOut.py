# -*- coding: utf-8 -*-
"""
Created on Wed May  1 08:42:51 2024

@author: shender
"""
import math
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import Calendar
import mplcursors  # Import mplcursors for interactive annotations

from GameList_history import games
from GamesList_api import games_api
from dicts import initial_ratings
from dicts import team_names
from dicts import gamecount_active
from dicts import team_gp_dict
from dicts import active_forfeits

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
        
    def asymp_ratio(self, numerator, denominator):
        """
        Compute a smoothly limited ratio that asymptotically approaches `limit` and `1/limit`,
        with steeper transition near 1.
        
        Args:
            numerator (float): The numerator of the ratio.
            denominator (float): The denominator of the ratio.
            limit (float): Maximum divergence allowed from 1. Must be > 1.
            steepness (float): Controls how steep the curve is around 1. Higher = sharper transition.
    
        Returns:
            float: A squashed ratio in range [1/limit, limit].
        """
        limit=3.0
        steepness=1
        
        if denominator == 0:
            raise ValueError("Denominator cannot be zero.")
        if limit <= 1:
            raise ValueError("Limit must be greater than 1.")
        if steepness <= 0:
            raise ValueError("Steepness must be positive.")
        
        raw_ratio = numerator / denominator
        log_ratio = math.log(raw_ratio)
        
        # Increase steepness by scaling input to tanh
        squashed_log = math.tanh(steepness * log_ratio) * math.log(limit)
        
        return math.exp(squashed_log)

    def compute_gpf(self, team_gp_dict, game_d):
        #compute new team score
        for team in team_gp_dict:
            gp = 1
            gcount = 0
            z=0
            if len(team_gp_dict[team]) > 0:
                exp = 0
                for x in team_gp_dict[team]:
                    #print(date_query)
                    delta = (game_d - x[0]).days
                    if delta >= 365: #if x[0][0] < (game_d + relativedelta(months=-12)):
                        #print(game_d, ": game too old")
                        z+=1
                        continue
                    elif 273 <= delta < 365: #elif x[0][0] < (game_d + relativedelta(months=-9)):
                        #print(game_d, ": games weighted to 0.25")
                        wt = 0.25
                    elif 182 <= delta < 272: #elif x[0][0] < (game_d + relativedelta(months=-9)):
                        #print(game_d, ": games weighted to 0.25")
                        wt = 0.5
                    #if x[0].year < date_query.year:  
                    #    wt = 0.1
                    else:
                        wt = 1  

                    if x[4] != 1:
                        gp_weighted = x[4]**wt
                        gp *= gp_weighted
                        exp += wt
                    
                    try:
                        power = 1/(exp)
                    except ZeroDivisionError:
                        #print(team, "problem with gpf exponent")
                        power = 0
                    
                    gpf = pow(gp,power)
                    
                    if len(team_gp_dict[team][z]) == 5:
                        team_gp_dict[team][z].append(gpf)
                    z += 1
                    #if(team=='DGC'):     #Enter a team to track their gpf for troubleshooting. Here it's computed for on every gameday, for each of the games played by THIS team.
                        #print("gameday = ",x[0], game_d.year, "gp = ", x[4],"wt = ", wt,"current gpf = ",gpf)
                        #print(game_d.year, date_query.year)
                    self.ratings[team] = gpf
                    
                    #Count games for ranking and post season elligibility. Exclude Champs games. This will fail IF other games are played on the same days as champs
                    #P&P: Qualifier games shouldn't count after 9 months. Champs after 6 months...
                    champs_dates = {date(2024, 10, 11), date(2024, 10, 12), date(2024, 10, 13)}
                    if x[0] not in champs_dates:
                        gcount += 1

                # if(team=='DGC'):     #Enter a team to track their gpf at the end of each gameday (regardless if they played)
                #     print(game_d,x[0],"current gpf = ",gpf)
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
            # ea = ra/rb
            # if ea < 0.33:
            #     ea = 0.33
            # if ea > 3:
            #     ea = 3
            ea = self.asymp_ratio(ra,rb)
            
            eb = rb/ra
            # if eb < 0.33:
            #     eb = 0.33
            # if eb > 3:
            #     eb = 3
            eb = self.asymp_ratio(rb,ra)
        
            # Deal with forfeits. Giving game credit to non-forfeiting team. Not using 100-0 score for now.
            #This has been dealt with in the score import code, but leaving here for now.
            if (score_a == 0 and score_b in (100, 250)) or (score_a in (100, 250) and score_b == 0) or (score_a == 0 and score_b == 0):
                if (score_a == 0 and score_b in (100, 250)):
                    team_gp_dict[team_b].append(list((game_d,f"forfeit by {team_a}", eb, "-", 1)))
                    if game_d > (date_query - relativedelta(months=12)):
                        active_forfeits[team_a] += 1
                    #print(game_d,team_a,ra,"forfeit",team_b,rb,"1")
                if (score_a in (100, 250) and score_b == 0):
                    team_gp_dict[team_a].append(list((game_d,f"forfeit by {team_b}", ea, "-", 1)))
                    if game_d > (date_query - relativedelta(months=12)):
                        active_forfeits[team_b] += 1
                    #print(game_d,team_a,ra,"1",team_b,rb,"forfeit")
                if (score_a == 0 and score_b == 0):
                    print(game_d," 0-0 score reported. MRDA Central problem?")
                continue
            
            # Determine actual scores
            # sa = score_a/score_b
            # if sa < 0.33:
            #     sa = 0.33
            # if sa > 3:
            #     sa = 3
            sa = self.asymp_ratio(score_a,score_b)
            # sb = score_b/score_a
            # if sb < 0.33:
            #     sb = 0.33
            # if sb > 3:
            #     sb = 3
            sb = self.asymp_ratio(score_b,score_a)
            
            #Game points:
            gpa = ra * max(0.33, min(3, sa/ea))
            gpb = rb * max(0.33, min(3, sb/eb))
            
            #Add game points to game list for each teams.
            # for x in team_gp_list:
            #     if x[0] == team_a:
            #         x.append((game_d,gpa))
            # for x in team_gp_list:
            #     if x[0] == team_b:
            #         x.append((game_d,gpb))
            team_gp_dict[team_a].append(list((game_d,f"{score_a} vs {score_b} {team_b}", ea, sa, gpa)))
            team_gp_dict[team_b].append(list((game_d,f"{score_b} vs {score_a} {team_a}", eb, sb, gpb)))

            if team_a =='TNF' or team_b == 'TNF': #game_d > datetime.strptime("2024-10-07",'%Y-%m-%d').date():
               print(game_d, team_a, score_a, ea, sa, team_b, score_b, eb, sb)       #Uncomment for game point details
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

#Combine the games from both sources
games.extend(games_api)

#Roll through gamedays and compute scores and gpf's as it goes
for gameday in games:
    if datetime.strptime(gameday[0][0],'%Y-%m-%d').date() < date_query:
        #print(datetime.strptime(gameday[0][0],'%Y-%m-%d').date())
        rank.update_ratings(gameday)
        
        
#compute final gpf for the desired date
rank.compute_gpf(team_gp_dict, date_query)

ratings = {team: rank.get_rating(team) for team in team_names}

sorted_ratings = sorted(rank.ratings.items(), key=lambda item: item[1], reverse=True)

#position = 1
# for code, rating in sorted_ratings:
#     if gamecount_active[code] > 2:
#         full_name = team_names.get(code, "Unknown Team")
# #        print(f"{position}\t{code}\t{rating:.2f}")
#         gamecount=gamecount_active[code]
#         print(f"{position}\t{full_name}\t{rating:.2f}\t{gamecount}") if (gamecount > 4 or (code in ['CRD','CRD(B)','DIS','PSO','SDA','SDA(B)'] and gamecount > 2)) else print(f"{position}\t{full_name}*\t{rating:.2f}\t{gamecount}")
#         position += 1
#     else:
#         full_name = team_names.get(code, "Unknown Team")
#         gamecount=gamecount_active[code]
#         unranked.append((full_name,gamecount))

#Create final ranking table and apply forfeit penalties
# Step 1: Build the list of eligible teams sorted by rating
eligible_teams = []
unranked = []
for code, rating in sorted_ratings:
    if gamecount_active[code] > 2:
        eligible_teams.append({
            'code': code,
            'name': team_names.get(code, "Unknown Team"),
            'rating': rating,
            'gamecount': gamecount_active[code],
            'forfeits': active_forfeits.get(code, 0)
        })
    else:
        full_name = team_names.get(code, "Unknown Team")
        gamecount=gamecount_active[code]
        unranked.append((full_name,gamecount))
        
# Step 2: Apply penalty as actual positional shifts
final_list = eligible_teams.copy()
for i in range(len(eligible_teams)):
    team = eligible_teams[i]
    penalty = team['forfeits'] * 2
    if penalty == 0:
        continue

    # Calculate new position, can't go beyond end
    new_pos = min(i + penalty, len(final_list) - 1)

    # Remove and re-insert at new position
    final_list.remove(team)
    final_list.insert(new_pos, team)

# Step 3: Print the final list
print("\n")
print(f"Rankings as of {date_query}")
print("Position\tTeam\tGPA\tGames Played\tPenalty")
for position, team in enumerate(final_list, start=1):
    code = team['code']
    name = team['name']
    rating = team['rating']
    gamecount = team['gamecount']
    penalty = team['forfeits'] * 2

    star = "*" if (gamecount <= 4 and code not in ['CRD','CRD(B)','DIS','PSO','SDA','SDA(B)']) else ""
    print(f"{position}\t{name}{star}\t{rating:.2f}\t{gamecount}\t{penalty}")
    

sorted_unranked = sorted(unranked)
print("\n")
print("Unranked Teams")        
for team, number in sorted_unranked:
    print(f"{team} {number}")


def plot_team_games(team_code, team_gp_dict, team_names):
    """Display a plot for the selected team's games below its row."""
    global open_plot_window
    if team_code not in team_gp_dict:
        messagebox.showerror("Error", f"No game data available for {team_names.get(team_code, 'Unknown Team')} ({team_code}).")
        return

    # Extract game data
    games = team_gp_dict[team_code]
    if not games:
        messagebox.showerror("Error", f"No games listed for {team_names.get(team_code, 'Unknown Team')} ({team_code}).")
        return
    
    # Create a new independent window for each team plot
    window = tk.Toplevel()
    window.title(f"Game Data for {team_names.get(team_code, 'Unknown Team')} ({team_code})")
    window.geometry("700x1000")

    dates = [game[0] for game in games]
    gps = [game[4] for game in games]
    gpfs = [game[5] for game in games]

    # Create a matplotlib figure
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(dates, gps, linestyle='', marker='o', color='blue', label="GP")
    ax.plot(dates, gpfs, linestyle='--', color='green', label="GPA")    
    ax.set_title(f"Gamepoints Over Time for {team_names.get(team_code, 'Unknown Team')} ({team_code})")
    fig.suptitle(f"Current GPA for {team_names.get(team_code, 'Unknown Team')} = {ratings.get(team_code):#6.2f}")
    ax.set_xlabel("Date")
    ax.set_ylabel("GP / GPA")
    ax.grid(True)
    ax.legend()

    # Add hover interaction using mplcursors
    cursor = mplcursors.cursor(ax.scatter(dates,gps,color='blue'), hover=True)
    @cursor.connect("add")
    def on_hover(sel):
        idx = int(sel.index)  # Cast to int
        game = games[idx]
        date, score, exp_ratio, actual_ratio, gpa, gpf = game
        sel.annotation.set_text(f"Date: {date}\n Score: {score}\n GP: {gpa:#6.2f}\n GPA at EOD: {gpf:#6.2f}")

    # Embed the plot in the window
    canvas = FigureCanvasTkAgg(fig, master=window) #open_plot_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    plt.close(fig)

    # Create a frame for the table
    table_frame = ttk.Frame(window) #open_plot_window)
    table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    # Create the table (Treeview)
    columns = ("Date", "Score", "Expected Ratio", "Actual Ratio", "Gamepoints")
    game_table = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)

    # Define column headers
    for col in columns:
        game_table.heading(col, text=col)
        game_table.column(col, anchor="center", width=100)

    # Insert game data into the table
    for game in games[::-1]:
        date, score, exp_ratio, actual_ratio, gpa, gpf = game
        actual_ratio_display = f"{actual_ratio:.2f}" if isinstance(actual_ratio, (int, float)) else actual_ratio
        game_table.insert("", "end", values=(date, score, f"{exp_ratio:.2f}", actual_ratio_display, f"{gpa:.3f}"))

    game_table.pack(fill=tk.BOTH, expand=True)


def on_team_select(event, tree, team_gp_dict, team_names):
    """Handle the event when a team is selected and open a new plot window."""
    # global open_plot_window

    selected_item = tree.selection()
    if not selected_item:
        return

    selected_code = tree.item(selected_item, "values")[1]

    plot_team_games(selected_code, team_gp_dict, team_names)


def show_rankings(final_list, team_names, gamecount_active, date_query, team_gp_dict):
    import tkinter as tk
    from tkinter import ttk

    # Create a new window
    root = tk.Tk()
    root.title(f"Rankings as of {date_query}")

    # Maximize the window
    screen_width = 700 #root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()-75
    root.geometry(f"{screen_width}x{screen_height}")

    root.grid_rowconfigure(0, weight=5)
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # --- Ranked Teams Frame ---
    ranked_frame = ttk.Frame(root)
    ranked_frame.grid(row=0, column=0, sticky="nsew")

    ranked_scrollbar = ttk.Scrollbar(ranked_frame)
    ranked_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    tree = ttk.Treeview(
        ranked_frame,
        columns=("Rank", "Code", "Team", "GPA", "Games"),
        show="headings",
        yscrollcommand=ranked_scrollbar.set
    )
    tree.column("Rank", width=50, anchor=tk.CENTER)
    tree.column("Code", width=50, anchor=tk.CENTER)
    tree.column("Team", width=200, anchor=tk.W)
    tree.column("GPA", width=80, anchor=tk.CENTER)
    tree.column("Games", width=50, anchor=tk.CENTER)
    tree.pack(fill=tk.BOTH, expand=True)
    ranked_scrollbar.config(command=tree.yview)

    for col in ("Rank", "Code", "Team", "GPA", "Games"):
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.CENTER)

    position = 1
    for team in final_list:
        if team['gamecount'] > 2:
            tree.insert("", "end", values=(position, team['code'], team['name'], f"{team['rating']:.2f}", team['gamecount']))
            position += 1

    tree.bind("<<TreeviewSelect>>", lambda event: on_team_select(event, tree, team_gp_dict, team_names))

    # --- Unranked Teams Frame ---
    unranked_frame = ttk.LabelFrame(root, text="Unranked Teams")
    unranked_frame.grid(row=1, column=0, sticky="nsew")

    unranked_scrollbar = ttk.Scrollbar(unranked_frame)
    unranked_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    unranked_tree = ttk.Treeview(
        unranked_frame,
        columns=("Rank", "Code", "Team", "GPA", "Games"),
        show="headings",
        yscrollcommand=unranked_scrollbar.set
    )
    unranked_tree.column("Rank", width=50, anchor=tk.CENTER)
    unranked_tree.column("Code", width=50, anchor=tk.CENTER)
    unranked_tree.column("Team", width=200, anchor=tk.W)
    unranked_tree.column("GPA", width=80, anchor=tk.CENTER)
    unranked_tree.column("Games", width=50, anchor=tk.CENTER)

    unranked_tree.pack(fill=tk.BOTH, expand=True)
    unranked_scrollbar.config(command=unranked_tree.yview)

    for col in ("Rank", "Code", "Team", "GPA", "Games"):
        unranked_tree.heading(col, text=col)
        unranked_tree.column(col, anchor=tk.CENTER)

    for team in final_list:
        if team['gamecount'] <= 2:
            unranked_tree.insert("", "end", values=(position, team['code'], team['name'], f"{team['rating']:.2f}", team['gamecount']))

    unranked_tree.bind("<<TreeviewSelect>>", lambda event: on_team_select(event, unranked_tree, team_gp_dict, team_names))

    root.mainloop()


# Display rankings with clickable teams
show_rankings(final_list, team_names, gamecount_active, date_query, team_gp_dict)

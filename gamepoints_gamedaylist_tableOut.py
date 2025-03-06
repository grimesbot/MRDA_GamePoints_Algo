# -*- coding: utf-8 -*-
"""
Created on Wed May  1 08:42:51 2024

@author: shender
"""
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import Calendar
import mplcursors  # Import mplcursors for interactive annotations

from GameList import games
from dicts import initial_ratings
from dicts import team_names
from dicts import gamecount_active
from dicts import team_gp_dict

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
                    # print(delta)
                    if delta >= 365: #if x[0][0] < (game_d + relativedelta(months=-12)):
                        #print(game_d, ": game too old")
                        z+=1
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
                    
                    if len(team_gp_dict[team][z]) == 5:
                        team_gp_dict[team][z].append(gpf)
                    z += 1
                    #if(team=='CAB'):     #Enter a team to track their gpf for troubleshooting. Here it's computed for on every gameday, for each of the games played by THIS team.
                    #     print(x[0],x[4],wt,"current gpf = ",gpf)
                    self.ratings[team] = gpf
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
                    team_gp_dict[team_b].append(list((game_d,f"forfeit by {score_a} {team_a}", eb, "-", 1)))
                    print(game_d,team_a,ra,"forfeit",team_b,rb,"1")
                if score_b == 0:
                    # for x in team_gp_list:
                    #     if x[0] == team_a:
                    #         x.append((game_d,1))
                    team_gp_dict[team_a].append(list((game_d,f"forfeit by {team_b}", ea, "-", 1)))
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
            team_gp_dict[team_a].append(list((game_d,f"{score_a} vs {score_b} {team_b}", ea, sa, gpa)))
            team_gp_dict[team_b].append(list((game_d,f"{score_b} vs {score_a} {team_a}", eb, sb, gpb)))

            #if team_a =='BOR' or team_b == 'BOR': #game_d > datetime.strptime("2024-10-07",'%Y-%m-%d').date():
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
unranked = []
for code, rating in sorted_ratings:
    if gamecount_active[code] > 2:
        full_name = team_names.get(code, "Unknown Team")
#        print(f"{position}\t{code}\t{rating:.2f}")
        print(f"{position}\t{full_name}\t{rating:.2f}") if (gamecount_active[code] > 4 or (code in ['CRD','CRD(B)','DIS','PSO','SDA','SDA(B)'] and gamecount_active[code] > 2)) else print(f"{position}\t{full_name}*\t{rating:.2f}")
        position += 1
    else:
        full_name = team_names.get(code, "Unknown Team")
        unranked.append(full_name)

sorted_unranked = sorted(unranked)
print("\n")
print("Unranked Teams")        
print("\n".join(sorted_unranked))


open_plot_window = None


def plot_team_games(team_code, team_gp_dict, team_names):
    """Display a plot for the selected team's games below its row."""
    global open_plot_window
    if team_code not in team_gp_dict:
        messagebox.showerror("Error", f"No game data available for {team_names.get(team_code, 'Unknown Team')} ({team_code}).")
        return

    # Extract game data
    games = team_gp_dict[team_code]
    if not games:
        messagebox.showerror("Error", f"No game data available for {team_names.get(team_code, 'Unknown Team')} ({team_code}).")
        return

    # Close the previous plot window if it exists
    if open_plot_window is not None:
        open_plot_window.destroy()
    
    # Create a new window for the plot
    open_plot_window = tk.Toplevel()
    open_plot_window.title(f"Game Data for {team_names.get(team_code, 'Unknown Team')} ({team_code})")
    open_plot_window.geometry("700x1000")
    
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
    canvas = FigureCanvasTkAgg(fig, master=open_plot_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Create a frame for the table
    table_frame = ttk.Frame(open_plot_window)
    table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    # Create the table (Treeview)
    columns = ("Date", "Score", "Expected Ratio", "Actual Ratio", "Gamepoints")
    game_table = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)

    # Define column headers
    for col in columns:
        game_table.heading(col, text=col)
        game_table.column(col, anchor="center", width=100)

    # Insert game data into the table
    for game in games:
        date, score, exp_ratio, actual_ratio, gpa, gpf = game
        actual_ratio_display = f"{actual_ratio:.2f}" if isinstance(actual_ratio, (int, float)) else actual_ratio
        game_table.insert("", "end", values=(date, score, f"{exp_ratio:.2f}", actual_ratio_display, f"{gpa:.3f}"))

    game_table.pack(fill=tk.BOTH, expand=True)

    # Add a scrollbar
    # scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=game_table.yview)
    # game_table.configure(yscroll=scrollbar.set)
    # scrollbar.pack(side="right", fill="y")

    # Add a close button
    # close_button = ttk.Button(open_plot_window, text="Close", command=open_plot_window.destroy)
    # close_button.pack(pady=5)


def on_team_select(event, tree, team_gp_dict, team_names):
    """Handle the event when a team is selected and open a new plot window."""
    global open_plot_window

    selected_item = tree.selection()
    if not selected_item:
        return

    selected_code = tree.item(selected_item, "values")[1]

    # If the currently open plot window is for the same team, close it
    if open_plot_window is not None and open_plot_window.wm_title().endswith(f"({selected_code})"):
        open_plot_window.destroy()
        open_plot_window = None
    else:
        plot_team_games(selected_code, team_gp_dict, team_names)


def show_rankings(sorted_ratings, team_names, gamecount_active, date_query, team_gp_dict):
    # Create a new window
    root = tk.Tk()
    root.title(f"Rankings as of {date_query}")

    # Create a Treeview widget
    tree = ttk.Treeview(root, columns=("Rank", "Code", "Team", "GPA"), show="headings", height=len(sorted_ratings))
    tree.pack(fill=tk.BOTH, expand=True)

    # Define the columns
    tree.heading("Rank", text="Rank")
    tree.heading("Code", text="Code")
    tree.heading("Team", text="Team")
    tree.heading("GPA", text="GPA")

    tree.column("Rank", width=50, anchor=tk.CENTER)
    tree.column("Code", width=50, anchor=tk.CENTER)
    tree.column("Team", width=200, anchor=tk.CENTER)
    tree.column("GPA", width=100, anchor=tk.CENTER)

    # Populate the Treeview with the sorted ratings
    position = 1
    for code, rating in sorted_ratings:
        if gamecount_active[code] > 2:  # Include only ranked teams
            full_name = team_names.get(code, "Unknown Team")
            tree.insert("", "end", values=(position, code, full_name, f"{rating:.2f}"))
            position += 1

    # Bind the Treeview selection to display a plot
    tree.bind("<<TreeviewSelect>>", lambda event: on_team_select(event, tree, team_gp_dict, team_names))

    root.mainloop()


# Display rankings with clickable teams
show_rankings(sorted_ratings, team_names, gamecount_active, date_query, team_gp_dict)

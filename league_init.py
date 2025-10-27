# Initate League 
from padelLeague import padelLeague
# from Bin.PadelLeagueTables import PadelLeagueTables
import pyperclip
import pickle
from datetime import date
import os
import random


# === League Parameters ===
# Teams and players 
teams_and_players = {
    "Sets in the City": ['Joe', 'Callum'],
    "That's A Paddlin'": ['David C', 'Garbhan'],
    "Player? I hardly know her": ['Odhran', 'Lee'],
    "Cheaper by the Counsin'": ['Luke', 'Colm'],
    "Armaghgeddon": ['Michael', 'Curtis'],
    "Slim Reapers": ['Eamonn', 'Conor'], 
    "Rose and Crown Padel Club": ['Jack', 'Cahal'],
    "The Binge Drinkers": ['David T', 'James'],
    "The Receptionists": ['Victoria', 'Sarah'],
    # "Newry Heads": ['Aaron', 'Jamie']
}

players = [player for team in teams_and_players.values() for player in team]

# Teams
teams = list(teams_and_players.keys())

# Define league start date and init date
league_start_date = "2025-10-12"
league_init_date = date.today().strftime("%Y-%m-%d")

# ==== LEAGUE INITIALISATION ====
# Fucntion to an unique league schedule
def round_robin(teams_and_players, teams):
    teams_with_bye = teams.copy()
    if len(teams) % 2:
        teams_with_bye.append("BYE")
    schedule = []
    n = len(teams_with_bye)
    fixtures = list(range(n))
    for _ in range(n-1):
        week = []
        for i in range(n // 2):
            t1 = teams_with_bye[fixtures[i]]
            t2 = teams_with_bye[fixtures[n - 1 - i]]
            if t1 != "BYE" or t2 != "BYE":
                week.append((t1, t2))
        fixtures = fixtures[:1] + fixtures[-1:] + fixtures[1:-1]
        schedule.append(week)
    return schedule

# Initate League by defining scehdule 
schedule = round_robin(teams_and_players, teams)

# === Save Schedule with unqiue identifier ===
# Create a unique folder name using league start and init dates
unique_folder = f"league_{league_start_date}_init_{league_init_date}"
unique_folder_reports = f"{unique_folder}\\League Reports"
unique_folder_report_images = f"{unique_folder}\\Report Images"
os.makedirs(unique_folder, exist_ok=True)
os.makedirs(unique_folder_reports, exist_ok=True)
os.makedirs(unique_folder_report_images, exist_ok=True)

# Define file paths inside the unique folder
unique_schedule_filename = os.path.join(unique_folder, "league_schedule.pkl")
unique_teams_filename = os.path.join(unique_folder, "teams.pkl")

with open(unique_schedule_filename, 'wb') as file:
    pickle.dump(schedule, file)

with open(unique_teams_filename, 'wb') as file:
    pickle.dump(teams_and_players, file)

# === Create Script for League Management ===

# def generate_blank_record_match_code(self, weeks=None):
"""
Copies blank EBLeagueTables.record_match lines for all scheduled games to the clipboard.
If weeks is None, does all weeks. Otherwise, provide a list of week numbers.
"""

week_range = range(1, len(schedule) + 1)
lines = []
for week_num in week_range:
    lines.append(f"# Week {week_num}")
    lines.append(f"if {week_num-1} < st.session_state.weeks_complete:")
    for match in schedule[week_num - 1]:
        if "BYE" in match:
            continue
        team1, team2 = match
        lines.append(f'   st.session_state.League.record_match("{team1}", "{team2}", [(4 ,2 ), (2 ,4 ), (4 , 1)])')
    lines.append("")  # Blank line between weeks
output = "\n".join(lines)
pyperclip.copy("")
pyperclip.copy(output)

with open(os.path.join(unique_folder, "record_games.py"), "a", encoding="utf-8") as f:
    f.write(pyperclip.paste())
    f.write("\n")  # Add a newline for separation



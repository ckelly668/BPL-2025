# League Has Been Initialised already now to load the schedule and teams
import os
import pickle
from datetime import date
import pyperclip
from padelLeague import padelLeague
import matplotlib.image as img
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from pdf2image import convert_from_path
from PIL import Image


#  === Load Teams and Schedule ===
# Define Unique Identifiers for the league
# league_start_date = "2025-10-12"
# league_init_date = "2025-10-02"
league_start_date = "2025-10-12"
league_init_date = "2025-10-07"

# Get the number of weeks completed from user input as an integer
weeks_complete = int(input("Enter the number of weeks completed: "))

# Define File Names Strings
unique_folder = f"league_{league_start_date}_init_{league_init_date}"
unique_folder_reports = f"{unique_folder}\\League Reports"
unique_folder_report_images = f"{unique_folder}\\Report Images"
unique_schedule_filename = os.path.join(unique_folder, "league_schedule.pkl")
unique_teams_filename = os.path.join(unique_folder, "teams.pkl")
logo_filename = os.path.join("images/padel_logo_2.png")

# Initate League by checking if the unique folder exists
if not os.path.exists(unique_folder):
    print("League not initialised. Please run 'league_init.py' to set up the league.")
    # exec(open("league_init.py").read())
# Load the schedule and teams from the unique files
with open(unique_schedule_filename, 'rb') as file:
    schedule = pickle.load(file)

with open(unique_teams_filename, 'rb') as file:
    teams_and_players = pickle.load(file)

# === Create PadelLeagueTables Class ===
League = padelLeague(teams_and_players,
                                  startdate=league_start_date, 
                                  schedule=schedule)
# print(type(League.get_players('Smashers')))
# === Record Matches ===
# This section runs from 'record_games.py' to record the matches for each week.
exec(open(os.path.join(unique_folder, "record_games.py")).read())

# === Generate League Table ===
from aesthetic_tables import create_league_table, create_weekly_schedule_table, create_weekly_results_table, create_winners_page

fig_league_table = create_league_table(League.build_league_table_from_matrix())

if weeks_complete < len(League.get_teams()):
    fig_schedule = create_weekly_schedule_table(League, week = weeks_complete+1)
    # === Save Figures to PDF ===
    if weeks_complete != 0:
        fig_results = create_weekly_results_table(League, week = weeks_complete)
        figs = [fig_league_table, fig_results, fig_schedule]
    else:

        figs = [fig_league_table, fig_schedule]
else:
    fig_results = create_weekly_results_table(League, week = weeks_complete)
    # Create a Congratualtions figure for the winng team without function
    fig_winning_team = create_winners_page(League.build_league_table_from_matrix())  
    # print(f"Congratulations to {winning_team.iloc[0]['Team']} for winning the league!")
    figs = [fig_league_table, fig_results, fig_winning_team]

from matplotlib.backends.backend_pdf import PdfPages
with PdfPages(os.path.join(unique_folder_reports, f"Week {weeks_complete} Report.pdf")) as pdf:
    for fig in figs:
        pdf.savefig(fig, bbox_inches='tight') 

# Create single image
pages = convert_from_path(os.path.join(unique_folder_reports, f"Week {weeks_complete} Report.pdf"), 500)

image0_size = pages[0].size
image1_size = pages[1].size
if len(pages) > 2:
    image2_size = pages[2].size
    new_image = Image.new("RGB",(image0_size[0], image0_size[1]+image1_size[1]+image2_size[1]), (250,250,250))
    new_image.paste(pages[2],(0,image0_size[1]+image1_size[1]))
else:
    new_image = Image.new("RGB",(image0_size[0], image0_size[1]+image1_size[1]), (250,250,250))

new_image.paste(pages[0],(0,0))
new_image.paste(pages[1],(0,image0_size[1]))

new_image.save(os.path.join(unique_folder_report_images, f"Padel Week {weeks_complete}.jpg"))




reports_completed = len([name for name in os.listdir(unique_folder_reports)])

if reports_completed == (len(League.get_teams())+1):
    schedules = {}
    for i in range(reports_completed):

        pages = convert_from_path(os.path.join(unique_folder_reports, f"Week {i} Report.pdf"), 500)
        schedules[i] = pages[len(pages)-1]
    image_size = schedules[0].size
    one_img_schedule = Image.new("RGB",(image_size[0], (len(schedules)-1)*image_size[1]), (250,250,250))
    for i in range(len(schedules)-1):
        one_img_schedule.paste(schedules[i],(0,i*image_size[1]))
    one_img_schedule.save(os.path.join(unique_folder_report_images, f"Full Schedule.jpg"))

# print(f"Congratulations to {League.build_league_table_from_matrix().iloc[0]['Team']} for winning the league!")



# Using subprocess to open the PDF report
import webbrowser
pdf_path = os.path.join(unique_folder_reports, f"Week {weeks_complete} Report.pdf")
# webbrowser.open_new(pdf_path)
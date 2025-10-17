import streamlit as st
import os
import pickle
from padelLeague import padelLeague

def init_session():
    # if 'a' not in st.session_state:
    #     st.session_state.a = 1
    if 'weeks_complete' not in st.session_state:
        st.session_state['weeks_complete'] = 2
        #  =========== Load Teams and Schedule ==============
        # Define Unique Identifiers for the league
        league_start_date = "2025-10-12"
        league_init_date = "2025-10-07"

        # Define File Names Strings
        unique_folder = f"league_{league_start_date}_init_{league_init_date}"
        # unique_folder_reports = f"{unique_folder}\\League Reports"
        # unique_folder_report_images = f"{unique_folder}\\Report Images"
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

        # =========== Create PadelLeagueTables Class ==============
        League = padelLeague(teams_and_players,
                            startdate=league_start_date, 
                            schedule=schedule)
        
        st.session_state.League = League
        st.session_state.unique_folder = unique_folder
        st.session_state.schedule = schedule

        
        # ============== Get Match Records Matches ==============
        # This section runs from 'record_games.py' to record the matches for each week.
        exec(open(os.path.join(st.session_state.unique_folder , "record_games.py")).read())

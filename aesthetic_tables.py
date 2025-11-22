import pandas as pd
# from league_init import league_table
from pathlib import Path
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import matplotlib.image as image
import matplotlib.lines as mlines

import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from PIL import Image

from plottable import ColumnDefinition, Table
from plottable.cmap import normed_cmap
from plottable.plots import circled_image #image
from fpdf import FPDF
import datetime
from datetime import timedelta

# ============= STYLE SETTINGS =============
row_colors = {
        "top4": "#509b9b",
        "top6": "#516362",
        "playoffs": "#8d9386",
        "relegation": "#c8ab8d",
        "even": "#627979",
        "odd": "#68817e",
    }


logo_navy = "#273450"
logo_yellow = '#f4c949'
logo_grey = '#424141'

row_colors = {
        "top4": "#273450",
        "top6": "#616B81",
        "playoffs": "#b7a262",
        "relegation": "#f4c949",
        "even": "#686B72",
        "odd": "#616B81",
    }

bg_color = logo_grey #row_colors["odd"]
text_color = "#e0e8df"

def create_league_table(league_table):
    global row_colors, bg_color, text_color, col_defs

    # Define column definitions for creating the table with specific properties.
    col_defs = (
        [

            ColumnDefinition(
                name="Team",
                textprops={"ha": "left", "weight": "bold"},
                width=2.9,
            ),
             ColumnDefinition(
                name="Players",
                textprops={"ha": "left", "weight": "normal", "fontsize": 11},
                width=1.2,
            ),
            ColumnDefinition(
                name="Games Played",
                textprops={"ha": "center"},
                width=0.75,
            ),
            ColumnDefinition(
                name="Wins",
                textprops={"ha": "center"},
                width=0.75,
            ),
            ColumnDefinition(
                name="Losses",
                textprops={"ha": "center"},
                width=0.75,
            ),
            ColumnDefinition(
                name="Points",
                width=0.75,
                textprops={"ha": "center", "weight": "bold"},
            ),
            ColumnDefinition(
                name="Sets For",
                width=1.1,
                textprops={
                    "ha": "center", "fontsize": 14},
                group="Sets",
            ),
            ColumnDefinition(
                name="Sets Against",
                width=1.1,
                textprops={
                    "ha": "center", "fontsize": 14},
                group="Sets",
            ),
            ColumnDefinition(
                name="Games For",
                width=1.1,
                textprops={
                    "ha": "center", "fontsize": 14},
                group="Games",
            ),
            ColumnDefinition(
                name="Games Against",
                width=1.2,
                textprops={
                    "ha": "center", "fontsize": 14},
                group="Games",
            ),
        ])

    # Setting font for text rendering to "DejaVu Sans" and adjust the figure's bounding box to be "tight."
    plt.rcParams["font.family"] = ["DejaVu Sans"]
    # plt.rcParams["savefig.bbox"] = "tight"
    plt.rcParams["text.color"] = text_color
    # plt.rcParams["font.family"] = "Roboto"

    # Build the league table from your results matrix
    # league_table = build_league_table_from_matrix(results_matrix, points_per_win=3)
    league_table = league_table.set_index("Team")

    # print(league_table)
    # Import image
    # with cbook.get_sample_data("images\\padel_logo_2_small.png") as file:
    #     im = image.imread(file)
    # Create Table
    fig, ax = plt.subplots(figsize=(21, league_table.shape[0]+1))

    fig.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    table = Table(
        league_table,
        column_definitions=col_defs,
        row_dividers=True,
        col_label_divider=True,
        footer_divider=True,
        # index_col="Team",
        columns=league_table.columns,
        odd_row_color=row_colors["even"],
        # header_divider_kw={"color": logo_yellow, "lw": 2},
        footer_divider_kw={"color": bg_color, "lw": 2},
        row_divider_kw={"color": bg_color, "lw": 5},
        column_border_kw={"color": bg_color, "lw": 2},
        textprops={"fontsize": 16, "ha": "center", "fontname": "DejaVu Sans"},
    )
    
    num_teams = league_table.shape[0]
    league_split = False

    if league_split:
            
        for idx in [0,1,2,3,4]:
            table.rows[idx].set_facecolor(row_colors["top4"])
        for idx in [5,6,7,8]:
            table.rows[idx].set_facecolor(row_colors["playoffs"])

        cup_teams = mlines.Line2D([], [], color=row_colors["top4"], marker='s', linestyle='None',
                            markersize=15, label='Cup Teams')
        shield_teams = mlines.Line2D([], [], color=row_colors["playoffs"], marker='s', linestyle='None',
                            markersize=15, label='Shield Teams')

        legend=plt.legend(handles=[cup_teams, shield_teams], facecolor='white',
                    framealpha=1, loc='upper left', bbox_to_anchor=(0,0.97), fontsize=14, 
                    title="League Playoff Split", title_fontsize=16, labelcolor='linecolor' )
        plt.setp(legend.get_title(), color='black')
  
    else:
        for idx in [0]:
            table.rows[idx].set_facecolor(row_colors["top4"])
        if num_teams > 6:    
            for idx in [1]:
                table.rows[idx].set_facecolor(row_colors["top6"])
                
            for idx in [num_teams-2]:
                table.rows[idx].set_facecolor(row_colors["playoffs"])
                table.rows[idx].set_fontcolor(row_colors["top4"])

        for idx in [num_teams-1]:
            table.rows[idx].set_facecolor(row_colors["relegation"])
            table.rows[idx].set_fontcolor(row_colors["top4"])

        table.ro[num_teams-1, :].text.set_color("#e0e8df")

    # Adding the bold header as a text annotation using \n to create a new line
    header_text = "\n 2025 Belfast Padel League\n\n League Table \n\n"
    header_props = {'fontsize': 22, 
                    'fontweight': 'bold',
                    'va': 'center',
                    'ha': 'center',
                    'color': row_colors["relegation"]}
    # Adjusting the y-coordinate to bring the header closer to the table
    plt.text(0.5, 0.91, header_text, transform=fig.transFigure, **header_props)

    # Include Watermark 
    # fig.figimage(im, 250, 755, zorder=3, alpha=1)
    # fig.figimage(im, 1250, 755, zorder=3, alpha=1)

    return fig 

def create_weekly_results_table(League, week):
    global row_colors, bg_color, text_color, col_defs

    # Define column definitions for creating the table with specific properties.
    small_text = 12
    large_text = 14
    outer_width = 1.9
    col_defs = (
    [

        ColumnDefinition(
            name="Winner",
            title="Winners",
            textprops={"ha": "left", "weight": "bold"},
            width=outer_width,
        ),
        ColumnDefinition(
            name="Winner Players",
            title="",
            textprops={"ha": "left", "fontsize": small_text},
            width=1.5,
        ),
         ColumnDefinition(
            name="Set Score",
            title="",
            textprops={"ha": "center", "weight": "bold"},
            width=0.15,
        ),
         ColumnDefinition(
            name="Game Score",
            title="Score",
            textprops={"ha": "left", "weight": "bold"},
            width=0.75,
        ),
        ColumnDefinition(
            name="Loser Players",
            title="",
            textprops={"ha": "right", "fontsize": small_text},
            width=1.5,
        ),
        ColumnDefinition(
            name="Loser",
            title="Losers",
            textprops={"ha": "left", "weight": "bold"},
            width=outer_width+0.3,
        )
    ])

    # Setting font for text rendering to "DejaVu Sans" and adjust the figure's bounding box to be "tight."
    plt.rcParams["font.family"] = ["DejaVu Sans"]
    # plt.rcParams["savefig.bbox"] = "tight"
    plt.rcParams["text.color"] = text_color
    # plt.rcParams["font.family"] = "Roboto"

    # Build the league table from your results matrix
    # week_results = week_results_table(week)
    week_results = League.week_results_table(week).set_index("Winner")

    # print(week_results)
    # Creeate Table
    fig, ax = plt.subplots(figsize=(21, week_results.shape[0]+1))

    fig.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    table = Table(
        week_results,
        column_definitions=col_defs,
        row_dividers=True,
        col_label_divider=False,
        footer_divider=True,
        # index_col="Team",
        columns=week_results.columns,
        even_row_color=row_colors["even"],
        footer_divider_kw={"color": bg_color, "lw": 2},
        row_divider_kw={"color": bg_color, "lw": 5},
        column_border_kw={"color": bg_color, "lw": 2},
        textprops={"fontsize": 16, "ha": "center", "fontname": "DejaVu Sans"},
        col_label_cell_kw={'facecolor': row_colors['top4']}
    )
    
    table.rows[week_results.shape[0]-1].set_fontcolor(row_colors["top4"])

    # table.rows[table.shape[0]-1].set_fontcolor(row_colors["top4"])
    # Adding the bold header as a text annotation using \n to create a new line
    header_text = f"\n Week {week} Results"
    header_props = {'fontsize': 21, 'fontweight': 'bold', 'va': 'center', 'ha': 'center', 'color': row_colors["relegation"]}
    # Adjusting the y-coordinate to bring the header closer to the table
    plt.text(0.5, 1, header_text, transform=fig.transFigure, **header_props)

    #### ----
    # Adding the bold header as a text annotation using \n to create a new line
    start_date_dt = datetime.datetime.strptime(League.startdate, '%Y-%m-%d')
    week_ending   = start_date_dt + timedelta(days=(week-1)*7)
    
    week_buffer = 0
    week_ending = week_ending + timedelta(weeks=week_buffer)  
  
    def ordinal(n: int) -> str:
        """
        derive the ordinal numeral for a given number n
        """
        return f"{n:d}{'tsnrhtdd'[(n//10%10!=1)*(n%10<4)*n%10::4]}"
    
    dayOrdinal = ordinal(week_ending.day)

    date_string = week_ending.strftime(f'%A, {dayOrdinal} %B')

    subtitle_text = f"Week Ending: {date_string}"
    subtitle_props = {'fontsize': 16, 'fontweight': 'bold', 'va': 'bottom', 'ha': 'center'}#'
    # Adjusting the y-coordinate to bring the header closer to the table
    plt.text(0.5, 1, header_text, transform=fig.transFigure, **header_props)
    sub_title_switch = True
    if sub_title_switch == True:
        plt.text(0.5, 0.9, subtitle_text, transform=fig.transFigure, **subtitle_props)

    return fig
    # fig.savefig(f"Week {week} Results.png", facecolor=ax.get_facecolor(), dpi=200)

def create_weekly_schedule_table(League, week):
    global row_colors, bg_color, text_color, col_defs

    # Define column definitions for creating the table with specific properties.
    small_text = 12
    large_text = 14
    outer_width = 1.9

    col_defs = (
        [

            ColumnDefinition(
                name="Team 1",
                title="Team A",
                textprops={"ha": "left", "weight": "bold"},
                width=outer_width,
            ),
            ColumnDefinition(
                name="Players 1",
                title="",
                textprops={"ha": "left", "fontsize": small_text},
                width=1.5,
            ),
            ColumnDefinition(
                name=" ",
                textprops={"ha": "center"},
                width=0.75,
            ),
            ColumnDefinition(
                name="Players 2",
                title="",
                textprops={"ha": "right", "fontsize": small_text},
                width=1.5,
            ),
            ColumnDefinition(
                name="Team 2",
                title="Team B",
                textprops={"ha": "left", "weight": "bold"},
                width=outer_width+0.3,
            )
        ])

    # Setting font for text rendering to "DejaVu Sans" and adjust the figure's bounding box to be "tight."
    plt.rcParams["font.family"] = ["DejaVu Sans"]
    # plt.rcParams["savefig.bbox"] = "tight"
    plt.rcParams["text.color"] = text_color
    # plt.rcParams["font.family"] = "Roboto"

    # Build the league table from your results matrix
    week_schedule = League.week_schedule_table(week).set_index("Team 1")
    # print(week_schedule)
    # print(week_results)
    # Creeate Table
    fig, ax = plt.subplots(figsize=(21, week_schedule.shape[0]+1))

    fig.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    table = Table(
        week_schedule,
        column_definitions=col_defs,
        row_dividers=True,
        col_label_divider=False,
        footer_divider=True,
        # index_col="Team",
        columns=week_schedule.columns,
        even_row_color=row_colors["even"],
        footer_divider_kw={"color": bg_color, "lw": 2},
        row_divider_kw={"color": bg_color, "lw": 5},
        column_border_kw={"color": bg_color, "lw": 2},
        textprops={"fontsize": 16, "ha": "center", "fontname": "DejaVu Sans"},
        col_label_cell_kw={'facecolor': row_colors['top4']}
    )

    table.rows[week_schedule.shape[0]-1].set_fontcolor(row_colors["top4"])

    # Adding the bold header as a text annotation using \n to create a new line
    header_text = f"\n Week {week} Schedule"
    header_props = {'fontsize': 20, 'fontweight': 'bold', 'va': 'center', 'ha': 'center','color': row_colors["relegation"]}
    start_date_dt = datetime.datetime.strptime(League.startdate, '%Y-%m-%d')
    week_ending   = start_date_dt + timedelta(days=(week-1)*7)
    
    week_buffer = 0
    week_ending = week_ending + timedelta(weeks=week_buffer)  
  
    def ordinal(n: int) -> str:
        """
        derive the ordinal numeral for a given number n
        """
        return f"{n:d}{'tsnrhtdd'[(n//10%10!=1)*(n%10<4)*n%10::4]}"
    
    dayOrdinal = ordinal(week_ending.day)

    date_string = week_ending.strftime(f'%A, {dayOrdinal} %B')

    subtitle_text = f"Week Ending: {date_string}"
    subtitle_props = {'fontsize': 16, 'fontweight': 'bold', 'va': 'bottom', 'ha': 'center'}#'
    # Adjusting the y-coordinate to bring the header closer to the table
    plt.text(0.5, 1, header_text, transform=fig.transFigure, **header_props)
    sub_title_switch = True
    if sub_title_switch == True:
        plt.text(0.5, 0.9, subtitle_text, transform=fig.transFigure, **subtitle_props)


    return fig

def create_head_to_head_table(head_to_head_table):
    global row_colors, bg_color, text_color, col_defs

    # Define column definitions for creating the table with specific properties.
    teams  = head_to_head_table.columns.tolist()    
    col_defs = ([ColumnDefinition(
                name="index",
                title="                   Team B\n              vs          \n Team A           ",
                textprops={"ha": "right", "weight": "bold"},
                width=5.2,
            ),
            ColumnDefinition(
                name=teams[0],
                title="Sets \nin the \nCity \n ",
                textprops={"ha": "center", "weight": "bold"},
                width = 2.7,
            ),
            ColumnDefinition(
                name=teams[1],
                title="That's \nA \nPaddlin' \n ",
                textprops={"ha": "center", "weight": "bold"},
                width= 2.7,
            ),
            ColumnDefinition(
                name=teams[2],
                title="Player? \nI Hardly \nKnow Her \n ",
                textprops={"ha": "center", "weight": "bold"},
                width= 2.7,
            ),
            ColumnDefinition(
                name=teams[3],
                title="Cheaper \nby the \nCousin' \n ",
                textprops={"ha": "center", "weight": "bold"},
                width= 2.7,
            ),
            ColumnDefinition(
                name=teams[4],
                title="Armaghgeddon \n ",
                textprops={"ha": "center", "weight": "bold"},
                width= 2.7,
            ),
            ColumnDefinition(
                name=teams[5],
                title="Slim \n Reapers \n ",
                width= 2.7,
                textprops={"ha": "center", "weight": "bold"},
            ),
            ColumnDefinition(
                name=teams[6],
                title="Rose and \nCrown \n Padel Club \n ",
                width=2.7,
                textprops={"ha": "center", "weight": "bold"},
                # group="Sets",
            ),
            ColumnDefinition(
                name=teams[7],
                title="The Binge \n Drinkers \n ",
                width= 2.7,
                textprops={"ha": "center", "weight": "bold"},
            ),
            ColumnDefinition(
                name=teams[8],
                title="The \n Receptionists \n ",
                width=3,
                textprops={"ha": "center", "weight": "bold"},
            )])
  
    # Setting font for text rendering to "DejaVu Sans" and adjust the figure's bounding box to be "tight."
    plt.rcParams["font.family"] = ["DejaVu Sans"]
    # plt.rcParams["savefig.bbox"] = "tight"
    plt.rcParams["text.color"] = text_color
    # plt.rcParams["font.family"] = "Roboto"

    # Build the league table from your results matrix
    # league_table = build_league_table_from_matrix(results_matrix, points_per_win=3)
    # head_to_head_table = head_to_head_table.set_index("Team A")

    # print(league_table)
    # Import image
    # with cbook.get_sample_data("images\\padel_logo_2_small.png") as file:
    #     im = image.imread(file)
    # Create Table
    fig, ax = plt.subplots(figsize=(30, head_to_head_table.shape[0]+1))

    fig.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    table = Table(
        head_to_head_table,
        column_definitions=col_defs,
        row_dividers=True,
        col_label_divider=True,
        footer_divider=True,
        # index_col="Team",
        columns=head_to_head_table.columns,
        odd_row_color=row_colors["even"],
        # header_divider_kw={"color": logo_yellow, "lw": 2},
        footer_divider_kw={"color": bg_color, "lw": 2},
        row_divider_kw={"color": bg_color, "lw": 5},
        column_border_kw={"color": bg_color, "lw": 2},
        textprops={"fontsize": 16, "ha": "center", "fontname": "DejaVu Sans"},
    )
    

    for i in range(0,len(table.rows)):
        for j in range(1, len(table.columns)):
            if len(table.cells[i, j].text.get_text()) > 1:
                if int(table.cells[i, j].text.get_text()[1]) > int(table.cells[i, j].text.get_text()[4]):
                    table.cells[i, j].rectangle_patch.set_color("green")
                else: 
                    table.cells[i, j].rectangle_patch.set_color("red")


    # Adding the bold header as a text annotation using \n to create a new line
    header_text = "\n Head-to-Head\n\n\n"

    header_props = {'fontsize': 22, 
                    'fontweight': 'bold',
                    'va': 'center',
                    'ha': 'center',
                    'color': row_colors["relegation"]}
    # Adjusting the y-coordinate to bring the header closer to the table
    plt.text(0.5, 0.91, header_text, transform=fig.transFigure, **header_props)

    # Include Watermark 
    # fig.figimage(im, 250, 755, zorder=3, alpha=1)
    # fig.figimage(im, 1250, 755, zorder=3, alpha=1)

    return fig

def create_winners_page(league_table):
    global row_colors, bg_color, text_color, col_defs

    # Define column definitions for creating the table with specific properties.
    small_text = 12
    large_text = 14
    outer_width = 0.8 


   # Import image
    # with cbook.get_sample_data("C:\\Users\\colmk\\Documents\\Padel League\\images\\padel_logo_2.png") as file:
    #     im = image.imread(file)
    # Setting font for text rendering to "DejaVu Sans" and adjust the figure's bounding box to be "tight."
    plt.rcParams["font.family"] = ["DejaVu Sans"]
    # plt.rcParams["savefig.bbox"] = "tight"
    plt.rcParams["text.color"] = text_color
    # plt.rcParams["font.family"] = "Roboto"


    # print(week_results)
    # Creeate Table
    # fig = plt.figure(figsize=(21, 10))
    fig, ax = plt.subplots(figsize=(21, 7))

    fig.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)
    ax.axis('off')

    # Create some text celbrating the winning team
    winning_team = league_table.iloc[0]['Team']
    winning_players = league_table.iloc[0]['Players'].split(", ")
    # print(winning_players)
    header_props = {'fontweight': 'bold', 'va': 'center', 'ha': 'center'}
    
    fig.text(0.5, 0.7, "2  0  2  5",fontsize=56, color=row_colors["top4"], **header_props)

    fig.text(0.5, 0.6, "Padel League",fontsize=36, color=row_colors["top4"], **header_props)
    fig.text(0.5, 0.48, "CHAMPIONS",fontsize=40, color=row_colors["top4"], **header_props)
    fig.text(0.5, 0.35, f"{winning_team}",fontsize=30, color=row_colors["relegation"], **header_props)
    fig.text(0.5, 0.25, f"{winning_players[0]} & {winning_players[1]}",fontsize=25, color=text_color, **header_props)


    # Include Watermark
        # Include Watermark 
    # fig.figimage(im, 5, -10, zorder=3, alpha=1)
    # fig.figimage(im, 1055, -10, zorder=3, alpha=1)
    return fig

# fig.savefig("Images/league_table_New_New.png", facecolor=ax.get_facecolor(), dpi=200)

# if __name__ == "__main__":
#     create_league_table()
import pandas as pd
import numpy as np
# import pyperclip

class padelLeague():
    def __init__(self, teams_and_players, startdate, schedule):
        """
        teams_and_players: dict mapping team names to list of player names
        """
        self.teams_and_players = teams_and_players
        self.teams = list(teams_and_players.keys())
        self.__setattr__("startdate", startdate)

        self.round_robin_schedule = schedule

        # Build requirements
        self.sets_score_matrix = self.sets_score_matrix()
        self.games_score_matrix = self.games_score_matrix()
    
    
    # ==== DISPLAY ITEMS ====
    def get_teams(self):
        return self.teams
    
    def get_players(self, team):
        return self.teams_and_players.get(team, []) 
    
    # Display Week Schedule
    def show_week_schedule(self, week_num):
        print(f"\n--- Week {week_num} Fixtures ---")
        # If statement for if week too high
        if week_num > len(self.round_robin_schedule):
            print(f"Week {week_num} does not exist in the schedule.")
            return
        else:
            for match in self.round_robin_schedule[week_num - 1]:

                if "BYE" in match:
                    print(f"{match[0]} has a BYE")
                else:
                    print(f"{match[0]} vs {match[1]}")
    
    # Display Week Results
    def show_week_results(self, week_num):   
        print(f"\n--- Week {week_num} Results ---")
        if week_num > len(self.round_robin_schedule):
            print(f"Week {week_num} does not exist in the schedule.")
            return
        else:
            for match in self.round_robin_schedule[week_num - 1]:
                if "BYE" in match:
                    print(f"{match[0]} has a BYE")
                else:
                    team1, team2 = match
                    sets = self.games_score_matrix.loc[team1, team2]
                    score = self.sets_score_matrix.loc[team1, team2]
                    if score is None:   
                        print(f"{team1} vs {team2} | No result posted yet")
                    else:
                        print(f"{team1} vs {team2} | Sets: {sets[0]}-{sets[1]} | Score: {score}")
        
    # ==== ROUND ROBIN SCHEDULER ====
    # !!! DEFUCT As league is initialased and made unique through this function
    # def round_robin(self):
    #     teams_with_bye = self.teams.copy()
    #     if len(self.teams) % 2:
    #         teams_with_bye.append("BYE")
    #     schedule = []
    #     n = len(teams_with_bye)
    #     fixtures = list(range(n))
    #     for _ in range(n-1):
    #         week = []
    #         for i in range(n // 2):
    #             t1 = teams_with_bye[fixtures[i]]
    #             t2 = teams_with_bye[fixtures[n - 1 - i]]
    #             if t1 != "BYE" or t2 != "BYE":
    #                 week.append((t1, t2))
    #         fixtures = fixtures[:1] + fixtures[-1:] + fixtures[1:-1]
    #         schedule.append(week)
    #     return schedule
    
    # ==== RESULTS MATRICIS ====
    # Create empty results matrix (each cell will contain None initially)
    def sets_score_matrix(self):
        results_matrix = pd.DataFrame(
        np.full((len(self.teams), len(self.teams)), None),
        index = self.teams,
        columns = self.teams
        )
        return results_matrix

    # Create empty wins matrix (each cell will contain None initially)
    def games_score_matrix(self):
        wins_matrix = pd.DataFrame(
        np.full((len(self.teams), len(self.teams)), None),
        index = self.teams,
        columns = self.teams
        )
        return wins_matrix
    
    # === HELPER: PARSE MATCH SCORES ===
    def parse_set_totals(self, set_scores):
        """
        set_scores: list of tuples/lists like [(6,4), (5,7), (6,3)]
        Returns: (sets_won_team1, sets_won_team2)
        """
        sets_won_team1 = sum(1 for s in set_scores if s[0] > s[1])
        sets_won_team2 = sum(1 for s in set_scores if s[1] > s[0])
        return sets_won_team1, sets_won_team2
    
    def parse_game_totals(self, set_scores):
        """
        set_scores: list of tuples/lists like [(6,4), (5,7), (6,3)]
        Returns: (total_games_team1, total_games_team2)
        """
        total1 = sum(s[0] for s in set_scores)
        total2 = sum(s[1] for s in set_scores)
        return total1, total2
            
    # Function to record score in matrix
    def record_match(self, team1, team2, set_scores):
        # global results_matrix, wins_matrix
        """
        team1, team2: team names
        set_scores: list of tuples/lists like [(6,4), (5,7), (6,3)]
        """
        if len(set_scores) != 3:
            raise ValueError("Exactly three set scores must be entered.")
        for score in set_scores:
            if any (s > 5 for s in score):
                raise ValueError(f"Set scores must be between 0 and 5. {team1} vs. {team2}, {set_scores}")
            if max(score) <4:
                raise ValueError(f"Each set must have a winner. {team1} vs. {team2}, {set_scores}")

        # Record the match in results matrix
        self.games_score_matrix.loc[team1, team2] = set_scores
        self.games_score_matrix.loc[team2, team1] = [(b, a) for a, b in set_scores]  # reverse for
        # Record the match in wins matrix
        self.sets_score_matrix.loc[team1, team2] = self.parse_set_totals(set_scores)
        self.sets_score_matrix.loc[team2, team1] = (self.sets_score_matrix.loc[team1, team2][1], self.sets_score_matrix.loc[team1, team2][0])

    def build_league_table_from_matrix(self, points_per_win=3):
        """
        Build a fresh league table based entirely on the given results_matrix.
        results_matrix: DataFrame
            - Index = team names
            - Columns = team names
            - Each cell: list of tuples/lists representing set scores e.g. [(6,4),(5,7),(6,3)]
        points_per_win: int
            Points awarded for a win.
        Returns:
            A pandas DataFrame with columns: Team, Played, Wins, Losses, Points, GF, GA
        """
        table = pd.DataFrame({
            "Team": self.get_teams(),
            'Players': [", ".join(self.teams_and_players[team]) for team in self.get_teams()],
            "Played": 0,
            "Wins": 0,
            "Losses": 0,
            "Points": 0,
            "Sets For": 0,
            "Sets Against": 0,
            "Games For": 0,
            "Games Against": 0
        })
        
        # Process each match once (upper triangle of matrix)
        for i, team1 in enumerate(self.get_teams()):
            for j, team2 in enumerate(self.get_teams()):
                if j <= i:
                    continue  # Avoid duplicates and self-matches
                match_data = self.sets_score_matrix.loc[team1, team2]
                if match_data is None:
                    continue  # No result
            
                # Count total Sets for SF/SA
                sf1 = match_data[0]
                sa1 = match_data[1]
                sf2 = sa1
                sa2 = sf1

                # Count total games for GF/GA
                gf1 = self.parse_game_totals(self.games_score_matrix.loc[team1, team2])[0]
                ga1 = self.parse_game_totals(self.games_score_matrix.loc[team1, team2])[1]
                gf2 = ga1
                ga2 = gf1

                # Update matches played
                table.loc[table.Team == team1, "Played"] += 1
                table.loc[table.Team == team2, "Played"] += 1
                table.loc[table.Team == team1, "Sets For"] += sf1
                table.loc[table.Team == team1, "Sets Against"] += sa1
                table.loc[table.Team == team2, "Sets For"] += sf2
                table.loc[table.Team == team2, "Sets Against"] += sa2
                table.loc[table.Team == team1, "Games For"] += gf1
                table.loc[table.Team == team1, "Games Against"] += ga1
                table.loc[table.Team == team2, "Games For"] += gf2
                table.loc[table.Team == team2, "Games Against"] += ga2

                # Determine winner by set count
                sets_won_1 = sf1
                sets_won_2 = sf2
                if sets_won_1 > sets_won_2:
                    table.loc[table.Team == team1, "Wins"] += 1
                    table.loc[table.Team == team1, "Points"] += points_per_win
                    table.loc[table.Team == team2, "Losses"] += 1
                elif sets_won_2 > sets_won_1:
                    table.loc[table.Team == team2, "Wins"] += 1
                    table.loc[table.Team == team2, "Points"] += points_per_win
                    table.loc[table.Team == team1, "Losses"] += 1
                # If you want to handle draws, you could add here.

        # Sort table
        table = table.assign(set_diff=table["Sets For"] - table["Sets Against"]) \
                         .assign(game_diff=table["Games For"] - table["Games Against"]) \
             .sort_values(by=["Points", "set_diff", "game_diff", "Sets For", 'Games For', 'Sets Against', 'Games Against', 'Team'], 
                                ascending=[False, False, False, False, False,  True, True, True]).reset_index(drop=True)#\
            #   .drop(columns=["set_diff", "game_diff"]) 
        # print("\n--- League Table ---")
        # print(table.to_string(index=False))
        table = table.drop(columns=["set_diff", "game_diff"])

        return table
  
    # Weekly Schudule Table
    def week_schedule_table(self, week_num):
        """
        Returns a table (as a pandas DataFrame) for the given week's schedule.
        Each game is two rows: first row is team names, second row is player names, split into two columns.
        If a team has a BYE, show that this team rests, and place BYE rows at the bottom of the table.
        """
        game_rows = []
        bye_rows = []
        for match in self.round_robin_schedule[week_num - 1]:
            if "BYE" in match:
                resting_team = match[0] if match[1] == "BYE" else match[1]
                resting_players = ", ".join(self.teams_and_players[resting_team])
                bye_rows.append([resting_team, resting_players, '', '', "Rest Week"])
                # bye_rows.append(["","", ""])
                continue
            team1, team2 = match
            players1 = ", ".join(self.teams_and_players[team1])
            players2 =", ".join(self.teams_and_players[team2])
            game_rows.append([team1, players1,'vs', players2, team2])
        rows = game_rows + bye_rows
        df = pd.DataFrame(rows, columns=["Team 1", 'Players 1', '', 'Players 2', "Team 2"])
        return df
    
    # Weekly Results Table
    def week_results_table(self, week_num):
        """
        Returns a table (as a pandas DataFrame) for the given week's results.
        Each row: Winning Team, Winning Players, Score, Losing Team, Losing Players.
        If a team has a BYE, show that this team rests, and place BYE rows at the bottom of the table.
        """
        game_rows = []
        bye_rows = []
        for match in self.round_robin_schedule[week_num - 1]:
            if "BYE" in match:
                resting_team = match[0] if match[1] == "BYE" else match[1]
                resting_players = ", ".join(self.teams_and_players[resting_team])
                bye_rows.append([resting_team, resting_players, "", "","", "Rest Week"])
                continue
            team1, team2 = match
            players1 = ", ".join(self.teams_and_players[team1])
            players2 = ", ".join(self.teams_and_players[team2])
            set_scores = self.games_score_matrix.loc[team1, team2]
            sets = self.sets_score_matrix.loc[team1, team2]
            if set_scores is not None and sets is not None:
                if sets[0] > sets[1]:
                    winner, winner_players = team1, players1
                    loser, loser_players = team2, players2
                    set_score_str = f"{sets[0]}-{sets[1]}"
                    games_score_str = f"({', '.join(f'{a}-{b}' for (a, b) in set_scores)})"
                else:
                    winner, winner_players = team2, players2
                    loser, loser_players = team1, players1
                    # Reverse the set scores for display
                    reversed_scores = [(b, a) for (a, b) in set_scores]
                    set_score_str = f"{sets[1]}-{sets[0]}"
                    games_score_str = f"({', '.join(f'{a}-{b}' for (a, b) in reversed_scores)})"
            else:

                winner, winner_players, loser, loser_players, set_score_str, games_score_str = team1, players1, team2, players2, "", "Pending"
            game_rows.append([winner, winner_players, set_score_str, games_score_str, loser_players, loser])
        rows = game_rows + bye_rows
        df = pd.DataFrame(rows, columns=["Winner", "Winner Players", "Set Score", "Game Score", "Loser Players", "Loser"])

        return df
    




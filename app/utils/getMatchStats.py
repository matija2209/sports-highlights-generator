import pandas as pd
from models.Timestamp import TopPlayer,MatchScore,FootballEvent
from typing import List, Tuple

def get_top_players(timestamps: List[FootballEvent]) -> Tuple[List[TopPlayer], List[TopPlayer]]:
    # Convert list of dictionaries to a pandas DataFrame
    data = pd.DataFrame(timestamps)
    
    # Filter and count goals per player
    top_goal_scorers_series = data[data['type'] == 'GOL']['scorer'].value_counts().head(5)
    top_goal_scorers = [TopPlayer(name=name, count=count) for name, count in top_goal_scorers_series.items()]
    
    # Filter and count opportunities per player
    top_opportunity_creators_series = data[data['type'] == 'Priložnost']['scorer'].value_counts().head(5)
    top_opportunity_creators = [TopPlayer(name=name, count=count) for name, count in top_opportunity_creators_series.items()]

    return top_goal_scorers, top_opportunity_creators

def calculate_match_scores(data: List[FootballEvent]):
    # Initialize a list to hold the scores for each match
    df = pd.DataFrame(data)

    # Filter for Goal events
    goals_df = df[df['type'] == 'GOL']

    # Count goals by game and team
    goal_counts = goals_df.groupby(['game', 'team']).size().reset_index(name='goals')
    final_structure = []

    # Iterate over each game in goal_counts
    for game in goal_counts['game'].unique():
        # Extract rows for the current game
        game_goals = goal_counts[goal_counts['game'] == game]

        # Initialize goals for both teams to 0
        teamOneGoals = 0
        teamTwoGoals = 0

        # Assign goals to team one and team two based on the order they appear in the DataFrame
        if len(game_goals) > 0:
            teamOneGoals = game_goals.iloc[0]['goals']
        if len(game_goals) > 1:
            teamTwoGoals = game_goals.iloc[1]['goals']

        # Append the structured data for the current game to the final_structure list
        final_structure.append({
            'game': game,
            'teamOneGoals': teamOneGoals,
            'teamTwoGoals': teamTwoGoals
        })

    return final_structure
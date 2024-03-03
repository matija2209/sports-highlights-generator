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

def calculate_match_scores(data: List[dict]) -> List[dict]:
    # Finding match start indices and game numbers
    match_starts = [(index, event['game']) for index, event in enumerate(data) if event['type'] == 'Match Start']
    match_starts.append((len(data), None))  # Ensure the last match is included

    scores = []

    for i in range(len(match_starts) - 1):
        start, end = match_starts[i][0], match_starts[i + 1][0]
        game_number = match_starts[i][1]
        match_data = data[start:end]
        
        # Tally goals by team
        team_goals = {}
        for event in match_data:
            if event['type'] == 'GOL':
                team_goals[event['team']] = team_goals.get(event['team'], 0) + 1

        # Initialize goals to 0 for each team
        team_one_goals = team_goals.get('A', 0)
        team_two_goals = team_goals.get('B', 0)

        scores.append({'match': game_number, 'teamOneGoals': team_one_goals, 'teamTwoGoals': team_two_goals})

    return scores
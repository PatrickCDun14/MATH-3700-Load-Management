########
## Name: Patrick Dunleavy and Aleks Hremonic
## 

import nba_api
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import leagueleaders
import json

def get_players_for_year(season_year):

    # Create an instance of the LeagueLeaders class for the 2021-2022 season, 2021-22'
    league_leaders = leagueleaders.LeagueLeaders(season=season_year)

    #   Convert the data to a DataFrame
    leaders_stats_df = league_leaders.get_data_frames()[0]

    # Sort the DataFrame by points in descending order
    sorted_leaders_stats_df = leaders_stats_df.sort_values(by='PTS', ascending=False)

    # Convert the sorted DataFrame to a dictionary
    leaders_stats_dict = sorted_leaders_stats_df.to_dict(orient='records')

    # Convert the dictionary to a JSON string with formatting
    formatted_json = json.dumps(leaders_stats_dict, indent=4)

    # Write the formatted JSON to a file
    with open(f'nba_league_leaders_{season_year}_sorted_by_points.json', 'w') as file:
        file.write(formatted_json)

    print(f'NBA league leaders data for the  season, sorted by points, has been saved to nba_league_leaders_{season_year}_sorted_by_points.json')


def sort_players_by_pts_per_game(json_file):
    # Read JSON data
    with open(json_file, 'r') as file:
        players_data = json.load(file)

    # Calculate PTS/GP and add it to each player's data
    for player in players_data:
        pts = player.get('PTS', 0)
        gp = player.get('GP', 1)
        mp = player.get('MIN', 0)
        player['PTS/GP'] = pts / gp if gp else 0
        player['MPG'] = mp / gp if gp else 0
        player['MIN'] = mp
        player['GP'] = gp

    # Sort players by PTS/GP in descending order
    sorted_players = sorted(players_data, key=lambda x: x['PTS/GP'], reverse=True)

    return sorted_players

def average_minutes_of_top_players(players_data):


    players_data = sorted(players_data, key=lambda x: x.get('PTS', 0) / x.get('GP', 1), reverse=True)
    
    top_40_players = players_data[:40]
    
    total_minutes = sum(player.get('MIN', 0) for player in top_40_players)
    total_games = sum(player.get('GP', 0) for player in top_40_players)
    average_minutes = total_minutes / total_games
    average_games = total_games/len(top_40_players)

    return (f'The average games played was {average_games} and The average minutes were {average_minutes}')

# Example usage
get_players_for_year('1999-00')
print("\n\n\n\n\n\n")

for i in range(0, 23):
    try:
        if i >= 10:
            players_sorted = sort_players_by_pts_per_game(f'nba_league_leaders_20{i}-{i + 1}_sorted_by_points.json')
            averages = average_minutes_of_top_players(players_sorted)
            print(f'{averages} for the year 20{i}-{i + 1}')
        else:
            players_sorted = sort_players_by_pts_per_game(f'nba_league_leaders_200{i}-0{i + 1}_sorted_by_points.json')
            averages = average_minutes_of_top_players(players_sorted)
            print(f'{averages} for the year 200{i}-0{i + 1}')
    except :
        pass


for i in range(90, 99):
    players_sorted = sort_players_by_pts_per_game(f'nba_league_leaders_19{i}-{i + 1}_sorted_by_points.json')
    averages = average_minutes_of_top_players(players_sorted)
    print(f'{averages} for the year 19{i}-{i + 1}')
import os
from flask import json
from constants import PLAYER_DATA_FILE

def load_player_data():
    if os.path.exists(PLAYER_DATA_FILE):
        try:
            with open(PLAYER_DATA_FILE, 'r') as f:
                return json.load(f)
        except:
            print(f"Warning: {PLAYER_DATA_FILE} is corrupted. Resetting data.")
    return {}

def save_player_data(stats, weekly_logs, position, team_color, trade_value_history):
    data = {
        "season_stats": stats,
        "weekly_stats": weekly_logs,
        "position": position,
        "team_color": team_color,
        "trade_value_history": trade_value_history
    }
    with open(PLAYER_DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

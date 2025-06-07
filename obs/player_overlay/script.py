import json
import requests
from obswebsocket import obsws, requests as obs_requests

# CONFIGURE
OBS_HOST = "localhost"
OBS_PORT = 4455
OBS_PASSWORD = "your_password_here"
PLAYER_LIST_URL = "https://your-api.com/players"
PLAYER_INFO_URL = "https://your-api.com/player/"

# CONNECT TO OBS
ws = obsws(OBS_HOST, OBS_PORT, OBS_PASSWORD)
ws.connect()

def fetch_players():
    resp = requests.get(PLAYER_LIST_URL)
    return resp.json()

def fetch_player_info(player_id):
    resp = requests.get(PLAYER_INFO_URL + str(player_id))
    return resp.json()

def update_obs_sources(info):
    # Update a Text source
    ws.call(obs_requests.SetInputSettings("PlayerNameText", {"text": info['name']}, True))
    ws.call(obs_requests.SetInputSettings("PlayerTeamText", {"text": info['team']}, True))
    ws.call(obs_requests.SetInputSettings("PlayerStatsText", {"text": info['stats']}, True))

    # Update an image source
    ws.call(obs_requests.SetInputSettings("PlayerImage", {
        "file": info['image']
    }, True))

def hex_to_rgb(color_hex):
    color_hex = color_hex.lstrip('#')
    r, g, b = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
    return r, g, b

def update_color_filter(source_name, color_hex):
    r, g, b = hex_to_rgb(color_hex)
    ws.call(obs_requests.SetSourceFilterSettings(
        sourceName=source_name,
        filterName="Color Filter",
        filterSettings={
            "color": (r << 16) + (g << 8) + b
        }
    ))

def main():
    players = fetch_players()
    print("Available players:")
    for i, player in enumerate(players):
        print(f"{i + 1}. {player['name']}")

    choice = int(input("Select a player number: ")) - 1
    selected_player = players[choice]
    info = fetch_player_info(selected_player['id'])
    update_color_filter("OverlayBox", info['color'])

    print(f"Selected: {info['name']}")
    update_obs_sources(info)

    ws.disconnect()

if __name__ == "__main__":
    main()

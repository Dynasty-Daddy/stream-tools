from flask import Flask, redirect, render_template_string, request, jsonify, url_for
import threading
import requests as http_requests
import obsws_python as obs
from obsws_python.error import OBSSDKRequestError
from dotenv import load_dotenv
import os

TEAM_PRIMARY_COLOR_HEX = {
    "ARI": "#97233F", "ATL": "#A71930", "BAL": "#241773", "BUF": "#00338D",
    "CAR": "#0085CA", "CHI": "#0B162A", "CIN": "#FB4F14", "CLE": "#311D00",
    "DAL": "#041E42", "DEN": "#002244", "DET": "#0076B6", "GB":  "#203731",
    "HOU": "#03202F", "IND": "#002C5F", "JAX": "#006778", "KC":  "#E31837",
    "LV":  "#000000", "LAC": "#002A5E", "LA":  "#003594", "MIA": "#008E97",
    "MIN": "#4F2683", "NE":  "#002244", "NO":  "#D3BC8D", "NYG": "#0B2265",
    "NYJ": "#125740", "PHI": "#004C54", "PIT": "#FFB612", "SF":  "#AA0000",
    "SEA": "#002244", "TB":  "#D50A0A", "TEN": "#4B92DB", "WAS": "#773141"
}

# CONFIGURE
load_dotenv()
OBS_HOST = os.getenv("OBS_HOST")
OBS_PORT = int(os.getenv("OBS_PORT"))
OBS_PASSWORD = os.getenv("OBS_PASSWORD")
PLAYER_LIST_URL = "https://dynasty-daddy.com/api/v1/player/all/today"

app = Flask(__name__)
ws = obs.ReqClient(host=OBS_HOST, port=OBS_PORT, password=OBS_PASSWORD)

# Load player list once on startup
player_list = []
try:
    resp = http_requests.get(PLAYER_LIST_URL)
    if resp.status_code == 200:
        player_list = resp.json()
except Exception as e:
    print("Error loading players:", e)


def hex_to_rgb(color_hex):
    color_hex = color_hex.lstrip("#")
    return tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))


def update_obs(player):
    print(player)
    try:
        ws.set_input_settings(
            "PlayerNameText",
            {"text": player['full_name']},
            True
        )
    except OBSSDKRequestError as e:
        print(f"Warning: Couldn't update PlayerNameText - {e}")
    
    try:
        ws.set_input_settings(
            "PlayerTeamText",
            {"text": player['team']},
            True
        )
    except OBSSDKRequestError as e:
        print(f"Warning: Couldn't update PlayerTeamText - {e}")
    
    try:
        ws.set_input_settings(
            "PlayerSFValueText",
            {"text": str(player.get('sf_trade_value', '0'))},
            True
        )
    except OBSSDKRequestError as e:
        print(f"Warning: Couldn't update PlayerTeamText - {e}")
    
    try:
        ws.set_input_settings(
            "PlayerValueText",
            {"text": str(player.get('trade_value', '0'))},
            True
        )
    except OBSSDKRequestError as e:
        print(f"Warning: Couldn't update PlayerTeamText - {e}")

    try:
        ws.set_input_settings(
            "PlayerSFPosRankText",
            {"text": str(player.get('sf_position_rank', '0'))},
            True
        )
    except OBSSDKRequestError as e:
        print(f"Warning: Couldn't update PlayerSFPosRankText - {e}")
    
    try:
        ws.set_input_settings(
            "PlayerPosRankText",
            {"text": str(player.get('position_rank', '0'))},
            True
        )
    except OBSSDKRequestError as e:
        print(f"Warning: Couldn't update PlayerPosRankText - {e}")
        

    try:
        ws.set_input_settings(
            "PlayerSFRankText",
            {"text": str(player.get('sf_overall_rank', '0'))},
            True
        )
    except OBSSDKRequestError as e:
        print(f"Warning: Couldn't update PlayerSFRankText - {e}")
    
    try:
        ws.set_input_settings(
            "PlayerRankText",
            {"text": str(player.get('overall_rank', '0'))},
            True
        )
    except OBSSDKRequestError as e:
        print(f"Warning: Couldn't update PlayerRankText - {e}")

    # Calculate RGB color from hex
    color_hex = TEAM_PRIMARY_COLOR_HEX.get(player['team'], "#FFFFFF")
    r, g, b = hex_to_rgb(color_hex)
    color_int = (r << 16) + (g << 8) + b

    try:
        ws.set_source_filter_settings(
            "OverlayBox",
            "Color Filter",
            {"color": color_int}
        )
    except OBSSDKRequestError as e:
        print(f"Warning: Couldn't update color filter - {e}")


@app.route("/", methods=["GET"])
def home():
    q = request.args.get("q", "").lower()
    if q:
        filtered = [p for p in player_list if q in p['full_name'].lower()]
    else:
        filtered = player_list[:50]  # Show top 50 if no query
    return render_template_string(PAGE_HTML, players=filtered, query=q)


@app.route("/select_player/<string:name_id>")
def select_player(name_id):
    player = next((p for p in player_list if p["name_id"] == name_id), None)
    if player:
        update_obs(player)
    return redirect(url_for('home'))

PAGE_HTML = """
<!doctype html>
<title>Player Overlay Control</title>
<h1>Search Player</h1>
<form method="get">
    <input type="text" name="q" value="{{ query }}" placeholder="Search name..." autofocus>
    <button type="submit">Search</button>
</form>
<ul>
{% for player in players %}
  <li><a href="{{ url_for('select_player', name_id=player['name_id']) }}">{{ player['full_name'] }}</a></li>
{% endfor %}
</ul>"""

if __name__ == "__main__":
    app.run(port=5000)

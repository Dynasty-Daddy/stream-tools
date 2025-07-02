from flask import Flask, redirect, render_template_string, request, url_for, session
import requests as http_requests
import obsws_python as obs
from obsws_python.error import OBSSDKRequestError
from dotenv import load_dotenv
from constants import CONFIG_HTML, DEFAULT_PLAYER_IMG_URL, IMG_CSS, NFL_TEAM_IMG_URL, PAGE_HTML, PLAYER_IMG_URL, PLAYER_LIST_URL, TEAM_PRIMARY_COLOR_HEX
import os

# CONFIGURE
load_dotenv()
OBS_HOST = os.getenv("OBS_HOST")
OBS_PORT = int(os.getenv("OBS_PORT"))
OBS_PASSWORD = os.getenv("OBS_PASSWORD")

app = Flask(__name__)
ws = obs.ReqClient(host=OBS_HOST, port=OBS_PORT, password=OBS_PASSWORD)

# Load player list once on startup
player_list = []
queue = []
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

    fields = {
        "PlayerName": player['full_name'],
        "PlayerFirstName": player['first_name'],
        "PlayerLastName": player['last_name'],
        "PlayerTeam": player['team'],
        "PlayerSFValue": str(player.get('sf_trade_value', '0')),
        "PlayerValue": str(player.get('trade_value', '0')),
        "PlayerSFPosRank": str(player.get('sf_position_rank', '0')),
        "PlayerPosRank": str(player.get('position_rank', '0')),
        "PlayerSFRank": str(player.get('sf_overall_rank', '0')),
        "PlayerRank": str(player.get('overall_rank', '0')),
        "PlayerPosition": player.get('position', ''),
        "PlayerAge": str(player.get('age', '')),
        "PlayerExperience": str(player.get('experience', '')),
        "PlayerInjuryStatus": player.get('injury_status') or "Healthy",
        "PlayerDynastyADP": str(player.get('dynasty_daddy_adp', '')),
        "PlayerUnderdogADP": str(player.get('underdog_adp', '')),
        "PlayerAvgADP": str(player.get('avg_adp', '')),
        # Add more fields as needed...
    }

    for input_name, text_value in fields.items():
        try:
            ws.set_input_settings(input_name, {"text": text_value}, True)
        except OBSSDKRequestError as e:
            if e.code == 600:
                print(f"⚠️ Skipped missing source: '{input_name}'")
            else:
                print(f"⚠️ Error updating '{input_name}' - {e}")

    # Player Image Mapping
    player_img_url = DEFAULT_PLAYER_IMG_URL
    sleeper_id = player['sleeper_id']
    if sleeper_id is not None:
        player_img_url = PLAYER_IMG_URL.replace("SLEEPER_ID", sleeper_id)

    try:
        ws.set_input_settings(
            "PlayerImg",
            {
            "url": player_img_url,
            "css": IMG_CSS,
            },
            True
        )
    except OBSSDKRequestError as e:
        print(f"⚠️ Error updating PlayerImg source - {str(e)}")

    # Team Image Mapping
    team_acc = player['team'].lower()
    team_img_url = NFL_TEAM_IMG_URL.replace("TEAM_ACC", team_acc)

    try:
        ws.set_input_settings(
            "PlayerTeamImg",
            {
            "url": team_img_url,
            "css": IMG_CSS,
            },
            True
        )
    except OBSSDKRequestError as e:
        print(f"⚠️ Error updating PlayerTeamImg source - {str(e)}")
    
    # Team Color Mapping
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

def get_queue():
    return session.get("queue", [])

def save_queue(queue):
    session["queue"] = queue

@app.route("/", methods=["GET"])
def home():
    # Check if config in session, else redirect to config page
    if not all(k in session for k in ('obs_host', 'obs_port')):
        return redirect(url_for("config"))

    query = request.args.get("q", "").lower()
    if query:
        filtered = [p for p in player_list if query in p['full_name'].lower()]
    else:
        filtered = player_list[:25]
    queue_ids = get_queue()
    queue_players = []
    player_map = {p['name_id']: p for p in player_list}
    for name_id in queue_ids:
        player = player_map.get(name_id)
        if player:
            queue_players.append(player)
    return render_template_string(PAGE_HTML, query=query, players=filtered, queue=queue_players)

@app.route("/select_player/<string:name_id>")
def select_player(name_id):
    player = next((p for p in player_list if p["name_id"] == name_id), None)
    if player:
        update_obs(player)
    return redirect(url_for('home'))

@app.route("/queue/<name_id>")
def queue_player(name_id):
    queue = get_queue()
    if name_id not in queue:
        queue.append(name_id)
        save_queue(queue)
    return redirect(url_for("home"))

@app.route("/play-next", methods=["POST"])
def play_next_player():
    queue = get_queue()
    if queue:
        name_id = queue.pop(0)
        save_queue(queue)
        player = next((p for p in player_list if p["name_id"] == name_id), None)
        if player:
            update_obs(player)
    return redirect(url_for("home"))

@app.route("/clear-queue", methods=["POST"])
def clear_queue():
    save_queue([])
    return redirect(url_for("home"))

@app.route("/config", methods=["GET", "POST"])
def config():
    if request.method == "POST":
        session['obs_host'] = request.form['host']
        session['obs_port'] = int(request.form['port'])
        session['obs_password'] = request.form.get('password', '')
        return redirect(url_for("home"))

    # Prefill form if session has values
    return render_template_string(
        CONFIG_HTML,
        host=session.get('obs_host'),
        port=session.get('obs_port', 4455),
        password=session.get('obs_password')
    )

if __name__ == "__main__":
    app.secret_key = "supersecret"
    app.run(port=5000)

import os
from datetime import datetime
import threading
import webbrowser
from flask import Flask, redirect, render_template_string, request, url_for, session, send_from_directory
import requests as http_requests
import obsws_python as obs
from obsws_python.error import OBSSDKRequestError
from dotenv import load_dotenv
from constants import ADP_DADDY_MARKET_URL, ADP_DADDY_RD_MARKET_URL, CONFIG_HTML, DEFAULT_PLAYER_IMG_URL, DYNASTY_DADDY_MARKET_URL, FANTASY_DADDY_MARKET_URL, IMG_CSS, MARKET_FIELDS, NFL_TEAM_IMG_URL, PAGE_HTML, PLAYER_IMG_URL, PLAYER_LIST_URL, PLAYER_STATS_URL, SEASON_STATS_BY_POSITION, TEAM_PRIMARY_COLOR_HEX, WEEKLY_STATS_BY_POSITION
from player import load_player_data, save_player_data
from table import generate_stats_html

# CONFIGURE
load_dotenv()
OBS_HOST = os.getenv("OBS_HOST")
OBS_PORT = os.getenv("OBS_PORT")
OBS_PASSWORD = os.getenv("OBS_PASSWORD")

app = Flask(__name__, static_folder='static')

# Load player list once on startup
player_list = []
queue = []
try:
    resp = http_requests.get(PLAYER_LIST_URL)
    if resp.status_code == 200:
        player_list = resp.json()
except Exception as e:
    print("Error loading players:", e)

market_data = {}
# Helper to fetch and merge market data
def fetch_market_data(url, label):
    try:
        resp = http_requests.get(url)
        if resp.status_code == 200:
            market_players = resp.json()
            for m_player in market_players:
                name_id = m_player.get("name_id")
                if name_id not in market_data:
                    market_data[name_id] = {}
                for field in MARKET_FIELDS:
                    market_data[name_id][label + "_"+ field] = m_player.get(field, "")
        else:
            print(f"Error fetching {label}:", resp.status_code)
    except Exception as e:
        print(f"Exception fetching {label}:", e)

# Fetch all market data sources
fetch_market_data(DYNASTY_DADDY_MARKET_URL, "dynasty")
fetch_market_data(FANTASY_DADDY_MARKET_URL, "fantasy")
fetch_market_data(ADP_DADDY_MARKET_URL, "adp")
fetch_market_data(ADP_DADDY_RD_MARKET_URL, "adp_rd")

# Merge market data into player list
for player in player_list:
    pid = player.get("name_id")
    if pid in market_data:
        player.update(market_data[pid])

player_stats = {}
now = datetime.now()
cur_season = now.year if now.month >= 9 else now.year - 1
try:
    season = cur_season
    while season > cur_season - 3:
        resp = http_requests.get(PLAYER_STATS_URL.replace("SEASON", str(season)))
        if resp.status_code == 200:
            player_stats[season] = resp.json()
            player_stats[season]["season"] = season
        season -= 1
except Exception as e:
    print("Error loading player stats:", e)

weekly_gamelogs = {}
try:
    for week in range(1, 18):
        url = PLAYER_STATS_URL.replace("SEASON", str(cur_season)) + "/" + str(week)
        resp = http_requests.get(url)
        if resp.status_code == 200:
            weekly_gamelogs[week] = resp.json()
except Exception as e:
    print("Error loading player stats:", e)

def get_obs_config():
    # Prefer .env values if available
    if OBS_HOST and OBS_PORT:
        return {
            "host": OBS_HOST,
            "port": int(OBS_PORT),
            "password": OBS_PASSWORD or ""
        }

    # Fallback to session values
    return {
        "host": session.get("obs_host"),
        "port": int(session.get("obs_port", 4455)),
        "password": session.get("obs_password", "")
    }

def hex_to_rgb(color_hex):
    color_hex = color_hex.lstrip("#")
    return tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000") 

def update_obs_player(player):
    config = get_obs_config()
    ws = obs.ReqClient(
        host=config["host"],
        port=config["port"],
        password=config["password"]
    )

    sleeper_id = str(player.get("sleeper_id"))
    stats = player_stats.get(cur_season).get(sleeper_id, {})
    fields = {
        "PlayerName": player['full_name'],
        "PlayerFirstName": player['first_name'],
        "PlayerLastName": player['last_name'],
        "PlayerTeam": player['team'],
        
        "KeepTradeCutSFValue": str(player.get('sf_trade_value', '0')),
        "KeepTradeCut1QBValue": str(player.get('trade_value', '0')),
        "KeepTradeCutSFPosRank": str(player.get('sf_position_rank', '0')),
        "KeepTradeCut1QBPosRank": str(player.get('position_rank', '0')),
        "KeepTradeCutSFRank": str(player.get('sf_overall_rank', '0')),
        "KeepTradeCut1QBRank": str(player.get('overall_rank', '0')),
        
        "DynastyDaddySFValue": str(player.get('dynasty_sf_trade_value', '0')),
        "DynastyDaddy1QBValue": str(player.get('dynasty_trade_value', '0')),
        "DynastyDaddySFPosRank": str(player.get('dynasty_sf_position_rank', '0')),
        "DynastyDaddy1QBPosRank": str(player.get('dynasty_position_rank', '0')),
        "DynastyDaddySFRank": str(player.get('dynasty_sf_overall_rank', '0')),
        "DynastyDaddy1QBCutRank": str(player.get('dynasty_overall_rank', '0')),        

        "FantasyDaddySFValue": str(player.get('fantasy_sf_trade_value', '0')),
        "FantasyDaddy1QBValue": str(player.get('fantasy_trade_value', '0')),
        "FantasyDaddySFPosRank": str(player.get('fantasy_sf_position_rank', '0')),
        "FantasyDaddy1QBPosRank": str(player.get('fantasy_position_rank', '0')),
        "FantasyDaddySFRank": str(player.get('fantasy_sf_overall_rank', '0')),
        "FantasyDaddy1QBRank": str(player.get('fantasy_overall_rank', '0')),

        "ADPDaddy1QBSFValue": str(player.get('adp_sf_trade_value', '0')),
        "ADPDaddy1QBValue": str(player.get('adp_trade_value', '0')),
        "ADPDaddySFPosRank": str(player.get('adp_sf_position_rank', '0')),
        "ADPDaddy1QBPosRank": str(player.get('adp_position_rank', '0')),
        "ADPDaddySFRank": str(player.get('adp_sf_overall_rank', '0')),
        "ADPDaddy1QBRank": str(player.get('adp_overall_rank', '0')),
                
        "ADPDaddyRDSFValue": str(player.get('adp_rd_sf_trade_value', '0')),
        "ADPDaddyRD1QBValue": str(player.get('adp_rd_trade_value', '0')),
        "ADPDaddyRDSFPosRank": str(player.get('adp_rd_sf_position_rank', '0')),
        "ADPDaddyRD1QBPosRank": str(player.get('adp_rd_position_rank', '0')),
        "ADPDaddyRDSFRank": str(player.get('adp_rd_sf_overall_rank', '0')),
        "ADPDaddyRD1QBRank": str(player.get('adp_rd_overall_rank', '0')),

        "PlayerPosition": player.get('position', ''),
        "PlayerAge": str(player.get('age', '')),
        "PlayerExperience": str(player.get('experience', '')),
        "PlayerInjuryStatus": player.get('injury_status') or "Healthy",
        "PlayerDynastyADP": str(player.get('dynasty_daddy_adp', '')),
        "PlayerUnderdogADP": str(player.get('underdog_adp', '')),
        "PlayerAvgADP": str(player.get('avg_adp', '')),
        "PlayerPPRPoints": str(stats.get("pts_ppr", "0")),
        "PlayerTotalHalfPPR": str(stats.get("pts_half_ppr", 0.0)),
        "PlayerTotalPPR": str(stats.get("pts_ppr", 0.0)),
        "PlayerTotalSTD": str(stats.get("pts_std", 0.0)),
        "PlayerPPGHalfPPR": f"{stats.get('pts_half_ppr', 0.0) / stats.get('gp', 1):.2f}",
        "PlayerPPGPPR": f"{stats.get('pts_ppr', 0.0) / stats.get('gp', 1):.2f}",
        "PlayerPPGSTD": f"{stats.get('pts_std', 0.0) / stats.get('gp', 1):.2f}",
        "PlayerReceptions": f"{int(stats.get('rec', 0)):,}",
        "PlayerReceivingYards": f"{int(stats.get('rec_yd', 0)):,}",
        "PlayerReceivingTDs": f"{int(stats.get('rec_td', 0)):,}",
        "PlayerRushingAttempts": f"{int(stats.get('rush_att', 0)):,}",
        "PlayerRushingYards": f"{int(stats.get('rush_yd', 0)):,}",
        "PlayerRushingTDs": f"{int(stats.get('rush_td', 0)):,}",
        "PlayerPassingYards": f"{int(stats.get('pass_yd', 0)):,}",
        "PlayerPassingTDs": f"{int(stats.get('pass_td', 0)):,}",
        "PlayerInterceptions": f"{int(stats.get('int', 0)):,}",
        "PlayerGamesPlayed": f"{int(stats.get('gp', 0)):,}",
        # Add more fields as needed...
    }

    for input_name, text_value in fields.items():
        try:
            ws.set_input_settings(input_name, {"text": text_value}, True)
        except OBSSDKRequestError as e:
            if e.code != 600:
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
        if e.code != 600:
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
        if e.code != 600:
            print(f"⚠️ Error updating PlayerTeamImg source - {str(e)}")
    
    # Team Color Mapping
    current_team_color = TEAM_PRIMARY_COLOR_HEX.get(player['team'], "#FFFFFF")
    r, g, b = hex_to_rgb(current_team_color)
    color_int = (255 << 24) + (b << 16) + (g << 8) + r

    try:
        ws.set_input_settings("PlayerOverlayBox", {
            "color": color_int
        }, overlay=True)
    except OBSSDKRequestError as e:
        if e.code != 600:
            print(f"Warning: Couldn't update color filter - {e}")
    
    season_stats = []
    player_stats.get(cur_season).get(sleeper_id, {})
    for p in player_stats.values():
        if not isinstance(p, dict) or p.get(sleeper_id, {}).get("pts_ppr", None) is None:
            continue
        season_logs = p.get(sleeper_id, {}) 
        season_logs["season"] = p.get("season")
        season_logs["ppg_ppr"] = f"{season_logs.get('pts_ppr', 0.0) / season_logs.get('gp', 1):.2f}"
        season_stats.append(season_logs)
    weekly_logs = []
    for week, p in weekly_gamelogs.items():
        if not isinstance(p, dict) or p.get(sleeper_id, {}).get("pts_ppr", None) is None:
            continue
        weekly_log = p.get(sleeper_id, {}) 
        weekly_log["week"] = week
        weekly_logs.append(weekly_log)
    weekly_logs.reverse()

    save_player_data(season_stats, weekly_logs, player.get("position"), current_team_color)

    # Re-set the URL to force a refresh
    
    try:
        refreshed_url = f"http://127.0.0.1:5000/player_gamelogs_by_season"
        ws.set_input_settings("SeasonGamelogs", {"url": refreshed_url}, overlay=True)
    except OBSSDKRequestError as e:
        if e.code != 600:
            print(f"Warning: Couldn't update SeasonGamelogs - {e}")

    try:
        refreshed_url = f"http://127.0.0.1:5000/player_gamelogs_by_week"
        ws.set_input_settings("WeeklyGamelogs", {"url": refreshed_url}, overlay=True)
    except OBSSDKRequestError as e:
        if e.code != 600:
            print(f"Warning: Couldn't update WeeklyGamelogs - {e}")

def get_queue():
    return session.get("queue", [])

def save_queue(queue):
    session["queue"] = queue

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/", methods=["GET"])
def home():
    # Check if config in session, else redirect to config page
    config = get_obs_config()
    if not config["host"] or not config["port"]:
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
        update_obs_player(player)
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
            update_obs_player(player)
    return redirect(url_for("home"))

@app.route("/clear-queue", methods=["POST"])
def clear_queue():
    session["queue"] = []
    return redirect(url_for("home"))

@app.route("/remove-from-queue/<string:name_id>")
def remove_from_queue(name_id):
    queue = session.get("queue", [])
    if name_id in queue:
        queue.remove(name_id)
        session["queue"] = queue
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

# Route to serve the dynamically generated HTML table
@app.route('/player_gamelogs_by_season')
def serve_player_gamelogs_by_season_table():
    player = load_player_data()
    if player.get("team_color", None) is not None:
        html_output = generate_stats_html(
            player.get("season_stats"),
            fields=SEASON_STATS_BY_POSITION,
            position=player.get("position"),
            team_color=player.get("team_color")
        )
        return render_template_string(html_output)

@app.route('/player_gamelogs_by_week')
def serve_player_gamelogs_by_week_table():
    player = load_player_data()
    if player.get("team_color", None) is not None:
        html_output = generate_stats_html(
            player.get("weekly_stats"),
            fields=WEEKLY_STATS_BY_POSITION,
            position=player.get("position"),
            team_color=player.get("team_color")
        )
        return render_template_string(html_output)

if __name__ == "__main__":
    app.secret_key = "dynasty_daddy_stream_suite"
    threading.Timer(1.0, open_browser).start()
    app.run(port=5000)

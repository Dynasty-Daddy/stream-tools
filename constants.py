PLAYER_IMG_URL = "https://sleepercdn.com/content/nfl/players/thumb/SLEEPER_ID.jpg"
PLAYER_LIST_URL = "https://dynasty-daddy.com/api/v1/player/all/today"
NFL_TEAM_IMG_URL = "https://a.espncdn.com/i/teamlogos/nfl/500/TEAM_ACC.png"
DEFAULT_PLAYER_IMG_URL = "https://www.pff.com/images/webui/player_default.png"

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

IMG_CSS = """
html, body {
  margin: 0 !important;
  padding: 0 !important;
  background: transparent !important;
  overflow: hidden !important;
  height: 100% !important;
  width: 100% !important;
}

img {
  display: block;
  max-width: 100%;
  max-height: 100%;
  background: transparent !important;
}
"""

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
  <li>
    <a href="{{ url_for('select_player', name_id=player['name_id']) }}">{{ player['full_name'] }}</a>
    - <a href="{{ url_for('queue_player', name_id=player['name_id']) }}">Queue</a>
  </li>
{% endfor %}
</ul>

<hr>
<h2>Queued Players</h2>
<ol>
{% for player in queue %}
  <li>{{ player['full_name'] }}</li>
{% endfor %}
</ol>

{% if queue %}
  <form id="nextForm" action="{{ url_for('play_next_player') }}" method="post">
    <button type="submit">▶️ Show Next Player</button>
  </form>
{% endif %}
"""

CONFIG_HTML = """
<!doctype html>
<title>Configure OBS Connection</title>
<h1>OBS Connection Setup</h1>
<form method="post">
  <label for="host">OBS Host:</label>
  <input type="text" id="host" name="host" value="{{ host or '' }}" required><br><br>

  <label for="port">OBS Port:</label>
  <input type="number" id="port" name="port" value="{{ port or 4455 }}" required><br><br>

  <label for="password">OBS Password:</label>
  <input type="password" id="password" name="password" value="{{ password or '' }}"><br><br>

  <button type="submit">Save and Continue</button>
</form>
"""

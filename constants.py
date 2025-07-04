# files
PLAYER_DATA_FILE = 'current_player_data.json'

# urls
PLAYER_IMG_URL = "https://sleepercdn.com/content/nfl/players/thumb/SLEEPER_ID.jpg"
PLAYER_LIST_URL = "https://dynasty-daddy.com/api/v1/player/all/today"
DYNASTY_DADDY_MARKET_URL = "https://dynasty-daddy.com/api/v1/player/all/market/14"
FANTASY_DADDY_MARKET_URL = "https://dynasty-daddy.com/api/v1/player/all/market/15"
ADP_DADDY_MARKET_URL = "https://dynasty-daddy.com/api/v1/player/all/market/6"
ADP_DADDY_RD_MARKET_URL = "https://dynasty-daddy.com/api/v1/player/all/market/7"
NFL_TEAM_IMG_URL = "https://a.espncdn.com/i/teamlogos/nfl/500/TEAM_ACC.png"
DEFAULT_PLAYER_IMG_URL = "https://www.pff.com/images/webui/player_default.png"
PLAYER_STATS_URL = "https://api.sleeper.app/v1/stats/nfl/regular/SEASON"

MARKET_FIELDS = ["trade_value", "sf_trade_value", "position_rank", "sf_position_rank", "sf_overall_rank", "overall_rank"]

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

SEASON_STATS_BY_POSITION = {
    "QB": [
        ("Season", "season"),
        ("Games", "gp"),
        ("PPR Points", "pts_ppr"),
        ("PPG (PPR)", "ppg_ppr"),
        ("Pass Yds", "pass_yd"),
        ("Pass TDs", "pass_td"),
        ("Ints", "pass_int"),
        ("Rush Att", "rush_att"),
        ("Rush Yds", "rush_yd"),
        ("Rush TDs", "rush_td"),
        ("Sacks", "pass_sack")
    ],
    "RB": [
        ("Season", "season"),
        ("Games", "gp"),
        ("PPR Points", "pts_ppr"),
        ("PPG (PPR)", "ppg_ppr"),
        ("Rush Att", "rush_att"),
        ("Rush Yds", "rush_yd"),
        ("Rush TDs", "rush_td"),
        ("Rec", "rec"),
        ("Rec Yds", "rec_yd"),
        ("Rec TDs", "rec_td"),
    ],
    "WR": [
        ("Season", "season"),
        ("Games", "gp"),
        ("PPR Points", "pts_ppr"),
        ("PPG (PPR)", "ppg_ppr"),
        ("Rec", "rec"),
        ("Rec Yds", "rec_yd"),
        ("Rec TDs", "rec_td"),
    ],
    "TE": [
        ("Season", "season"),
        ("Games", "gp"),
        ("PPR Points", "pts_ppr"),
        ("PPG (PPR)", "ppg_ppr"),
        ("Rec", "rec"),
        ("Rec Yds", "rec_yd"),
        ("Rec TDs", "rec_td"),
    ],
}

WEEKLY_STATS_BY_POSITION = {
    "QB": [
        ("Week", "week"),
        ("PPR Points", "pts_ppr"),
        ("Pass Yds", "pass_yd"),
        ("Pass TDs", "pass_td"),
        ("Ints", "pass_int"),
        ("Rush Att", "rush_att"),
        ("Rush Yds", "rush_yd"),
        ("Rush TDs", "rush_td"),
        ("Sacks", "pass_sack")
    ],
    "RB": [
        ("Week", "week"),
        ("PPR Points", "pts_ppr"),
        ("Rush Att", "rush_att"),
        ("Rush Yds", "rush_yd"),
        ("Rush TDs", "rush_td"),
        ("Rec", "rec"),
        ("Rec Yds", "rec_yd"),
        ("Rec TDs", "rec_td"),
    ],
    "WR": [
        ("Week", "week"),
        ("PPR Points", "pts_ppr"),
        ("Rec", "rec"),
        ("Rec Yds", "rec_yd"),
        ("Rec TDs", "rec_td"),
    ],
    "TE": [
        ("Week", "week"),
        ("PPR Points", "pts_ppr"),
        ("Rec", "rec"),
        ("Rec Yds", "rec_yd"),
        ("Rec TDs", "rec_td"),
    ],
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
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Stream Suite | Dynasty Daddy</title>
  <link rel="icon" href="/static/favicon.png" type="image/png">
  <style>
    body {
      font-family: 'Segoe UI', sans-serif;
      background: #f9fafb;
      color: #1f2937;
      max-width: 700px;
      margin: 4rem auto 2rem; /* add top margin for header space */
      padding: 2rem;
      border-radius: 12px;
      background-color: white;
      box-shadow: 0 4px 12px rgb(0 0 0 / 0.1);
      position: relative;
      z-index: 0;
    }

    /* New header styles */
    header {
      position: fixed;
      top: 0;
      left: 50%;
      transform: translateX(-50%);
      width: 700px;
      max-width: 95vw;
      background-color: #1d4ed8;
      color: white;
      padding: 1rem 2rem;
      border-radius: 0 0 12px 12px;
      box-shadow: 0 4px 12px rgb(0 0 0 / 0.15);
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-weight: 700;
      font-size: 1.25rem;
      z-index: 1000;
    }

    header nav a {
      color: #bfdbfe;
      margin-left: 1rem;
      font-weight: 500;
      font-size: 1rem;
      text-decoration: none;
      transition: color 0.2s ease;
    }

    header nav a:hover {
      color: #93c5fd;
      text-decoration: underline;
    }

    h1, h2 {
      text-align: center;
      color: #2c3e50;
    }

    form {
      display: flex;
      justify-content: center;
      gap: 1rem;
      margin-bottom: 1.5rem;
    }

    input[type="text"] {
      padding: 0.5rem;
      font-size: 1rem;
      width: 60%;
      border: 1px solid #ccc;
      border-radius: 4px;
    }

    button {
      padding: 0.5rem 1rem;
      font-size: 1rem;
      background-color: #3498db;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }

    button:hover {
      background-color: #2980b9;
    }

    ul, ol {
      list-style-type: none;
      padding: 0;
    }

    li {
      padding: 0.5rem 0;
      border-bottom: 1px solid #eee;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 1rem;
    }

    .player-info {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      flex-wrap: wrap;
      flex-grow: 1;
    }

    .position-pill {
      background-color: #e0f0ff;
      color: #007acc;
      font-weight: 600;
      font-size: 0.85rem;
      padding: 0.15rem 0.5rem;
      border-radius: 12px;
      white-space: nowrap;
    }

    .team-pill {
      background-color: #f0e5ff;
      color: #7b3cff;
      font-weight: 600;
      font-size: 0.85rem;
      padding: 0.15rem 0.5rem;
      border-radius: 12px;
      white-space: nowrap;
      text-transform: uppercase;
    }

    a {
      color: #3498db;
      text-decoration: none;
      font-weight: 600;
    }

    a:hover {
      text-decoration: underline;
    }

    hr {
      margin: 2rem 0;
    }

    .queue-section {
      margin-bottom: 2rem;
    }

    #nextForm {
      display: flex;
      justify-content: center;
      gap: 1rem;
      margin-top: 1rem;
    }

    #nextForm button,
    #clearQueueBtn {
      background-color: #2ecc71;
      padding: 0.5rem 1rem;
      font-size: 1rem;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }

    #nextForm button:hover,
    #clearQueueBtn:hover {
      background-color: #27ae60;
    }

    .remove-link {
      color: #e74c3c;
      cursor: pointer;
      font-weight: 600;
      margin-left: 1rem;
      text-decoration: none;
    }

    .remove-link:hover {
      text-decoration: underline;
    }
  </style>
</head>
<body>
  <header>
    <div style="display: flex; align-items: center; gap: 0.5rem;">
      <img src="/static/favicon.png" alt="favicon" style="width: 24px; height: 24px;">
      <span>Dynasty Daddy Stream Suite</span>
    </div>
    <nav style="display: flex; align-items: center;">
      <a href="https://github.com/Dynasty-Daddy/stream-tools#readme" target="_blank" rel="noopener noreferrer">How to use</a>
      <a href="https://dynasty-daddy.com" target="_blank" rel="noopener noreferrer">Dynasty Daddy</a>
      <a href="/config" title="Configuration" style="font-size: 1.25rem; margin-left: 1.25rem;">⚙️</a>
    </nav>
  </header>


  {% if queue %}
    <div class="queue-section">
      <h2>Queued Players</h2>
      <ol>
        {% for player in queue %}
          <li style="{% if loop.index0 == 0 %}background-color: #dff0d8; border-left: 5px solid #4CAF50; padding-left: 1rem; position: relative;{% else %}background: none;{% endif %}">
            <div class="player-info">
              {% if loop.index0 == 0 %}
                <span style="position: absolute; left: -80px; top: 50%; transform: translateY(-50%); 
                            background-color: #4CAF50; color: white; padding: 0.25rem 0.5rem; border-radius: 4px; font-weight: bold; font-size: 0.85rem;">
                  Up Next
                </span>
              {% endif %}
              <span class="position-pill">{{ player['position'] }}</span>
              <span class="team-pill">{{ player['team'] }}</span>
              <span>{{ player['full_name'] }}</span>
            </div>
            <div>
              <a href="{{ url_for('remove_from_queue', name_id=player['name_id']) }}" class="remove-link" title="Remove from queue">✖ Remove</a>
            </div>
          </li>
        {% endfor %}
      </ol>

      <form id="nextForm" action="{{ url_for('play_next_player') }}" method="post">
        <button type="submit">▶️ Show Next Player</button>
      </form>

      <hr>
    </div>
  {% endif %}

  <h1>Player Overlay Control</h1>
  <form method="get">
      <input type="text" name="q" value="{{ query }}" placeholder="Search name..." autofocus>
      <button type="submit">Search</button>
  </form>

  <ul>
  {% for player in players %}
    <li>
      <div class="player-info">
        <span class="position-pill">{{ player['position'] }}</span>
        <span class="team-pill">{{ player['team'] }}</span>
        <span>{{ player['full_name'] }}</span>
      </div>
      <div>
        <a href="{{ url_for('select_player', name_id=player['name_id']) }}">Show</a> |
        <a href="{{ url_for('queue_player', name_id=player['name_id']) }}">Queue</a>
      </div>
    </li>
  {% endfor %}
  </ul>

</body>
</html>
"""

CONFIG_HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Stream Suite | Dynasty Daddy</title>
  <link rel="icon" href="/static/favicon.png" type="image/png">
  <style>
    body {
      font-family: 'Segoe UI', sans-serif;
      background: #f9f9f9;
      color: #333;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
    }

        /* New header styles */
    header {
      position: fixed;
      top: 0;
      left: 50%;
      transform: translateX(-50%);
      width: 700px;
      max-width: 95vw;
      background-color: #1d4ed8;
      color: white;
      padding: 1rem 2rem;
      border-radius: 0 0 12px 12px;
      box-shadow: 0 4px 12px rgb(0 0 0 / 0.15);
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-weight: 700;
      font-size: 1.25rem;
      z-index: 1000;
    }

    header nav a {
      color: #bfdbfe;
      margin-left: 1rem;
      font-weight: 500;
      font-size: 1rem;
      text-decoration: none;
      transition: color 0.2s ease;
    }

    header nav a:hover {
      color: #93c5fd;
      text-decoration: underline;
    }

    .config-container {
      background: #fff;
      padding: 2rem 3rem;
      border-radius: 12px;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
      max-width: 400px;
      width: 100%;
    }

    h1 {
      text-align: center;
      color: #2c3e50;
      margin-bottom: 1.5rem;
    }

    label {
      display: block;
      margin-bottom: 0.25rem;
      font-weight: 600;
    }

    input[type="text"],
    input[type="number"],
    input[type="password"] {
      width: 100%;
      padding: 0.5rem;
      margin-bottom: 1.25rem;
      border: 1px solid #ccc;
      border-radius: 6px;
      font-size: 1rem;
    }

    button {
      width: 100%;
      padding: 0.75rem;
      background-color: #3498db;
      border: none;
      border-radius: 6px;
      color: white;
      font-size: 1rem;
      font-weight: bold;
      cursor: pointer;
      transition: background 0.3s ease;
    }

    button:hover {
      background-color: #2980b9;
    }
  </style>
</head>
<body>
  <header>
    <div style="display: flex; align-items: center; gap: 0.5rem;">
      <img src="/static/favicon.png" alt="favicon" style="width: 24px; height: 24px;">
      <span>Dynasty Daddy Stream Suite</span>
    </div>
    <nav style="display: flex; align-items: center;">
      <a href="https://github.com/Dynasty-Daddy/stream-tools#readme" target="_blank" rel="noopener noreferrer">How to use</a>
      <a href="https://dynasty-daddy.com" target="_blank" rel="noopener noreferrer">Dynasty Daddy</a>
    </nav>
  </header>


  <div class="config-container">
    <a href="/" style="display: inline-block; margin-bottom: 1rem; color: #3498db; text-decoration: none; font-weight: 600;">
      ← Back to Home
    </a>
    <h1>OBS Connection Setup</h1>
    <form method="post">
      <label for="host">OBS Host:</label>
      <input type="text" id="host" name="host" value="{{ host or '' }}" required>

      <label for="port">OBS Port:</label>
      <input type="number" id="port" name="port" value="{{ port or 4455 }}" required>

      <label for="password">OBS Password:</label>
      <input type="password" id="password" name="password" value="{{ password or '' }}">

      <button type="submit">Save and Continue</button>
    </form>
  </div>
</body>
</html>
"""

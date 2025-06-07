
# 🎮 OBS Player Overlay Updater

A simple Python tool that connects to OBS using WebSocket and dynamically updates:

- Player name, team, and stats (text sources)  
- Player image (image source)  
- Overlay background color (via hex code from API using a color filter)  

Perfect for fantasy football, live streams, or sports podcasts!

---

## ✅ Requirements

### 1. OBS Setup

- Install OBS Studio: https://obsproject.com/  
- Install OBS WebSocket Plugin: https://github.com/obsproject/obs-websocket/releases  
  (If you're using OBS 28+, WebSocket is built-in)

Then:

1. Open OBS  
2. Go to **Tools → WebSocket Server Settings**  
3. Enable WebSocket server  
4. Note the port (default: 4455) and password

---

### 2. Install Python & Packages

Make sure you have Python 3.8+ installed.

Install required packages:

```
pip install obs-websocket-py requests
```

---

## 🎯 OBS Scene Setup

Create the following sources in your OBS scene **with exact names**:

| Source Name        | Type         | Description                             |
|--------------------|--------------|-----------------------------------------|
| PlayerNameText     | Text (GDI+)  | Shows player name                       |
| PlayerTeamText     | Text (GDI+)  | Shows team name                         |
| PlayerStatsText    | Text (GDI+)  | Shows player stats                      |
| PlayerImage        | Image        | Displays player's image                 |
| OverlayBox         | Color or Image | Used to dynamically change background color |

---

### Add Color Filter to OverlayBox

1. Right-click `OverlayBox` in OBS  
2. Select **Filters**  
3. Click `+` → Add **Color Correction**  
4. Name it **Color Filter**  

---

## 🚀 Running the Script

Update this section of `main.py` with your settings:

```python
OBS_HOST = "localhost"
OBS_PORT = 4455
OBS_PASSWORD = "your_password_here"

PLAYER_LIST_URL = "https://your-api.com/players"
PLAYER_INFO_URL = "https://your-api.com/player/"
```

Then run the script:

```
python main.py
```

You'll see a list of players printed in your terminal.  
Select a number, and the overlay will update in OBS.

---

## 🔄 API Format (Expected)

### GET /players

```json
[
  { "id": "1", "name": "Patrick Mahomes" },
  { "id": "2", "name": "Justin Jefferson" }
]
```

### GET /player/:id

```json
{
  "name": "Patrick Mahomes",
  "team": "Chiefs",
  "stats": "4000 yds / 35 TDs",
  "image": "/path/to/image.png",
  "color": "#FF0000"
}
```

---

## 🔧 Features & Customization

- Updates multiple OBS sources in real-time  
- Changes background color using color filter  
- Easily extend to update more elements or run on a timer  
- Optional: add GUI or auto-refresh mode

---

## 📄 License

MIT License

---

## 🧠 Credits

Built using [OBS WebSocket Python API](https://github.com/Elektordi/obs-websocket-py)

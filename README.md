
# Dynasty Daddy Stream Suite

A simple Python tool that connects to OBS using WebSocket and dynamically updates:

- Player name, team, and stats (text sources)  
- Player image (image source)  
- Overlay background color (via hex code from API using a color filter)  

Perfect for fantasy football, live streams, or sports podcasts!

---

## ✅ Requirements

### OBS Setup

- Install OBS Studio: https://obsproject.com/  
- Install OBS WebSocket Plugin: https://github.com/obsproject/obs-websocket/releases  
  (If you're using OBS 28+, WebSocket is built-in)

Then:

1. Open OBS  
2. Go to **Tools → WebSocket Server Settings**  
3. Enable WebSocket server  
4. Note the port (default: 4455) and password

---

### ⚙️ Configuration with .env File
You can configure the connection to your OBS WebSocket server by creating a `.env` file in the project root directory.

Create `.env` file from the `.env.template`.
Add the following variables:

```
OBS_HOST=localhost
OBS_PORT=4455
OBS_PASSWORD=your_password_here
```

OBS_HOST: The hostname or IP address of your OBS WebSocket server (usually localhost if running locally)
OBS_PORT: The port number of the WebSocket server (default is 4455)
OBS_PASSWORD: The password you set for your OBS WebSocket server (can be empty if no password set)

## 🎯 OBS Scene Setup

Create the following sources in your OBS scene **with exact names**:

| Field Name            | OBS Type | Description                                            |
| --------------------- | ---- | ------------------------------------------------------ |
| PlayerName            | Text (GDI+)   | Full name of the player                                |
| PlayerFirstName       | Text (GDI+)   | Player's first name                                    |
| PlayerLastName        | Text (GDI+)   | Player's last name                                     |
| PlayerTeam            | Text (GDI+)   | Player's team abbreviation (e.g., "NE", "DAL")         |
| PlayerImg             | Browser       | Image of the player                                    |
| PlayerTeamImg         | Browser       | Image of the player's team logo                        |
| PlayerSFValue         | Text (GDI+)   | Sleeper Fantasy trade value                            |
| PlayerValue           | Text (GDI+)   | General trade value                                    |
| PlayerSFPosRank       | Text (GDI+)   | Sleeper Fantasy position rank                          |
| PlayerPosRank         | Text (GDI+)   | Position rank                                          |
| PlayerSFRank          | Text (GDI+)   | Sleeper Fantasy overall rank                           |
| PlayerRank            | Text (GDI+)   | Overall player rank                                    |
| PlayerPosition        | Text (GDI+)   | Player's position (e.g., "QB", "RB")                   |
| PlayerAge             | Text (GDI+)   | Player's age                                           |
| PlayerExperience      | Text (GDI+)   | Years of experience in the league                      |
| PlayerInjuryStatus    | Text (GDI+)   | Injury status (e.g., "Healthy", "Out", "Questionable") |
| PlayerDynastyADP      | Text (GDI+)   | Dynasty ADP (Average Draft Position)                   |
| PlayerUnderdogADP     | Text (GDI+)   | Underdog ADP                                           |
| PlayerAvgADP          | Text (GDI+)   | Average ADP across platforms                           |
| PlayerPPRPoints       | Text (GDI+)   | Total PPR fantasy points                               |
| PlayerTotalHalfPPR    | Text (GDI+)   | Total Half-PPR fantasy points                          |
| PlayerTotalPPR        | Text (GDI+)   | Total PPR fantasy points                               |
| PlayerTotalSTD        | Text (GDI+)   | Total Standard scoring fantasy points                  |
| PlayerPPGHalfPPR      | Text (GDI+)   | Average fantasy points per game (Half-PPR)             |
| PlayerPPGPPR          | Text (GDI+)   | Average fantasy points per game (PPR)                  |
| PlayerPPGSTD          | Text (GDI+)   | Average fantasy points per game (Standard)             |
| PlayerReceptions      | Text (GDI+)   | Total receptions                                       |
| PlayerReceivingYards  | Text (GDI+)   | Total receiving yards                                  |
| PlayerReceivingTDs    | Text (GDI+)   | Total receiving touchdowns                             |
| PlayerRushingAttempts | Text (GDI+)   | Total rushing attempts                                 |
| PlayerRushingYards    | Text (GDI+)   | Total rushing yards                                    |
| PlayerRushingTDs      | Text (GDI+)   | Total rushing touchdowns                               |
| PlayerPassingYards    | Text (GDI+)   | Total passing yards                                    |
| PlayerPassingTDs      | Text (GDI+)   | Total passing touchdowns                               |
| PlayerInterceptions   | Text (GDI+)   | Total interceptions                                    |
| PlayerGamesPlayed     | Text (GDI+)   | Total games played                                     |

---

### Add Color Filter to OverlayBox

1. Right-click `OverlayBox` in OBS  
2. Select **Filters**  
3. Click `+` → Add **Color Correction**  
4. Name it **Color Filter**  

---

## Development

1. (Optional) Create and activate a virtual environment  
2. Install dependencies: `pip install -r requirements.txt`  
3. Build a standalone executable with:

```bash
pyinstaller --onefile app.py
```

## 📄 License

MIT License

---

## 🧠 Credits

Built using [OBS WebSocket Python API](https://github.com/Elektordi/obs-websocket-py)

import requests
import json
import os
from datetime import datetime, timezone

# ===== CONFIG =====
COC_API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImExNDk0MDY2LTNlNzYtNGIzMi05ZDEwLWMzMTljYWYyZDUzMyIsImlhdCI6MTc2ODk4MDQyOSwic3ViIjoiZGV2ZWxvcGVyLzFkZjk0ZmExLTUyMWEtOWU4NC1kY2ZkLThjMzU3OThhMThjMSIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjkxLjE0MC4yNC4yOCJdLCJ0eXBlIjoiY2xpZW50In1dfQ.D7VHc2ZdD1liQEva28uyFL309_Pk1W1RZsxDKCEBJ846jBjH9P4VGf6q4G6orvv3MnpO5-ndqfbeh18mZ1DOcw"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1463424384675872811/t22hbwaPyZZGXCUcMCgMOsNa9WCBXfQhUdnzpS8v74Nj0nyzOBg2lq5Qmzozq-_48S8S"

LOCATION_ID = "32000097"  # Greece
LEGEND_TROPHIES = 4700
MAX_PLAYERS = 100
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "previous_ranks.json")
dt = datetime.now(timezone.utc)
today = f"{dt.strftime('%B')} {dt.day}, {dt.year}"
# ==================

headers = {
    "Authorization": f"Bearer {COC_API_TOKEN}"
}

# --- Load yesterday's data ---
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        previous_data = json.load(f)
else:
    previous_data = {}

# --- Fetch Greek players ---
url = f"https://api.clashofclans.com/v1/locations/{LOCATION_ID}/rankings/players"
response = requests.get(url, headers=headers)
response.raise_for_status()

items = response.json().get("items", [])

# --- Filter Legend League players ---
legend_players = [p for p in items if p.get("trophies", 0) >= LEGEND_TROPHIES]
players = legend_players[:MAX_PLAYERS]

lines = []
current_data = {}

MAX_NAME_LEN = 20

for index, p in enumerate(players, start=1):
    tag = p["tag"]
    name = p["name"]
    trophies = p["trophies"]
    clan = p["clan"]["name"] if "clan" in p else "No Clan"
    if len(name) > MAX_NAME_LEN:
        name = name[:MAX_NAME_LEN]

    current_data[tag] = index

    # --- Rank change logic ---
    if tag not in previous_data:
        change = "🆕"
    else:
        diff = previous_data[tag] - index
        if diff > 0:
            change = f"↑{diff}"
        elif diff < 0:
            change = f"↓{abs(diff)}"
        else:
            change = "→"

    rank = str(index).rjust(3)  # pads to width 3

    lines.append(
        f"{rank}- {name} | {trophies}"
    )

# --- Save today's data for tomorrow ---
with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(current_data, f, ensure_ascii=False, indent=2)

# Embdeds
fields = []

# Safe chunk size for short lines
CHUNK_SIZE = 20

for i in range(0, len(lines), CHUNK_SIZE):
    fields.append({
        "name": "\u200b",  # invisible title
        "value": "\n".join(lines[i:i + CHUNK_SIZE]),
        "inline": False
    })

embed = {
    "title": f"🏆 Greece Legends Leaderboard for {today} 🇬🇷",
    "color": 0x1ABC9C,
    "fields": fields,
    "timestamp": datetime.now(timezone.utc).isoformat()
}

payload = {"embeds": [embed]}
response = requests.post(DISCORD_WEBHOOK_URL, json=payload)

print("Discord status:", response.status_code)
print("Discord response:", response.text)
print("Total players processed:", len(players))
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

# ========= CONFIG =========
URL = "https://coc-stats.net/en/locations/32000097/players/"
DISCORD_WEBHOOK = os.environ["DISCORD_WEBHOOK"]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

MAX_PLAYERS = 100
# ==========================

# Fetch page
response = requests.get(URL, headers=HEADERS, timeout=30)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

rows = soup.select("table tr")

players = []
seen_tags = set()

for row in rows:
    cols = row.find_all("td")
    if len(cols) < 3:
        continue

    # ---- Player tag (for deduplication) ----
    raw_text = cols[1].get_text(" ", strip=True)
    if "#" not in raw_text:
        continue

    tag = raw_text.split("#")[-1].strip()
    if tag in seen_tags:
        continue
    seen_tags.add(tag)

    # ---- Rank ----
    rank_tag = cols[0].find("h3")
    if not rank_tag:
        continue
    rank = rank_tag.text.split(".")[0].strip()

    # ---- Name ----
    name_tag = cols[1].find("a")
    if not name_tag:
        continue
    name = name_tag.text.strip()

    # ---- Trophies ----
    trophies_text = cols[2].get_text(strip=True)
    trophies = "".join(c for c in trophies_text if c.isdigit())

    players.append(f"{rank}. {name} | {trophies}")

    if len(players) >= MAX_PLAYERS:
        break

# ---- Build embed ----
today = datetime.now().strftime("%B %d")

embed = {
    "title": f"Greece Legends Leaderboard for {today}",
    "description": "\n".join(players),
    "color": 0xF1C40F
}

payload = {
    "embeds": [embed]
}

# Send to Discord
discord_response = requests.post(DISCORD_WEBHOOK, json=payload)
print("Discord status:", discord_response.status_code)
print(discord_response.text)

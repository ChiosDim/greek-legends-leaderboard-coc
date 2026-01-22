import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from zoneinfo import ZoneInfo

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

URL = "https://brawlace.com/coc/leaderboards/players?locationId=32000097"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=HEADERS, timeout=20)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

table = soup.find("table")
if not table:
    raise RuntimeError("Leaderboard table not found")

rows = table.select("tbody tr")

lines = []
for row in rows[:100]:  # top 100 players
    cols = row.find_all("td")
    if len(cols) < 4:
        continue

    rank = cols[0].get_text(strip=True)
    name = cols[1].get_text(strip=True)
    trophies = cols[3].get_text(strip=True)

    lines.append(f"{rank}. {name} | {trophies} 🏆")

description = "\n".join(lines)

# Greece local date
greece_time = datetime.now(ZoneInfo("Europe/Athens"))
date_str = greece_time.strftime("%B %d")

embed = {
    "title": f"Greece Legends Leaderboard for {date_str}",
    "description": description[:4096],  # Discord embed limit
    "color": 0x1ABC9C
}

payload = {
    "embeds": [embed]
}

r = requests.post(DISCORD_WEBHOOK, json=payload)
r.raise_for_status()

print("Greek Legends leaderboard posted successfully")

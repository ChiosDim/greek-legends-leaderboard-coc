# Greece Ranking Leaderboard (Clash of Clans)

This repository contains a Python script that automatically posts the **Greek Legends League leaderboard** to a Discord channel every day.

The data is scraped from a public leaderboard page and formatted into a single Discord embed.

---

## ✨ Features

- Top **100 Greek Legends players**
- One clean Discord embed
- Trophy change vs **previous day** (🟢 ▲ / 🔴 ▼ / ⚪ ▬)
- Footer showing **posting time (Greece time)**
- Runs automatically via **GitHub Actions**
- No Clash API key required

---

## 🕒 Schedule

The bot runs **every day at 06:59 (Greece time)** using GitHub Actions cron scheduling.

You can also trigger it manually from the **Actions** tab.

---


## 🔐 Configuration

The only required secret is:

- `DISCORD_WEBHOOK`  
  Your Discord webhook URL (stored as a **Repository Secret**)

---

## 📁 Files

- `greek_legends.py` → Main script
- `previous_day.json` → Stores yesterday’s trophies for comparison
- `requirements.txt` → Python dependencies
- `.github/workflows/greek_legends.yml` → GitHub Actions workflow

---

## ⚠️ Notes

- Trophy comparison appears starting from the **second run**
- If the source website changes its HTML structure, the scraper may need adjustment
- GitHub Actions cron jobs may run a few minutes late occasionally (normal behavior)

---

## 📜 License

This project is for personal/community use.  
Clash of Clans content is owned by **Supercell**.

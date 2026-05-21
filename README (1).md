# 🚀 The Last Signal — Choose Your Own Adventure

> **MLH Global Hack Week: GenAI 2025**
> Challenge: Use GitHub Copilot / AI to Build a Simple Application

🌐 **Live Demo:** [the-last-signal.onrender.com](https://the-last-signal.onrender.com)

---

## What Is This?

**The Last Signal** is a browser-based Choose Your Own Adventure game built with Python + Flask, assisted by an AI coding assistant (Claude by Anthropic).

You play as the last astronaut aboard a failing space station. Every choice affects your O₂, health, and survival.

---

## Play Online

👉 Visit the live deploy: **https://the-last-signal.onrender.com**

No installation needed — runs in any browser.

---

## Run Locally

**Requirements:** Python 3.7+

```bash
# Install dependencies
pip install -r requirements.txt

# Run the web app
python app.py

# Or run the original CLI version
python3 adventure.py
```

Then open: http://localhost:5000

---

## Features

- 🌐 **Browser playable** — deployed as a Flask web app on Render
- 🎨 **Sci-fi terminal UI** — dark theme, glowing teal accents, Orbitron font
- 📊 **Live stat bars** — O₂ and Health update in real time
- 🔀 **Branching paths** — Engineering Bay vs Science Lab, multiple outcomes
- 🎒 **Inventory system** — find items that unlock better results
- ⭐ **Scoring + ratings** — Perfect Escape ★★★ down to Barely Made It ★
- 🔁 **Replayable** — different choices = different endings

---

## Game Paths

```
START
 ├─ Engineering Bay (shorter, dangerous)
 │   ├─ Have Repair Kit? → Easy clear
 │   ├─ Dash through flames? → Take damage
 │   └─ Go back → Science Lab route
 │
 └─ Science Lab (longer, safer)
     ├─ Search locker? → Find Repair Kit + health restore
     └─ Skip it → Continue to Airlock

AIRLOCK (both paths converge)
 ├─ Manual override → Safe open
 ├─ Hotwire panel → Takes damage, works
 └─ Wait → O₂ drains, forced to retry

ESCAPE POD → SURVIVAL or DEATH
```

---

## Files

```
app.py            ← Flask web app (browser game)
adventure.py      ← Original CLI version
requirements.txt  ← Python dependencies
Procfile          ← Render/Heroku deploy config
render.yaml       ← Render auto-deploy config
README.md         ← This file
```

---

## How AI Was Used

Built using **Claude (Anthropic)** as AI coding assistant:

- Designed the branching scene graph and game state machine
- Built the Flask API backend with session state
- Created the sci-fi terminal UI (HTML/CSS/JS, no frameworks)
- Wrote all narrative text and branching dialogue
- Generated deployment configuration for Render

**Sample prompt:** *"Build a Python Flask web app version of a choose-your-own-adventure CLI game. The player is an astronaut on a dying space station. Include a dark sci-fi UI with stat bars, branching paths, inventory, and scoring."*

---

## Score Guide

| Score | Rating              |
|-------|---------------------|
| 90+   | ★★★ Perfect Escape  |
| 60–89 | ★★ Skilled Survivor |
| <60   | ★ Barely Made It    |

---

*Built for MLH Global Hack Week: GenAI 2025*

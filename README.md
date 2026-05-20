# 🚀 The Last Signal — Choose Your Own Adventure

> **MLH Global Hack Week: GenAI 2025**
> Challenge: Use GitHub Copilot / AI to Build a Simple Application

---

## What Is This?

**The Last Signal** is a terminal-based Choose Your Own Adventure game built in Python with the help of an AI coding assistant (Claude by Anthropic).

You play as the last astronaut aboard a failing space station. A micrometeorite strike has breached the hull, your crewmates are gone, and a single escape pod remains. Every choice you make affects your oxygen, health, and survival.

---

## How to Play

**Requirements:** Python 3.7+

```bash
python3 adventure.py
```

Works on macOS, Linux, and Windows (best in a terminal with ANSI colour support).

---

## Features

- 🎨 **Colourful terminal UI** with ANSI colour codes and live stat bars
- 📊 **Dynamic status display** — O₂, Power, Health bars update each scene
- 🔀 **Branching paths** — multiple routes, each with different consequences
- 🎒 **Inventory system** — find items that unlock better outcomes
- ⭐ **Scoring system** — rated from "Barely Made It" to "Perfect Escape"
- 🔁 **Replayable** — play again with different choices for a different ending

---

## Paths & Outcomes

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

ESCAPE POD → SURVIVAL or DEATH (if O₂/health hits 0)
```

---

## How AI Was Used

This project was built using **Claude (Anthropic)** as an AI coding assistant:

- Designed the full branching scene graph and state machine
- Wrote the ANSI terminal styling helpers and stat bar display
- Created all narrative text and branching dialogue
- Structured the game loop, inventory system, and scoring logic
- Generated and debugged the complete Python implementation

**Sample prompt used:**
> *"Build a Python command-line choose your own adventure game. The player is an astronaut on a dying space station. Include branching paths, an inventory system, ANSI colour output, health/oxygen stats, and a scoring system."*

---

## File Structure

```
adventure.py    ← entire game in one file, no dependencies
README.md       ← this file
```

---

## Score Guide

| Score | Rating |
|-------|--------|
| 90+   | ★★★ Perfect Escape |
| 60–89 | ★★ Skilled Survivor |
| <60   | ★ Barely Made It |

---

*Built for MLH Global Hack Week: GenAI 2025*

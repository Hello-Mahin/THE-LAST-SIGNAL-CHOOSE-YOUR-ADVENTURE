#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║        THE LAST SIGNAL — A Choose Your Own Adventure        ║
║              Built with AI Coding Assistant                  ║
║                   MLH Global Hack Week                       ║
╚══════════════════════════════════════════════════════════════╝

A sci-fi survival adventure. You are the last astronaut on a
dying space station. Every choice matters.
"""

import time
import sys
import os

# ── ANSI colours ────────────────────────────────────────────────────────────
class C:
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    DIM    = "\033[2m"
    RED    = "\033[91m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    CYAN   = "\033[96m"
    WHITE  = "\033[97m"
    MAGENTA= "\033[95m"
    BLUE   = "\033[94m"

# ── Helpers ──────────────────────────────────────────────────────────────────
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def slow_print(text, delay=0.022):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def header():
    print(f"\n{C.CYAN}{C.BOLD}")
    print("  ╔══════════════════════════════════════════════╗")
    print("  ║         T H E   L A S T   S I G N A L       ║")
    print("  ╚══════════════════════════════════════════════╝")
    print(f"{C.RESET}")

def separator():
    print(f"\n{C.DIM}  {'─'*46}{C.RESET}\n")

def narrate(text):
    slow_print(f"\n  {C.WHITE}{text}{C.RESET}", delay=0.018)

def alert(text):
    slow_print(f"\n  {C.RED}{C.BOLD}⚠  {text}{C.RESET}", delay=0.015)

def success(text):
    slow_print(f"\n  {C.GREEN}{C.BOLD}✓  {text}{C.RESET}", delay=0.015)

def info(text):
    slow_print(f"  {C.CYAN}{text}{C.RESET}", delay=0.012)

def choose(options: dict) -> str:
    """Show numbered choices, return chosen key."""
    print()
    for key, label in options.items():
        print(f"  {C.YELLOW}{C.BOLD}[{key}]{C.RESET}  {label}")
    print()
    while True:
        try:
            raw = input(f"  {C.MAGENTA}Your choice ▶  {C.RESET}").strip().upper()
            if raw in options:
                return raw
            print(f"  {C.RED}Enter one of: {', '.join(options.keys())}{C.RESET}")
        except (EOFError, KeyboardInterrupt):
            print(f"\n\n  {C.DIM}Signal lost. Goodbye, astronaut.{C.RESET}\n")
            sys.exit(0)

def pause(seconds=1.2):
    time.sleep(seconds)

# ── Game state ───────────────────────────────────────────────────────────────
class Game:
    def __init__(self):
        self.oxygen   = 100   # %
        self.power    = 100   # %
        self.health   = 100   # %
        self.items    = []
        self.score    = 0
        self.name     = "Astronaut"

    def show_status(self):
        o_bar = self._bar(self.oxygen,  C.CYAN)
        p_bar = self._bar(self.power,   C.YELLOW)
        h_bar = self._bar(self.health,  C.GREEN if self.health > 40 else C.RED)
        separator()
        print(f"  {C.DIM}O₂ {o_bar} {self.oxygen:3d}%   "
              f"Power {p_bar} {self.power:3d}%   "
              f"Health {h_bar} {self.health:3d}%{C.RESET}")
        if self.items:
            print(f"  {C.DIM}Inventory: {', '.join(self.items)}{C.RESET}")
        separator()

    def _bar(self, val, color, length=8):
        filled = round(val / 100 * length)
        return f"{color}{'█'*filled}{'░'*(length-filled)}{C.RESET}"

    def is_alive(self):
        return self.oxygen > 0 and self.health > 0

    def drain(self, oxygen=0, power=0, health=0):
        self.oxygen  = max(0, self.oxygen  - oxygen)
        self.power   = max(0, self.power   - power)
        self.health  = max(0, self.health  - health)

    def restore(self, oxygen=0, power=0, health=0):
        self.oxygen  = min(100, self.oxygen  + oxygen)
        self.power   = min(100, self.power   + power)
        self.health  = min(100, self.health  + health)

    def add_item(self, item):
        if item not in self.items:
            self.items.append(item)
            success(f"Added to inventory: {item}")

    def check_death(self):
        if self.oxygen <= 0:
            return "oxygen"
        if self.health <= 0:
            return "health"
        return None

# ── Scenes ───────────────────────────────────────────────────────────────────

def intro(g: Game):
    clear()
    header()
    slow_print(f"""
  {C.DIM}STATION MERIDIAN-7  |  LOW EARTH ORBIT  |  03:42 UTC{C.RESET}
""", delay=0.01)
    pause(0.5)
    narrate("You jolt awake. Red emergency lights pulse through the cabin.")
    narrate("Alarms blare. A crack spiders across the viewport.")
    narrate("Your crewmates are gone — evacuation pods already launched.")
    narrate("You overslept during a micrometeorite strike.")
    pause(0.5)
    alert("HULL BREACH DETECTED — SECTOR 4")
    alert("OXYGEN NOMINAL — 100%")
    pause(0.6)
    narrate("The station groans. You have minutes, maybe less.")
    narrate("One emergency pod remains — but it's across the station.")

    print(f"\n  {C.CYAN}What is your name, astronaut?{C.RESET}")
    try:
        name = input(f"  {C.MAGENTA}▶  {C.RESET}").strip()
        g.name = name if name else "Astronaut"
    except (EOFError, KeyboardInterrupt):
        g.name = "Astronaut"
    success(f"Copy that, {g.name}. Stay sharp.")
    pause(1.0)

def scene_corridor(g: Game) -> str:
    clear()
    header()
    g.show_status()
    narrate("You're in the main corridor. Two routes to the escape pod:")
    info("Left: Engineering Bay — shorter but fires are reported there.")
    info("Right: Science Lab — longer, O₂ will drop more, but safer.")
    g.drain(oxygen=5)
    choice = choose({"L": "Take the Engineering Bay route", "R": "Take the Science Lab route"})
    return "engineering" if choice == "L" else "science_lab"

def scene_engineering(g: Game) -> str:
    clear()
    header()
    g.show_status()
    narrate("You sprint into Engineering. Flames lick the ceiling.")
    narrate("A fire suppression panel is on the wall — broken, but fixable.")
    g.drain(oxygen=10, health=10)

    if "Repair Kit" in g.items:
        narrate("You pull out the Repair Kit and fix the suppressor in seconds.")
        success("Fire suppressed! Path is clear.")
        g.restore(health=10)
        g.score += 20
        return "airlock"
    else:
        choice = choose({
            "D": "Dash through the flames — take the damage",
            "B": "Go back and try the Science Lab route",
        })
        if choice == "D":
            narrate("You tuck your head and run. The heat is searing.")
            g.drain(health=25)
            alert(f"Health -{25}. You made it through, barely.")
            g.score += 10
            return "airlock"
        else:
            narrate("You retreat. Smoke fills the corridor behind you.")
            g.drain(oxygen=8)
            return "science_lab"

def scene_science_lab(g: Game) -> str:
    clear()
    header()
    g.show_status()
    narrate("The Science Lab is quiet — eerie, actually.")
    narrate("Specimen containers float in zero-G. A locker stands open.")
    g.drain(oxygen=15)

    choice = choose({
        "L": "Search the open locker",
        "S": "Skip it — head straight for the pod",
    })
    if choice == "L":
        narrate("Inside: a Repair Kit and a half-eaten protein bar.")
        g.add_item("Repair Kit")
        g.restore(health=10)
        g.score += 15
        narrate("You pocket them and keep moving.")
    else:
        narrate("No time for detours. You push on.")
    return "airlock"

def scene_airlock(g: Game) -> str:
    clear()
    header()
    g.show_status()
    narrate("The airlock chamber. You can see the escape pod through the glass.")
    narrate("But the airlock control panel is dark — no power.")
    alert("POWER FAILURE — AIRLOCK DOOR OFFLINE")
    g.drain(oxygen=8)

    choice = choose({
        "M": "Find the manual override lever",
        "H": "Try to hotwire the panel directly",
        "W": "Wait and hope power restores",
    })

    if choice == "M":
        narrate("You scan the walls. There! A red lever behind a panel.")
        narrate("You yank it hard. The door shudders open with a hiss.")
        success("Airlock open!")
        g.score += 20
        return "pod"
    elif choice == "H":
        narrate("You strip wires with your fingernails and cross them.")
        narrate("Sparks fly. A small shock jolts your arm.")
        g.drain(health=15)
        alert("Mild electrical shock — but the door opens!")
        g.score += 15
        return "pod"
    else:
        narrate("You wait. The station groans louder.")
        narrate("After thirty agonising seconds, nothing happens.")
        narrate("Oxygen drops faster in the sealed chamber.")
        g.drain(oxygen=20)
        alert("Oxygen critically low. You need to act NOW.")
        return "airlock_retry"

def scene_airlock_retry(g: Game) -> str:
    g.show_status()
    narrate("Desperation sets in. You must open this door.")
    choice = choose({
        "M": "Manual override lever",
        "H": "Hotwire the panel",
    })
    if choice == "M":
        narrate("You find the lever and wrench it open.")
        success("Airlock open!")
        g.score += 10
    else:
        narrate("You hotwire it. Shock, sparks — door opens!")
        g.drain(health=15)
        g.score += 10
    return "pod"

def scene_pod(g: Game) -> str:
    clear()
    header()
    g.show_status()
    narrate("The escape pod is right there. One seat. Your name's on it.")
    narrate("You strap in. Your hands are shaking.")
    narrate("Launch sequence initiates automatically.")
    pause(0.8)
    narrate("COUNTDOWN: 5... 4... 3... 2... 1...")
    pause(1.0)
    success("LAUNCH SUCCESSFUL.")
    pause(0.5)
    narrate("You burst free from the station just as Sector 4 collapses.")
    narrate("Through the porthole, Meridian-7 glows — then breaks apart.")
    narrate("Earth fills your view. Blue. Beautiful. Alive.")
    g.score += 50
    return "ending_survive"

def ending_survive(g: Game):
    clear()
    header()
    separator()
    slow_print(f"\n  {C.GREEN}{C.BOLD}✦  YOU SURVIVED  ✦{C.RESET}", delay=0.05)
    separator()
    narrate(f"Mission Control crackles to life: \"{g.name}, we read you. Welcome home.\"")
    narrate("Re-entry trajectory locked. ETA: 4 hours.")
    narrate("You close your eyes. You made it.")
    print(f"\n  {C.YELLOW}{C.BOLD}FINAL SCORE: {g.score}{C.RESET}")
    print(f"  {C.DIM}Health remaining: {g.health}%   O₂ remaining: {g.oxygen}%{C.RESET}\n")
    _rate_ending(g)

def ending_death(g: Game, cause: str):
    clear()
    header()
    separator()
    slow_print(f"\n  {C.RED}{C.BOLD}✦  SIGNAL LOST  ✦{C.RESET}", delay=0.05)
    separator()
    if cause == "oxygen":
        narrate("Your visor fogs. The world goes grey.")
        narrate("Oxygen: 0%. The last thing you see is Earth, impossibly blue.")
    else:
        narrate("Your body gives out. The station drifts on without you.")
        narrate("Mission Control will wonder what happened for years.")
    print(f"\n  {C.YELLOW}{C.BOLD}FINAL SCORE: {g.score}{C.RESET}")
    print(f"  {C.DIM}Better luck next time, {g.name}.{C.RESET}\n")

def _rate_ending(g: Game):
    if g.score >= 90:
        print(f"  {C.CYAN}Rating: {C.BOLD}PERFECT ESCAPE ★★★{C.RESET}")
        narrate("You navigated every challenge flawlessly. True astronaut material.")
    elif g.score >= 60:
        print(f"  {C.CYAN}Rating: {C.BOLD}SKILLED SURVIVOR ★★{C.RESET}")
        narrate("Close calls, smart decisions. You earned your way home.")
    else:
        print(f"  {C.CYAN}Rating: {C.BOLD}BARELY MADE IT ★{C.RESET}")
        narrate("You survived — but just. Next time, plan ahead.")

def play_again() -> bool:
    print()
    choice = choose({"Y": "Play again", "N": "Exit"})
    return choice == "Y"

# ── Main loop ────────────────────────────────────────────────────────────────
def main():
    while True:
        g = Game()
        intro(g)

        # Scene routing
        scene = "corridor"
        scene_map = {
            "corridor":      scene_corridor,
            "engineering":   scene_engineering,
            "science_lab":   scene_science_lab,
            "airlock":       scene_airlock,
            "airlock_retry": scene_airlock_retry,
            "pod":           scene_pod,
        }

        while scene in scene_map:
            scene = scene_map[scene](g)
            death = g.check_death()
            if death:
                ending_death(g, death)
                break
        else:
            if scene == "ending_survive":
                ending_survive(g)

        if not play_again():
            slow_print(f"\n  {C.DIM}Thanks for playing THE LAST SIGNAL.{C.RESET}\n", delay=0.02)
            break

if __name__ == "__main__":
    main()

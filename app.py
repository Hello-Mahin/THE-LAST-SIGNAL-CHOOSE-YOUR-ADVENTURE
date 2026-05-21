from flask import Flask, request, jsonify, render_template_string
import json

app = Flask(__name__)

# ── Game Logic ────────────────────────────────────────────────────────────────

def new_state(name="Astronaut"):
    return {
        "name": name,
        "oxygen": 100,
        "health": 100,
        "items": [],
        "score": 0,
        "scene": "corridor",
        "log": [],
        "choices": {},
        "game_over": False,
        "won": False,
    }

def bar(val, length=10):
    filled = round(val / 100 * length)
    return "█" * filled + "░" * (length - filled)

def process(state, choice=None):
    """Advance the game state based on current scene + choice."""
    scene  = state["scene"]
    log    = []
    choices = {}

    def say(text, cls="narrate"):
        log.append({"text": text, "cls": cls})

    def alert(text):
        say(text, "alert")

    def ok(text):
        say(text, "ok")

    def drain(o=0, h=0):
        state["oxygen"] = max(0, state["oxygen"] - o)
        state["health"] = max(0, state["health"] - h)

    def restore(o=0, h=0):
        state["oxygen"] = min(100, state["oxygen"] + o)
        state["health"] = min(100, state["health"] + h)

    def add_item(item):
        if item not in state["items"]:
            state["items"].append(item)
            ok(f"🎒 Added to inventory: {item}")

    # ── Death check ─────────────────────────────────────────────────────────
    if state["oxygen"] <= 0:
        say("Your visor fogs. The world goes grey.", "alert")
        say("Oxygen: 0%. The last thing you see is Earth, impossibly blue.", "alert")
        say(f"SIGNAL LOST — Final Score: {state['score']}", "gameover")
        state["game_over"] = True
        return log, {}

    if state["health"] <= 0:
        say("Your body gives out. The station drifts on without you.", "alert")
        say(f"SIGNAL LOST — Final Score: {state['score']}", "gameover")
        state["game_over"] = True
        return log, {}

    # ── Scenes ──────────────────────────────────────────────────────────────
    if scene == "corridor":
        if choice is None:
            say("You're in the main corridor. Two routes to the escape pod:")
            say("Left: Engineering Bay — shorter but fires are reported.", "info")
            say("Right: Science Lab — longer, O₂ will drop more, but safer.", "info")
            choices = {"L": "🔥 Engineering Bay (shorter, dangerous)",
                       "R": "🔬 Science Lab (longer, safer)"}
        elif choice == "L":
            drain(o=5)
            state["scene"] = "engineering"
            return process(state)
        elif choice == "R":
            drain(o=5)
            state["scene"] = "science_lab"
            return process(state)

    elif scene == "engineering":
        if choice is None:
            say("You sprint into Engineering. Flames lick the ceiling.")
            say("A fire suppression panel on the wall — broken, but fixable.")
            drain(o=10, h=10)
            if "Repair Kit" in state["items"]:
                say("You pull out the Repair Kit and fix the suppressor in seconds.")
                ok("Fire suppressed! Path is clear.")
                restore(h=10)
                state["score"] += 20
                state["scene"] = "airlock"
                return process(state)
            else:
                choices = {"D": "🏃 Dash through the flames (take damage)",
                           "B": "↩️  Go back to the Science Lab route"}
        elif choice == "D":
            say("You tuck your head and run. The heat is searing.")
            drain(h=25)
            alert("Health -25. You made it through, barely.")
            state["score"] += 10
            state["scene"] = "airlock"
            return process(state)
        elif choice == "B":
            say("You retreat. Smoke fills the corridor behind you.")
            drain(o=8)
            state["scene"] = "science_lab"
            return process(state)

    elif scene == "science_lab":
        if choice is None:
            say("The Science Lab is quiet — eerie, actually.")
            say("Specimen containers float in zero-G. A locker stands open.")
            drain(o=15)
            choices = {"L": "🔍 Search the open locker",
                       "S": "⏩ Skip it — head straight for the pod"}
        elif choice == "L":
            say("Inside: a Repair Kit and a half-eaten protein bar.")
            add_item("Repair Kit")
            restore(h=10)
            state["score"] += 15
            say("You pocket them and keep moving.")
            state["scene"] = "airlock"
            return process(state)
        elif choice == "S":
            say("No time for detours. You push on.")
            state["scene"] = "airlock"
            return process(state)

    elif scene == "airlock":
        if choice is None:
            say("The airlock chamber. You can see the escape pod through the glass.")
            alert("POWER FAILURE — AIRLOCK DOOR OFFLINE")
            drain(o=8)
            choices = {"M": "🔧 Find the manual override lever",
                       "H": "⚡ Hotwire the panel directly",
                       "W": "⏳ Wait and hope power restores"}
        elif choice == "M":
            say("You scan the walls. There — a red lever behind a panel.")
            say("You yank it hard. The door shudders open with a hiss.")
            ok("Airlock open!")
            state["score"] += 20
            state["scene"] = "pod"
            return process(state)
        elif choice == "H":
            say("You strip wires with your fingernails and cross them.")
            say("Sparks fly. A small shock jolts your arm.")
            drain(h=15)
            alert("Mild electrical shock — but the door opens!")
            state["score"] += 15
            state["scene"] = "pod"
            return process(state)
        elif choice == "W":
            say("You wait. The station groans louder.")
            say("After thirty agonising seconds — nothing.")
            drain(o=20)
            alert("Oxygen critically low. You need to act NOW.")
            state["scene"] = "airlock_retry"
            return process(state)

    elif scene == "airlock_retry":
        if choice is None:
            say("Desperation sets in. You must open this door.")
            choices = {"M": "🔧 Manual override lever",
                       "H": "⚡ Hotwire the panel"}
        elif choice in ("M", "H"):
            if choice == "M":
                say("You find the lever and wrench it open.")
                ok("Airlock open!")
            else:
                say("You hotwire it. Sparks — door opens!")
                drain(h=15)
            state["score"] += 10
            state["scene"] = "pod"
            return process(state)

    elif scene == "pod":
        say("The escape pod is right there. One seat. Your name's on it.")
        say("You strap in. Your hands are shaking.")
        say("COUNTDOWN: 5… 4… 3… 2… 1…", "alert")
        ok("🚀 LAUNCH SUCCESSFUL.")
        say("You burst free from the station just as Sector 4 collapses.")
        say("Earth fills your view. Blue. Beautiful. Alive.")
        state["score"] += 50
        state["scene"] = "ending"
        state["won"] = True

        sc = state["score"]
        if sc >= 90:
            rating = "★★★ PERFECT ESCAPE"
        elif sc >= 60:
            rating = "★★ SKILLED SURVIVOR"
        else:
            rating = "★ BARELY MADE IT"

        say(f"Mission Control: \"{state['name']}, we read you. Welcome home.\"", "ok")
        say(f"FINAL SCORE: {sc}  |  Rating: {rating}", "win")
        choices = {"R": "🔄 Play Again"}

    elif scene == "ending":
        if choice == "R":
            # Reset — keep name
            name = state["name"]
            state.update(new_state(name))
            return process(state)

    state["log"] = log
    state["choices"] = choices
    return log, choices


# ── HTML Template ──────────────────────────────────────────────────────────────
HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Last Signal — Choose Your Adventure</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@700;900&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --bg:      #070d1a;
    --panel:   #0a1428;
    --border:  #1a3a5c;
    --teal:    #00e5ff;
    --cyan:    #29b6f6;
    --gold:    #ffd740;
    --red:     #ff5252;
    --green:   #69f0ae;
    --muted:   #546e7a;
    --text:    #b0bec5;
    --white:   #eceff1;
  }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'Share Tech Mono', monospace;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px 12px 40px;
  }

  header {
    text-align: center;
    margin-bottom: 24px;
    width: 100%;
    max-width: 700px;
  }

  .title {
    font-family: 'Orbitron', sans-serif;
    font-size: clamp(1.4rem, 5vw, 2.4rem);
    font-weight: 900;
    color: var(--teal);
    letter-spacing: 0.12em;
    text-shadow: 0 0 30px rgba(0,229,255,0.45);
    line-height: 1.1;
  }

  .subtitle {
    font-size: 0.78rem;
    color: var(--muted);
    margin-top: 6px;
    letter-spacing: 0.15em;
  }

  .container {
    width: 100%;
    max-width: 700px;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  /* Status bar */
  .status {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 14px 18px;
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 10px;
  }

  .stat-label {
    font-size: 0.68rem;
    color: var(--muted);
    letter-spacing: 0.1em;
    margin-bottom: 4px;
  }

  .stat-bar-wrap {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .bar-track {
    flex: 1;
    height: 7px;
    background: #1a2a3a;
    border-radius: 4px;
    overflow: hidden;
  }

  .bar-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 0.4s ease;
  }

  .bar-o2   { background: var(--teal); }
  .bar-hp   { background: var(--green); }
  .bar-hp.low { background: var(--red); }

  .stat-val {
    font-size: 0.78rem;
    color: var(--white);
    min-width: 34px;
    text-align: right;
  }

  .inventory {
    grid-column: 1 / -1;
    font-size: 0.72rem;
    color: var(--gold);
    margin-top: 2px;
  }

  /* Log */
  .log-box {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 18px 20px;
    min-height: 220px;
    max-height: 340px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 7px;
    scroll-behavior: smooth;
  }

  .log-line { font-size: 0.95rem; line-height: 1.55; }
  .narrate  { color: var(--white); }
  .info     { color: var(--cyan); }
  .alert    { color: var(--red); font-weight: bold; }
  .ok       { color: var(--green); }
  .win      { color: var(--gold); font-weight: bold; font-size: 1.05rem; text-align: center; letter-spacing: 0.05em; }
  .gameover { color: var(--red); font-weight: bold; font-size: 1.05rem; text-align: center; }
  .dim      { color: var(--muted); font-size: 0.82rem; }

  /* Name input */
  .name-form {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 18px 20px;
  }

  .name-form label {
    font-size: 0.9rem;
    color: var(--teal);
    display: block;
    margin-bottom: 10px;
  }

  .name-row {
    display: flex;
    gap: 10px;
  }

  .name-input {
    flex: 1;
    background: #0d1e35;
    border: 1px solid var(--border);
    border-radius: 6px;
    color: var(--white);
    font-family: 'Share Tech Mono', monospace;
    font-size: 1rem;
    padding: 8px 14px;
    outline: none;
    transition: border-color 0.2s;
  }

  .name-input:focus { border-color: var(--teal); }

  /* Choices */
  .choices {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .choice-btn {
    background: transparent;
    border: 1px solid var(--border);
    border-radius: 8px;
    color: var(--white);
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.95rem;
    padding: 13px 18px;
    text-align: left;
    cursor: pointer;
    transition: all 0.18s ease;
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .choice-btn:hover {
    background: rgba(0,229,255,0.07);
    border-color: var(--teal);
    color: var(--teal);
    transform: translateX(4px);
  }

  .choice-btn:active { transform: translateX(2px); opacity: 0.8; }

  .choice-key {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.72rem;
    color: var(--gold);
    background: rgba(255,215,64,0.12);
    border: 1px solid rgba(255,215,64,0.3);
    border-radius: 4px;
    padding: 2px 7px;
    min-width: 28px;
    text-align: center;
    flex-shrink: 0;
  }

  .start-btn {
    background: var(--teal);
    border: none;
    border-radius: 6px;
    color: var(--bg);
    font-family: 'Orbitron', sans-serif;
    font-size: 0.85rem;
    font-weight: 700;
    padding: 9px 22px;
    cursor: pointer;
    letter-spacing: 0.08em;
    transition: opacity 0.2s;
    white-space: nowrap;
  }

  .start-btn:hover { opacity: 0.85; }

  .spinner {
    text-align: center;
    color: var(--muted);
    font-size: 0.85rem;
    padding: 12px 0;
    display: none;
  }

  footer {
    margin-top: 32px;
    font-size: 0.72rem;
    color: var(--muted);
    text-align: center;
    letter-spacing: 0.08em;
  }

  footer a { color: var(--muted); text-decoration: none; }
  footer a:hover { color: var(--teal); }
</style>
</head>
<body>

<header>
  <div class="title">⬡ THE LAST SIGNAL ⬡</div>
  <div class="subtitle">MLH GLOBAL HACK WEEK · GENAI 2025 · CHOOSE YOUR ADVENTURE</div>
</header>

<div class="container">

  <!-- Status -->
  <div class="status" id="status" style="display:none">
    <div>
      <div class="stat-label">O₂ LEVEL</div>
      <div class="stat-bar-wrap">
        <div class="bar-track"><div class="bar-fill bar-o2" id="bar-o2" style="width:100%"></div></div>
        <div class="stat-val" id="val-o2">100%</div>
      </div>
    </div>
    <div>
      <div class="stat-label">HEALTH</div>
      <div class="stat-bar-wrap">
        <div class="bar-track"><div class="bar-fill bar-hp" id="bar-hp" style="width:100%"></div></div>
        <div class="stat-val" id="val-hp">100%</div>
      </div>
    </div>
    <div>
      <div class="stat-label">SCORE</div>
      <div class="stat-bar-wrap" style="justify-content:flex-end">
        <div class="stat-val" id="val-score" style="color:var(--gold);font-size:1.1rem">0</div>
      </div>
    </div>
    <div class="inventory" id="inventory"></div>
  </div>

  <!-- Name form -->
  <div class="name-form" id="name-form">
    <label>📡 INCOMING TRANSMISSION — What is your name, astronaut?</label>
    <div class="name-row">
      <input class="name-input" id="name-input" type="text" placeholder="Enter your name…" maxlength="24" autocomplete="off">
      <button class="start-btn" id="start-btn" onclick="startGame()">LAUNCH</button>
    </div>
  </div>

  <!-- Log -->
  <div class="log-box" id="log-box" style="display:none"></div>

  <!-- Spinner -->
  <div class="spinner" id="spinner">Processing…</div>

  <!-- Choices -->
  <div class="choices" id="choices"></div>

</div>

<footer>
  Built with AI assistance ·
  <a href="https://github.com/Hello-Mahin/THE-LAST-SIGNAL-CHOOSE-YOUR-ADVENTURE" target="_blank">GitHub ↗</a>
  · MLH Global Hack Week: GenAI 2025
</footer>

<script>
  let state = null;

  document.getElementById('name-input').addEventListener('keydown', e => {
    if (e.key === 'Enter') startGame();
  });

  async function startGame() {
    const name = document.getElementById('name-input').value.trim() || 'Astronaut';
    const res = await fetch('/api/start', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name })
    });
    const data = await res.json();
    state = data.state;
    document.getElementById('name-form').style.display = 'none';
    document.getElementById('status').style.display = 'grid';
    document.getElementById('log-box').style.display = 'flex';
    renderLog(data.log);
    renderChoices(data.choices);
    updateStatus();
  }

  async function makeChoice(key) {
    if (!state) return;
    setLoading(true);
    const res = await fetch('/api/choose', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ state, choice: key })
    });
    const data = await res.json();
    state = data.state;
    setLoading(false);
    appendLog(data.log);
    renderChoices(data.choices);
    updateStatus();
  }

  function renderLog(lines) {
    const box = document.getElementById('log-box');
    box.innerHTML = '';
    lines.forEach(l => {
      const div = document.createElement('div');
      div.className = 'log-line ' + l.cls;
      div.textContent = l.text;
      box.appendChild(div);
    });
    box.scrollTop = box.scrollHeight;
  }

  function appendLog(lines) {
    const box = document.getElementById('log-box');
    if (lines.length > 0) {
      const sep = document.createElement('div');
      sep.className = 'log-line dim';
      sep.textContent = '─'.repeat(42);
      box.appendChild(sep);
    }
    lines.forEach(l => {
      const div = document.createElement('div');
      div.className = 'log-line ' + l.cls;
      div.textContent = l.text;
      box.appendChild(div);
    });
    box.scrollTop = box.scrollHeight;
  }

  function renderChoices(choices) {
    const box = document.getElementById('choices');
    box.innerHTML = '';
    for (const [key, label] of Object.entries(choices)) {
      const btn = document.createElement('button');
      btn.className = 'choice-btn';
      btn.innerHTML = `<span class="choice-key">${key}</span><span>${label}</span>`;
      btn.onclick = () => {
        // disable all while loading
        document.querySelectorAll('.choice-btn').forEach(b => b.disabled = true);
        makeChoice(key);
      };
      box.appendChild(btn);
    }
  }

  function updateStatus() {
    if (!state) return;
    const o2 = state.oxygen, hp = state.health;
    document.getElementById('bar-o2').style.width = o2 + '%';
    document.getElementById('val-o2').textContent = o2 + '%';
    document.getElementById('bar-hp').style.width = hp + '%';
    document.getElementById('val-hp').textContent = hp + '%';
    const hpBar = document.getElementById('bar-hp');
    hpBar.classList.toggle('low', hp <= 35);
    document.getElementById('val-score').textContent = state.score;
    const inv = document.getElementById('inventory');
    inv.textContent = state.items.length ? '🎒 ' + state.items.join(', ') : '';

    // Restart on game over / win after a delay
    if ((state.game_over || state.won) && Object.keys(state.choices || {}).length === 0) {
      setTimeout(() => {
        const box = document.getElementById('choices');
        const btn = document.createElement('button');
        btn.className = 'choice-btn';
        btn.innerHTML = '<span class="choice-key">R</span><span>🔄 Play Again</span>';
        btn.onclick = () => {
          state = null;
          document.getElementById('name-form').style.display = 'block';
          document.getElementById('status').style.display = 'none';
          document.getElementById('log-box').style.display = 'none';
          document.getElementById('choices').innerHTML = '';
          document.getElementById('name-input').value = '';
          document.getElementById('name-input').focus();
        };
        box.appendChild(btn);
      }, 600);
    }
  }

  function setLoading(on) {
    document.getElementById('spinner').style.display = on ? 'block' : 'none';
  }
</script>
</body>
</html>
"""

# ── Routes ─────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/api/start", methods=["POST"])
def api_start():
    data = request.get_json()
    name = data.get("name", "Astronaut")[:24]
    state = new_state(name)
    log, choices = process(state)
    state["log"] = []
    return jsonify({"state": state, "log": log, "choices": choices})

@app.route("/api/choose", methods=["POST"])
def api_choose():
    data   = request.get_json()
    state  = data["state"]
    choice = data["choice"]
    log, choices = process(state, choice)
    state["log"] = []
    return jsonify({"state": state, "log": log, "choices": choices})

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)

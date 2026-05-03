import json
from pathlib import Path

SETTINGS_FILE = Path("settings.json")
LEADERBOARD_FILE = Path("leaderboard.json")


DEFAULT_SETTINGS = {
    "sound": True,
    "difficulty": "medium",
    "car_color": "green"
}


def load_settings():
    if not SETTINGS_FILE.exists():
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    try:
        with open(SETTINGS_FILE, "r") as f:
            data = json.load(f)
            return {**DEFAULT_SETTINGS, **data}
    except:
        return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)


def load_leaderboard():
    if not LEADERBOARD_FILE.exists():
        return []

    try:
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def add_score(name, score, distance, coins):
    data = load_leaderboard()

    data.append({
        "name": name,
        "score": int(score),
        "distance": int(distance),
        "coins": int(coins)
    })

    data = sorted(data, key=lambda x: x["score"], reverse=True)[:10]

    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(data, f, indent=4)
"""
Command line runner for the Music Recommender Simulation.

Runs six user profiles through the recommender and prints results:
  - Three standard profiles: High-Energy Pop, Chill Lofi, Deep Intense Rock
  - Three adversarial/edge-case profiles to stress-test scoring logic
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from recommender import load_songs, recommend_songs

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "songs.csv"

# ── Standard profiles ────────────────────────────────────────────────────────
PROFILES = {
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood":  "happy",
        "target_energy":  0.85,
        "target_valence": 0.82,
        "target_tempo":   0.50,
        "likes_acoustic": False,
    },
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood":  "chill",
        "target_energy":  0.38,
        "target_valence": 0.60,
        "target_tempo":   0.15,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood":  "intense",
        "target_energy":  0.92,
        "target_valence": 0.45,
        "target_tempo":   0.75,
        "likes_acoustic": False,
    },

    # ── Adversarial / edge-case profiles ────────────────────────────────────
    # Conflict: wants high energy but a sad mood — these rarely co-occur
    "Sad but Hype": {
        "favorite_genre": "r&b",
        "favorite_mood":  "sad",
        "target_energy":  0.90,
        "target_valence": 0.20,
        "target_tempo":   0.60,
        "likes_acoustic": False,
    },
    # Conflict: extreme acoustic preference but wants high danceability/energy
    "Acoustic Raver": {
        "favorite_genre": "edm",
        "favorite_mood":  "euphoric",
        "target_energy":  0.95,
        "target_valence": 0.90,
        "target_tempo":   0.65,
        "likes_acoustic": True,   # pulls acousticness target to 0.80 — opposite of EDM
    },
    # Edge case: perfectly neutral on everything — should score all songs similarly
    "Completely Neutral": {
        "favorite_genre": "unknown",  # will never match any genre
        "favorite_mood":  "unknown",  # will never match any mood
        "target_energy":  0.50,
        "target_valence": 0.50,
        "target_tempo":   0.50,
        "likes_acoustic": False,      # acousticness target = 0.15
    },
}


def print_profile(name: str, user_prefs: dict, results: list) -> None:
    """Print a formatted recommendation block for one user profile."""
    print()
    print("=" * 62)
    print(f"  PROFILE: {name}")
    print(f"  genre={user_prefs['favorite_genre']}  "
          f"mood={user_prefs['favorite_mood']}  "
          f"energy={user_prefs['target_energy']}  "
          f"acoustic={'yes' if user_prefs['likes_acoustic'] else 'no'}")
    print("=" * 62)

    for rank, (song, score, explanation) in enumerate(results, start=1):
        bar_filled = int(score * 20)
        score_bar = "[" + "#" * bar_filled + "-" * (20 - bar_filled) + "]"

        print(f"\n  #{rank}  {song['title']}  —  {song['artist']}")
        print(f"       Genre: {song['genre']:<12}  Mood: {song['mood']:<10}  "
              f"Energy: {song['energy']:.2f}")
        print(f"       Score: {score:.4f}  {score_bar}")
        print("       Why:")
        for reason in explanation.split(" | "):
            print(f"         • {reason}")

    print()
    print("=" * 62)


def main() -> None:
    songs = load_songs(str(DATA_PATH))

    for name, prefs in PROFILES.items():
        results = recommend_songs(prefs, songs, k=5)
        print_profile(name, prefs, results)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        traceback.print_exc()

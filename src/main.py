"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from recommender import load_songs, recommend_songs

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "songs.csv"


def main() -> None:
    songs = load_songs(str(DATA_PATH))

    # Starter example profile
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood":  "happy",
        "target_energy":  0.80,
        "target_valence": 0.80,
        "target_tempo":   0.50,
        "likes_acoustic": False,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    # ── Header ──────────────────────────────────────────────────────────────
    print()
    print("=" * 60)
    print("  MUSIC RECOMMENDER — Top 5 Picks")
    print("=" * 60)
    print(f"  Profile: genre={user_prefs['favorite_genre']}  "
          f"mood={user_prefs['favorite_mood']}  "
          f"energy={user_prefs['target_energy']}")
    print("=" * 60)

    # ── Results ─────────────────────────────────────────────────────────────
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
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
    print("=" * 60)
    print()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        traceback.print_exc()

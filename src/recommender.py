import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py

    Algorithm Recipe (max possible = 7.00 points):
      +2.00  genre match         (categorical exact match)
      +1.50  mood match          (categorical exact match)
      +1.50  energy proximity    (1 - |target - song|)
      +1.00  acousticness proximity
      +0.75  valence proximity
      +0.25  tempo proximity     (tempo_bpm normalized to 0-1 first)

    Returns:
        (normalized_score, reasons)  where normalized_score is in [0.0, 1.0]
    """
    MAX_SCORE = 7.00
    score = 0.0
    reasons = []

    # --- Categorical: genre match (+2.00) ---
    if song["genre"] == user_prefs.get("favorite_genre", ""):
        score += 2.00
        reasons.append(f"genre match '{song['genre']}' (+2.00)")

    # --- Categorical: mood match (+1.50) ---
    if song["mood"] == user_prefs.get("favorite_mood", ""):
        score += 1.50
        reasons.append(f"mood match '{song['mood']}' (+1.50)")

    # --- Numerical: energy proximity (weight 1.50) ---
    target_energy = user_prefs.get("target_energy", 0.5)
    energy_prox = 1.0 - abs(target_energy - song["energy"])
    score += 1.50 * energy_prox
    reasons.append(f"energy proximity {energy_prox:.2f} (+{1.50 * energy_prox:.2f})")

    # --- Numerical: acousticness proximity (weight 1.00) ---
    acoustic_target = 0.80 if user_prefs.get("likes_acoustic", False) else 0.15
    acoustic_prox = 1.0 - abs(acoustic_target - song["acousticness"])
    score += 1.00 * acoustic_prox
    reasons.append(f"acousticness proximity {acoustic_prox:.2f} (+{1.00 * acoustic_prox:.2f})")

    # --- Numerical: valence proximity (weight 0.75) ---
    target_valence = user_prefs.get("target_valence", 0.5)
    valence_prox = 1.0 - abs(target_valence - song["valence"])
    score += 0.75 * valence_prox
    reasons.append(f"valence proximity {valence_prox:.2f} (+{0.75 * valence_prox:.2f})")

    # --- Numerical: tempo proximity (weight 0.25, normalized to 0-1) ---
    target_tempo = user_prefs.get("target_tempo", 0.17)
    tempo_norm = (song["tempo_bpm"] - 60) / (180 - 60)
    tempo_prox = 1.0 - abs(target_tempo - tempo_norm)
    score += 0.25 * tempo_prox
    reasons.append(f"tempo proximity {tempo_prox:.2f} (+{0.25 * tempo_prox:.2f})")

    normalized = round(score / MAX_SCORE, 4)
    return normalized, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # TODO: Implement scoring and ranking logic
    # Expected return format: (song_dict, score, explanation)
    return []

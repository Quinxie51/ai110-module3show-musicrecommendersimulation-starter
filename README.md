# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world recommenders like Spotify combine two strategies: **collaborative filtering** (finding users with similar taste and borrowing their history) and **content-based filtering** (matching songs by their measurable attributes). This simulation focuses entirely on **content-based filtering** — the system never looks at what other users did. Instead, it builds a profile of what one user prefers (genre, mood, energy level, and acoustic feel) and scores every song by how close its attributes are to those preferences. This approach is transparent, easy to debug, and avoids the "cold start" problem for new songs. The tradeoff is a filter bubble: the system will confidently recommend more of what you already like, but it won't surprise you the way collaborative filtering can.

---

### Song Attributes Used in Scoring

| Feature | Type | Role |
|---|---|---|
| `genre` | categorical | Exact-match bonus — broad style label |
| `mood` | categorical | Exact-match bonus — emotional intent label |
| `energy` | float 0–1 | Proximity-scored against user's target energy |
| `valence` | float 0–1 | Proximity-scored — musical positivity/happiness |
| `danceability` | float 0–1 | Proximity-scored — rhythmic feel |
| `acousticness` | float 0–1 | Proximity-scored — organic vs. electronic texture |
| `tempo_bpm` | float | Normalized to [0–1] then proximity-scored |

### UserProfile Fields

| Field | Type | Purpose |
|---|---|---|
| `favorite_genre` | str | Preferred genre for exact-match scoring |
| `favorite_mood` | str | Preferred mood for exact-match scoring |
| `target_energy` | float | Ideal energy level (0–1); closer songs score higher |
| `likes_acoustic` | bool | Maps to acousticness target (high if True, low if False) |

---

### Algorithm Recipe (Finalized)

The system scores every song on a **0.0–1.0 scale** using additive weighted points, then normalizes by the maximum possible score (7.00).

#### Step 1 — Categorical Matching (exact match = full points, no match = 0)

```
+2.00  genre match    — hard filter; genre is rare in a large catalog, so it earns the most
+1.50  mood match     — intent signal; rewards songs that fit how the user wants to feel
```

Genre earns more than mood because a genre match is statistically rarer (1-in-13 chance across the catalog) and eliminates the most mismatched songs quickly. Mood earns slightly less but still outweighs any single numerical feature, because it captures the user's emotional intent directly.

#### Step 2 — Numerical Proximity Scoring

Each numerical feature is scored using:

```
proximity = 1 - |user_target - song_value|   →  range: 0.0 (opposite) to 1.0 (perfect match)
```

| Feature | Points (× proximity) | Why this weight |
|---|---|---|
| `energy` | × 1.50 | Single strongest perceptual axis — intensity is felt immediately |
| `acousticness` | × 1.00 | Defines sonic texture; separates organic from electronic |
| `valence` | × 0.75 | Emotional tone; partially captured by mood already |
| `tempo_bpm` | × 0.25 | Fine-tuning; correlated with energy, so lower weight avoids double-counting |

`tempo_bpm` is normalized before scoring: `tempo_norm = (bpm - 60) / (180 - 60)`

`acousticness` target is derived from `likes_acoustic`: `0.80` if `True`, `0.15` if `False`

#### Step 3 — Full Formula

```
score = 2.00 × genre_match
      + 1.50 × mood_match
      + 1.50 × energy_proximity
      + 1.00 × acousticness_proximity
      + 0.75 × valence_proximity
      + 0.25 × tempo_proximity

normalized_score = score / 7.00
```

#### Step 4 — Ranking Rule

All songs are scored independently, then **sorted descending by normalized score**. The top K results are returned. Songs with equal scores are ordered by their original catalog position (stable sort).

---

### Expected Biases and Limitations

**1. Genre lock-in (strongest bias)**
With `genre_match` worth 2.00 points out of 7.00 (29% of the maximum), a genre-matching song always has a 0.29 head start over non-matching songs. A jazz ballad that perfectly matches a user's energy, mood, valence, and tempo could still lose to a mediocre pop song just because the genre label matched. This system will consistently under-recommend songs from adjacent genres that the user might actually enjoy.

**2. Mood as a coarse label**
`mood` is a single categorical label chosen by whoever tagged the song. Two songs both labeled "chill" may feel completely different. A track tagged "relaxed" that the user would describe as "chill" gets zero mood points even though the intent is the same. The system has no way to detect near-miss label disagreements.

**3. Acousticness oversimplification**
`likes_acoustic: bool` collapses a nuanced preference into a binary — either targeting 0.80 (acoustic) or 0.15 (electric). A user who enjoys both a lo-fi guitar loop and a clean synth pad will always be penalized on one end. A continuous `target_acousticness` float would be more accurate.

**4. Valence and mood double-count happiness**
High valence and a "happy" mood label are strongly correlated. A happy pop song earns points from both `mood_match` and `valence_proximity`, effectively being rewarded twice for the same attribute. This inflates scores for obviously happy songs and may crowd out nuanced mid-valence tracks.

**5. No diversity enforcement**
The ranking rule is a pure sort — it will happily return 5 lofi tracks in a row if they all outscore everything else. A real recommender would apply a diversity cap (e.g., max 2 songs per genre in the top 5) to prevent the list from feeling repetitive.

---

## Sample Output

Running `python -m src.main` with the default `pop/happy` profile produces:

![Terminal output showing top 5 recommendations for a pop/happy user profile](assets/terminal_output.png)

**Results make sense:**
- **#1 Sunrise City** — full genre + mood match (`pop`/`happy`), energy 0.82 ≈ target 0.80 → score 0.99
- **#2 Gym Hero** — genre match (`pop`), wrong mood (`intense`) → drops to 0.74
- **#3 Groove Pocket** — no genre match but mood match (`happy`) + near-perfect energy → 0.68
- **#5 Concrete Jungle** — no categorical matches at all, ranked purely on numerical proximity

---

## Profile Experiments

The system was tested against six profiles — three standard and three adversarial edge cases designed to stress-test the scoring logic.

### Standard Profiles

**High-Energy Pop** — genre=pop, mood=happy, energy=0.85

![High-Energy Pop recommendations](assets/profile_pop.png)

**Chill Lofi** — genre=lofi, mood=chill, energy=0.38, acoustic=yes

![Chill Lofi recommendations](assets/profile_lofi.png)

**Deep Intense Rock** — genre=rock, mood=intense, energy=0.92

![Deep Intense Rock recommendations](assets/profile_rock.png)

---

### Adversarial / Edge-Case Profiles

These profiles were designed to find weaknesses in the scoring logic.

**"Sad but Hype"** — high energy (0.90) + sad mood — these almost never co-occur in the catalog

![Sad but Hype recommendations](assets/profile_sad_hype.png)

> Expected weakness: no song matches both constraints well. The system is forced to trade off energy score against mood match, revealing which weight dominates.

**"Acoustic Raver"** — EDM genre + `likes_acoustic=True` — EDM songs have acousticness ~0.03, so the acoustic preference directly fights the genre preference

![Acoustic Raver recommendations](assets/profile_acoustic_raver.png)

> Expected weakness: genre match (+2.00) pulls toward EDM, but acousticness proximity pulls toward folk/jazz. The system cannot satisfy both simultaneously.

**"Completely Neutral"** — unknown genre/mood that never matches, all numerical targets at 0.50

![Completely Neutral recommendations](assets/profile_neutral.png)

> Expected behavior: all songs score similarly (~0.40–0.55). Ranking becomes nearly arbitrary — exposing that tie-breaking falls back to catalog order, not any meaningful signal.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

> Full model card: [model_card.md](model_card.md)

### Biggest Learning Moment

The biggest learning moment was not in the code — it was the moment the "Completely Neutral" profile ran and all 18 songs scored between 0.40 and 0.55. Nothing felt recommended. Nothing felt rejected. The list was practically random.

That one test made it obvious that the categorical features — genre and mood — were doing most of the real work in the system. The numerical features (energy, tempo, valence) are good at fine-tuning rankings within a cluster of similar songs, but they cannot strongly separate a great match from a mediocre one on their own. This is a much more general lesson than it first appears: in many machine learning systems, a few high-signal features carry the result, while the rest add marginal refinement. Knowing which features are load-bearing and which are decorative is one of the most important skills in building any prediction system.

### How AI Tools Helped — and When to Double-Check

AI tools accelerated the early design work significantly. Explaining the difference between collaborative and content-based filtering, generating the initial weight rationale, drafting the bias analysis, and suggesting adversarial test profiles all happened faster than they would have through documentation alone. The tools were most useful when the task was generating options or explaining tradeoffs — situations where having a first draft to react to is faster than starting from zero.

The moments that required the most double-checking were the ones involving the actual running code. The import path bug (`from recommender import` failing silently under `python -m src.main`) is a good example: AI tools suggested the fix confidently, but the fix needed to be verified against the real project structure and Python module resolution rules — not just accepted on trust. The same was true for the normalization math. When the weights changed (energy doubled, genre halved), the MAX_SCORE denominator had to be recalculated manually to confirm scores would still fall between 0.0 and 1.0. AI reasoning about math is usually right but always worth checking with a concrete example.

The general rule that emerged: trust AI tools for *design and explanation*, verify them for *execution and correctness*.

### What Was Surprising About Simple Algorithms Feeling Like Recommendations

The most surprising thing was how quickly a short list of weighted rules started producing output that felt meaningful. Running `Sunrise City` at the top of the Happy Pop list and `Library Rain` at the top of the Chill Lofi list — these felt right, in the same way a friend's recommendation feels right. But the entire logic behind it was six multiplication steps and a sort. No neural network, no listening history, no understanding of what music actually sounds like.

This is both encouraging and unsettling. Encouraging because it means a transparent, inspectable system can produce genuinely useful output without complexity. Unsettling because it means users might trust the output more than they should. A song that scores 0.97 feels like a confident, intelligent recommendation — but it just means six numbers happened to line up. The system has no idea whether the user will actually enjoy the song. It only knows the attributes match on paper.

The gap between "scoring well" and "being a good recommendation" is exactly where human judgment still matters. A person who knows music knows that `Gym Hero` by Max Pulse is a workout track that would feel jarring during a quiet evening even if all its genre and energy numbers match a "happy pop" profile. The algorithm sees matching numbers. A human hears the vibe.

### What Would Come Next

**1. Add a listening history layer.** Right now every run starts fresh with no memory. A real improvement would store which songs a user has already heard (or skipped) and penalize repeated recommendations. Even a simple "don't recommend the same song twice in a row" rule would make the output feel more dynamic.

**2. Experiment with collaborative filtering on top.** The current system is purely content-based — it never looks at what other users liked. Adding even a small collaborative component (if two users have similar profiles, share their top-rated songs) would allow the system to surface songs the user never would have described in their preferences but that statistically similar users loved. This is how Spotify's "Discover Weekly" introduces genuinely new music rather than just more of the same.

**3. Make the weights learnable.** Right now the weights (genre=2.00, energy=1.50, etc.) were chosen by reasoning and experimentation. A next step would be to collect feedback — even simulated feedback like "thumbs up / thumbs down" — and use it to adjust the weights automatically toward whatever produces higher satisfaction. This is the bridge between a hand-crafted scoring rule and a machine learning model.

---

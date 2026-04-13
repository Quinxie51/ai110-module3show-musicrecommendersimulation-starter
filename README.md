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

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"


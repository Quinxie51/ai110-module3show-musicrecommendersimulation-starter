# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

A content-based music recommender that scores songs against a user's taste profile and returns the closest matches.

---

## 2. Goal / Task

VibeFinder tries to answer one question: *"Given what a user tells us they like, which songs in the catalog fit them best?"*

It is not trying to predict what a user will click on or stream next. It is trying to find songs that match a described vibe — a combination of genre, mood, energy level, and acoustic feel. This is for classroom exploration only. It is not designed for real users or production use.

---

## 3. Algorithm Summary

Every song gets a score from 0.0 to 1.0 based on how well it matches the user's preferences. Higher score = better match.

The scoring works in two steps:

**Step 1 — Categorical checks (yes or no):**
- If the song's genre matches the user's preferred genre, it earns bonus points.
- If the song's mood matches the user's preferred mood, it earns bonus points.
- Genre is worth more than mood because genre is rarer to match — there are 13 genres in the catalog and only 18 songs, so a genre match is a strong signal.

**Step 2 — Closeness checks (how near is the song to the target?):**
- For energy, valence, acousticness, and tempo, the system measures the gap between what the user wants and what the song has.
- A smaller gap = more points. A song with energy 0.82 scores higher for a user who wants 0.80 than a song with energy 0.50 does.
- Energy gets the most weight among numerical features because it is the most immediately noticeable quality in music — you feel the intensity within seconds.

All points are added up and divided by the maximum possible score so the final result always falls between 0.0 and 1.0. The top-ranked songs are returned as recommendations.

---

## 4. Data Used

- **Catalog size:** 18 songs (10 starter songs + 8 added to expand genre coverage)
- **Features per song:** genre, mood, energy (0–1), tempo in BPM, valence (0–1), danceability (0–1), acousticness (0–1)
- **Genres covered:** pop, lofi, rock, ambient, jazz, synthwave, indie pop, r&b, hip-hop, classical, edm, country, metal, funk, soul
- **Moods covered:** happy, chill, intense, relaxed, focused, moody, melancholic, energetic, euphoric, sad

**Limits:**
- 18 songs is extremely small. A real recommender works with millions.
- Several moods appear only once (sad, euphoric, melancholic). Users who prefer these moods get fewer strong matches.
- All songs were created for this exercise. They do not reflect real listening data or cultural diversity.
- There are no lyrics, no artist popularity signals, and no listening history — just the numbers in the CSV.

---

## 5. Strengths

- **Clear-preference users get accurate results.** When a user's genre, mood, and energy all align with a real song cluster (like chill lofi or high-energy pop), the top results feel immediately right.
- **Transparent reasoning.** Every recommendation comes with a list of reasons — you can see exactly why each song scored the way it did. Most real recommenders are black boxes. This one is not.
- **No cold start for songs.** A brand new song can be recommended immediately as long as its features are filled in — no listening history needed.
- **Fast and simple.** The entire system runs in under a second on a small catalog, and the logic can be read and understood by anyone.

---

## 6. Limitations and Bias

**Primary weakness: Mood label sparsity creates permanently disadvantaged users.**

The catalog has zero songs labeled `sad` in the original 10 songs, and only one in the full set. A user who prefers `sad` music can earn the mood bonus at most once. A user who prefers `happy` or `chill` can earn it on three or four songs. This is not because sad-music fans have worse taste — it is because the dataset was not built with them in mind. In a real product, this kind of imbalance would mean certain listener types receive consistently worse service, not because the algorithm is unfair in its formula, but because the data it was trained on does not represent them equally.

**Secondary weakness: Extreme-preference users are silently penalized.**

The closeness formula (`1 - gap`) works the same way everywhere on the scale. But a user who wants very low energy (like 0.10) or very high energy (like 0.95) has fewer songs close to their target. The scoring range for these users is compressed — all songs score similarly low — which makes it hard for the system to tell a good match from a bad one. A mid-preference user (energy ≈ 0.50) benefits from more of the catalog being within range, so their recommendations feel sharper and more confident.

**Third weakness: Conflicting preferences are silently resolved by whichever earns more points.**

If a user asks for something contradictory — like high energy and a sad mood — the system does not flag the conflict or try to find a compromise. It just picks the songs that score highest overall. In practice, energy (worth more points) tends to win, and the mood preference quietly disappears from the results. The user has no way of knowing this happened.

---

## 7. Evaluation Process

Six user profiles were tested to evaluate the system's behavior:

| Profile | Type | What it tested |
|---|---|---|
| High-Energy Pop | Standard | Do genre + mood + energy all reinforce each other? |
| Chill Lofi | Standard | Does the system correctly favor slow, acoustic songs? |
| Deep Intense Rock | Standard | Can it identify high-tempo, high-energy songs? |
| Sad but Hype | Adversarial | What happens when energy and mood conflict? |
| Acoustic Raver | Adversarial | What happens when genre and texture conflict? |
| Completely Neutral | Adversarial | What happens when there are no categorical matches? |

**Key findings:**
- Standard profiles produced intuitive results — the system worked as designed for clear-preference users.
- `Gym Hero` (genre=pop, mood=intense) consistently appeared in the Happy Pop top 5 even though its mood was wrong. The genre and energy bonuses were enough to compensate for the missing mood match.
- The Completely Neutral profile scored all 18 songs within a 15-point band (0.40–0.55), showing that categorical features carry most of the meaningful differentiation.
- A weight sensitivity experiment (doubling energy, halving genre) caused cross-genre songs to invade the top results, confirming that the original genre weight was actively preventing genre-irrelevant songs from ranking high.

---

## 8. Intended Use and Non-Intended Use

**Intended use:**
- Classroom demonstration of how content-based filtering works
- Learning how scoring rules translate preferences into rankings
- Exploring how bias enters a system through data imbalance and weight choices

**Not intended for:**
- Real music recommendations to actual listeners
- Any production or commercial application
- Making decisions about which artists or songs to promote
- Representing the full diversity of musical taste or culture

---

## 9. Ideas for Improvement

**1. Replace the boolean `likes_acoustic` with a continuous target.**
Right now, a user is either "acoustic (0.80)" or "not acoustic (0.15)." A float like `target_acousticness: 0.45` would let users who like a mix of both styles express that, and the proximity formula already supports it — only the input needs to change.

**2. Add a diversity cap to the ranking step.**
The current ranking rule is a pure sort — it will return 5 lofi songs in a row if they all outscore everything else. A simple rule like "no more than 2 songs from the same genre in the top 5" would make the output feel less repetitive and surface songs the user might not have considered.

**3. Balance the catalog before comparing users.**
Before scoring, normalize how many songs exist per mood and genre so that rare moods are not structurally disadvantaged. One way to do this: weight the mood match bonus by the inverse frequency of that mood in the catalog. A `sad` mood match would be worth more than a `happy` mood match precisely because sad songs are harder to find — rewarding the system for surfacing them rather than penalizing users for wanting them.

---

## 10. Personal Reflection

Building this recommender made it clear that a scoring formula is only as fair as the data behind it. The math itself was straightforward — add up weighted scores, sort, return the top results. But the real work was noticing where the system behaved in ways that were technically correct but intuitively wrong: a song showing up because it matched a genre label even though the mood was completely off, or a user's preference quietly disappearing because it conflicted with a higher-weighted feature.

The most surprising discovery was how little the numerical features (energy, valence, tempo) could do on their own. When genre and mood matches were removed from the equation — as in the Completely Neutral experiment — all songs clustered within a narrow score band and the rankings felt nearly arbitrary. This mirrors a real challenge in music recommendation: the features that are easiest to measure (BPM, loudness, key) are not the ones that explain why people love a song. The features that matter most — cultural context, personal memory, lyrical meaning — are the hardest to put into a spreadsheet.

# Reflection: Profile Comparisons

Plain-language notes comparing what each pair of profiles revealed about the recommender's behavior.

---

## High-Energy Pop vs. Chill Lofi

These two profiles are almost perfect opposites, and the results reflected that clearly.

The High-Energy Pop profile wants loud, danceable music with a happy mood. The system gave it `Sunrise City` at the top — a bright synth-pop track with high energy and a happy tag. The Chill Lofi profile wants quiet, acoustic, focused music. Its top result was `Library Rain` — a slow, rainy-day lofi track with barely any energy.

What's interesting is that almost no songs appeared in both top-5 lists. The energy target alone (0.85 vs. 0.38) was enough to push the two lists in completely opposite directions, because energy is the highest-weighted numerical feature. This makes sense: in real life, you would never recommend a gym playlist to someone studying for an exam, and the system reflected that correctly.

The one exception: `Groove Pocket` (funk, mood=happy, energy=0.78) appeared in the Pop profile's top 3 because it matched the happy mood and had high energy — even though it's not a pop song. This is the system treating "vibe" correctly even when the genre label doesn't match.

---

## Deep Intense Rock vs. Sad but Hype (Adversarial)

Both profiles want high energy — but for completely different emotional reasons.

The Rock profile wants `mood=intense` and `genre=rock`. Its top result is `Storm Runner`, which makes total sense: it's literally tagged rock/intense, with the highest tempo in the catalog (152 BPM). The system nailed this one.

The Sad but Hype profile is the interesting case. It asks for `energy=0.90` and `mood=sad` at the same time — a combination that almost doesn't exist in music. A sad song is usually slow and quiet. A hype song is usually fast and loud. Our catalog has no songs that are both.

What happened: the system gave the Sad but Hype user mostly high-energy songs (`Iron Veil`, `Drop Zone`, `Gym Hero`) because energy is worth more points than mood. It essentially ignored the "sad" request and just found loud songs. In plain terms: the system understood "loud" but couldn't understand "sad and loud at the same time" because that combination doesn't exist in its training data.

This reveals a real limitation: when a user has contradictory preferences, the system doesn't try to find a compromise — it just picks whichever preference it can score points on, and ignores the rest.

---

## Acoustic Raver vs. Completely Neutral (Adversarial)

These two profiles stress-tested the system from opposite angles.

The Acoustic Raver profile asked for `genre=edm` and `likes_acoustic=True` — essentially "I want electronic music but it should feel warm and organic." These two preferences are almost mutually exclusive: EDM songs are produced electronically and have near-zero acoustic scores, while acoustic instruments produce the opposite. The system's top results were EDM songs with terrible acousticness scores. The genre bonus (+1.00 or +2.00) was simply worth more points than the acousticness penalty, so electronic songs won.

In plain language: imagine telling a music store employee "I want electronic dance music, but make it acoustic." They would be confused — and so was our system, though it didn't say so. It just picked the EDM songs and quietly lost points for acousticness.

The Completely Neutral profile took the opposite approach: no genre or mood preference, all numerical targets at 0.50 (dead center on every scale). This produced the most boring output of all six profiles — a nearly random-looking list where all scores were bunched between 0.41 and 0.55. Nothing felt strongly recommended or strongly rejected.

This matters because it shows that the categorical bonuses (genre and mood) are responsible for most of the meaningful score separation in this system. Without them, numerical features alone cannot tell a great match from a mediocre one. A real recommender would need richer data — or more features — to make strong recommendations for a user who hasn't expressed clear categorical preferences.

---

## Why Does Gym Hero Keep Appearing for Happy Pop Users?

`Gym Hero` is tagged as `mood=intense` — not `mood=happy`. So why does it show up near the top for a user who wants happy pop music?

The short answer: it earns points in enough other categories to compensate.

Here's the breakdown for a Happy Pop user (target energy=0.85, genre=pop):
- `genre=pop` matches → earns the genre bonus (the biggest single point reward)
- `energy=0.93` is very close to the target of 0.85 → earns nearly full energy points
- `valence=0.77` is close to a happy valence target → earns good valence points
- `mood=intense` does NOT match `mood=happy` → earns zero mood points

The mood miss costs 1.50 points. But the genre match + energy match together earn more than enough to make up for it. The system sees a pop song with high energy and a positive sound and puts it near the top — even though a human listener would notice right away that the song feels pushy and intense rather than cheerful.

This reveals something important about how scoring systems work: they add up individual pieces of evidence and pick the highest total score. They don't understand that certain combinations of features define an experience. A human listener knows that "happy pop" means something specific — it should feel light, celebratory, easy. The recommender doesn't know that. It just sees "pop: check, energy: close, valence: decent" and calls it good enough.

---

## Overall Takeaway

The system works well when a user's preferences align with a cluster of songs that are similar on all dimensions at once. It struggles when preferences conflict with each other, or when a user's taste is rare in the catalog. The experiments showed that genre and mood labels do most of the heavy sorting, while numerical features do the fine-tuning within a genre. A system without categorical features would produce much flatter, less useful rankings.

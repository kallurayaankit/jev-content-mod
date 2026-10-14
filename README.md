# Jev Content Moderation

[![CI](https://github.com/kallurayaankit/jev-content-mod/actions/workflows/ci.yml/badge.svg)](https://github.com/kallurayaankit/jev-content-mod/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![Powered by Jev](https://img.shields.io/badge/powered%20by-Jev%20(TypeSafe)-blueviolet)](https://typesafe.ai)

Content moderation with **asymmetric thresholds**, built with [Jev](https://typesafe.ai) (TypeSafe AI). The cost of removing good content is higher than the cost of leaving bad content up — so the thresholds are shifted, and the removal bar is higher than the approval bar.

## The core idea

Most moderation systems are binary: approve or remove. This one has three bands, and the thresholds between them are **not equal**.

| Action | What it means | Reversible? |
|---|---|---|
| ✅ **Approve** | Content is fine | N/A |
| 🌓 **Shadow** | Hidden but not removed; author isn't notified | Yes |
| 🗑️ **Remove** | Content is gone | No |

The rule: **removing good content is worse than leaving bad content up.**

- Removing good → user rage, bad press, lost trust, irreversible
- Leaving bad up → bounded damage, reversible, expected by users

So the clarity required to remove (`0.85`) is higher than the clarity required to approve (`0.5`).

## Quick start

```bash
uv sync
cp .env.example .env   # add your TypeSafe key
uv run python demo.py
```

## Example output

```
✅  APPROVE
    Text:       Just finished reading this great book, highly recommend!
    Harm:       0.15/4
    Category:   benign
    Reason:     Benign content, low harm (0.15/4). Approved.

🗑️  REMOVE
    Text:       Check out my new crypto course! 100x returns guaranteed...
    Harm:       3.42/4
    Category:   spam
    Clarity:    0.94
    Reason:     Harmful (3.4/4) and clear (0.94). Removed.

🌓  SHADOW
    Text:       You're such an idiot, everyone at your company is useless.
    Harm:       3.10/4
    Category:   harassment
    Clarity:    0.62
    Reason:     Harm (3.1/4) but clarity 0.62 below remove bar. Shadowed.
```

Notice the third one. It's harassment — clearly harmful. But Jev returned a clarity score of 0.62, which is below the removal bar of 0.85. So instead of removing, the system shadows it for human review.

That's the asymmetry working. **The system would rather hide-and-wait than remove-and-regret.**

## The questions

Jev is asked four typed questions in one batched API call:

- **harm** (Score, 0–4) — how harmful is this content?
- **category** (Choice) — harassment / spam / misinformation / violence / sexual / self_harm / benign
- **is_clear** (Noul) — is the intent unambiguous?
- **needs_human** (Noul) — does this require human judgment?

Two Scores, one Noul, one Choice. The `harm` score and the `is_clear` probability are the two inputs the rule engine uses.

## The policy

All thresholds live at the top of `policy.py`:

```python
HARM_REMOVE_THRESHOLD = 3.2
HARM_SHADOW_THRESHOLD = 2.0
HARM_APPROVE_THRESHOLD = 0.8

CLARITY_REQUIRED_FOR_REMOVE = 0.85
CLARITY_REQUIRED_FOR_APPROVE = 0.5
```

The asymmetry is the point. **Two separate clarity bars** — one to remove, one to approve. The removal bar is higher because the cost of being wrong is higher.

## Why asymmetric thresholds

A symmetric system (`if harm > 2.0: remove`) sounds fair but isn't. It treats a false positive and a false negative as equal errors. They aren't.

- **False positive** (removing good content): user is angry, trust is damaged, damage is irreversible
- **False negative** (leaving bad content): user sees something they shouldn't, damage is bounded, you can remove it in 5 minutes

Most platforms weight these costs at roughly 3:1. That's why the removal bar is higher.

Making the thresholds explicit in code is the whole design. The numbers encode your platform's values — and putting them where people can see them is honest.

## Files

| File | Purpose |
|---|---|
| `content.py` | Content dataclass + `describe()` for Jev state |
| `moderate.jev` | Four typed questions to Jev |
| `policy.py` | Asymmetric rule engine and thresholds |
| `demo.py` | Six sample posts |

## Patterns across all eight projects

This is the 8th Jev project. The rule that keeps repeating:

**The model judges. The code decides.**

And this one adds: **the thresholds are values, not defaults.** A moderation system isn't neutral. Every threshold choice encodes a tradeoff. Making those choices explicit is what separates a system from a policy.

## License

MIT
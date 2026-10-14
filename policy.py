# policy.py
from dataclasses import dataclass
from typing import Literal

import jevlang

import moderate
from content import Content

Action = Literal["approve", "shadow", "remove", "human"]


@dataclass
class ModerationResult:
    action: Action
    harm: float
    category: str
    clarity: float
    confidence: float
    reason: str


# ---- Asymmetric thresholds ----
#
# Removing good content is worse than leaving bad content up.
# So the bar for removal is HIGHER than the bar for approval.
#
# Think of it as: the cost of a false positive (removing good)
# is 3x the cost of a false negative (leaving bad).
#
HARM_REMOVE_THRESHOLD = 3.2       # very confident it's harmful → remove
HARM_SHADOW_THRESHOLD = 2.0       # moderately harmful → shadow (reversible)
HARM_APPROVE_THRESHOLD = 0.8      # very confident it's fine → approve

CLARITY_REQUIRED_FOR_REMOVE = 0.85  # must be clear to remove
CLARITY_REQUIRED_FOR_APPROVE = 0.5  # less clarity needed to approve


def moderate_content(content: Content) -> ModerationResult:
    decision = moderate.evaluate_content(content.describe())

    harm = float(decision.harm)
    category = str(decision.category)
    clarity = float(decision.is_clear)
    needs_human = float(decision.needs_human) >= 0.5
    confidence = decision.harm.confidence

    # ---- Hard rules ----

    # Fast approve: benign + low harm + high clarity
    if (
        category == "benign"
        and harm < HARM_APPROVE_THRESHOLD
        and clarity >= CLARITY_REQUIRED_FOR_APPROVE
    ):
        return ModerationResult(
            "approve", harm, category, clarity, confidence,
            f"Benign content, low harm ({harm:.2f}/4). Approved.",
        )

    # Fast remove: critical harm regardless of clarity
    if harm >= 3.8:
        return ModerationResult(
            "remove", harm, category, clarity, confidence,
            f"Critical harm ({harm:.2f}/4). Removed.",
        )

    # ---- The asymmetric band ----

    # Remove requires BOTH high harm AND high clarity
    if harm >= HARM_REMOVE_THRESHOLD and clarity >= CLARITY_REQUIRED_FOR_REMOVE:
        return ModerationResult(
            "remove", harm, category, clarity, confidence,
            f"Harmful ({harm:.2f}/4) and clear ({clarity:.2f}). Removed.",
        )

    # High harm but low clarity → shadow (reversible middle ground)
    if harm >= HARM_SHADOW_THRESHOLD:
        return ModerationResult(
            "shadow", harm, category, clarity, confidence,
            f"Harm ({harm:.2f}/4) but clarity {clarity:.2f} below remove bar. "
            "Shadowed for review.",
        )

    # Jev says a human is needed → escalate
    if needs_human:
        return ModerationResult(
            "human", harm, category, clarity, confidence,
            "Jev flagged this as needing human judgment.",
        )

    # Low harm + not flagged → approve
    return ModerationResult(
        "approve", harm, category, clarity, confidence,
        f"Low harm ({harm:.2f}/4), no policy concern. Approved.",
    )
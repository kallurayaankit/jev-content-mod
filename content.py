# content.py
from dataclasses import dataclass


@dataclass
class Content:
    text: str
    author: str
    platform: str = "feed"
    author_account_age_days: int = 365
    prior_violations: int = 0

    def describe(self) -> str:
        lines = [
            f"Platform: {self.platform}",
            f"Author: {self.author}",
            f"Account age: {self.author_account_age_days} days",
            f"Prior violations: {self.prior_violations}",
            "",
            "Content:",
            self.text,
        ]
        return "\n".join(lines)
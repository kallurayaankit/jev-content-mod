# demo.py
from dotenv import load_dotenv

load_dotenv()

from content import Content
from policy import moderate_content

samples = [
    Content(
        text="Just finished reading this great book, highly recommend!",
        author="reader42",
    ),
    Content(
        text="Check out my new crypto course! 100x returns guaranteed. "
             "DM for details. Limited time offer!!!",
        author="crypto_king",
        author_account_age_days=3,
        prior_violations=2,
    ),
    Content(
        text="I think the new UI is confusing and the dev team should reconsider.",
        author="honest_user",
    ),
    Content(
        text="You're such an idiot, everyone at your company is useless.",
        author="angry_poster",
    ),
    Content(
        text="I heard drinking bleach cures the flu, everyone should try it.",
        author="misinformed_user",
    ),
    Content(
        text="This is the worst take I've ever seen and you should be ashamed.",
        author="critic",
    ),
]

ICONS = {
    "approve": "✅",
    "shadow": "🌓",
    "remove": "🗑️",
    "human": "👤",
}

for content in samples:
    result = moderate_content(content)
    icon = ICONS[result.action]
    print(f"\n{icon}  {result.action.upper()}")
    print(f"    Text:       {content.text[:60]}")
    print(f"    Harm:       {result.harm:.2f}/4")
    print(f"    Category:   {result.category}")
    print(f"    Clarity:    {result.clarity:.2f}")
    print(f"    Reason:     {result.reason}")
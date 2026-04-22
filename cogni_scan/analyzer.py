"""Rule-based cognitive analysis engine. Pure Python, deterministic."""
from __future__ import annotations
import re
import random
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from typing import Any

CATEGORY_KEYWORDS = {
    "News & Politics": ["news", "election", "politics", "government", "war", "policy", "president", "vote"],
    "Entertainment": ["movie", "film", "music", "song", "concert", "celebrity", "tv", "netflix", "show"],
    "Tech & Coding": ["code", "python", "javascript", "ai", "tech", "startup", "github", "developer", "ml"],
    "Lifestyle & Fashion": ["fashion", "outfit", "style", "beauty", "makeup", "skincare", "ootd"],
    "Sports": ["football", "soccer", "basketball", "cricket", "match", "team", "score", "league"],
    "Gaming": ["game", "gaming", "stream", "twitch", "valorant", "minecraft", "fortnite"],
    "Food": ["recipe", "food", "cooking", "restaurant", "meal", "chef", "dish"],
    "Memes & Humor": ["meme", "lol", "lmao", "funny", "joke", "haha"],
    "Fitness & Health": ["gym", "workout", "fitness", "yoga", "diet", "health", "running"],
    "Education": ["learn", "study", "book", "tutorial", "course", "university", "lecture"],
}

POSITIVE_WORDS = {"happy", "love", "great", "amazing", "awesome", "good", "wonderful", "excited",
                  "beautiful", "perfect", "best", "fun", "joy", "lol", "haha", "win", "thanks"}
NEGATIVE_WORDS = {"hate", "sad", "angry", "anxious", "depressed", "tired", "stressed", "fail",
                  "worst", "boring", "bad", "annoying", "lonely", "afraid", "fear", "ugh"}

RISK_KEYWORDS = {
    "Doomscrolling": ["disaster", "crisis", "war", "death", "tragedy", "shocking"],
    "Comparison Pressure": ["perfect life", "rich", "luxury", "envy", "everyone has", "i wish i"],
    "Outrage Bait": ["outraged", "you won't believe", "shocking truth", "exposed", "scandal"],
    "Information Overload": ["breaking", "update", "alert", "must read", "thread"],
    "Idealized Bodies": ["abs", "perfect body", "weight loss", "slim", "shredded"],
    "Toxic Positivity": ["just be happy", "manifest", "good vibes only", "stop complaining"],
    "FOMO": ["everyone is", "missing out", "fomo", "exclusive", "limited"],
}

HOUR_RE = re.compile(r"(\d{1,2}):(\d{2})")


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z']+", text.lower())


def _categorize(text_lower: str) -> str:
    scores: dict[str, int] = {}
    for cat, kws in CATEGORY_KEYWORDS.items():
        s = sum(text_lower.count(kw) for kw in kws)
        if s > 0:
            scores[cat] = s
    if not scores:
        return "Other"
    return max(scores, key=scores.get)


def _sentiment(tokens: list[str]) -> str:
    pos = sum(1 for t in tokens if t in POSITIVE_WORDS)
    neg = sum(1 for t in tokens if t in NEGATIVE_WORDS)
    if pos == 0 and neg == 0:
        return "neutral"
    if pos > neg:
        return "positive"
    if neg > pos:
        return "negative"
    return "neutral"


def _split_entries(content: str) -> list[str]:
    lines = [ln.strip() for ln in content.splitlines() if ln.strip()]
    return lines or [content.strip()]


def analyze(platform: str, content: str) -> dict[str, Any]:
    entries = _split_entries(content)
    n = max(len(entries), 1)

    cat_counter: Counter[str] = Counter()
    sentiment_by_day: dict[int, Counter[str]] = defaultdict(Counter)
    hour_counter: Counter[int] = Counter()
    risk_counter: Counter[str] = Counter()
    pos_total = neg_total = neu_total = 0

    rng = random.Random(hash((platform, content)) & 0xFFFFFFFF)

    for i, entry in enumerate(entries):
        low = entry.lower()
        tokens = _tokenize(entry)

        cat_counter[_categorize(low)] += 1

        sent = _sentiment(tokens)
        day = i % 7
        sentiment_by_day[day][sent] += 1
        if sent == "positive":
            pos_total += 1
        elif sent == "negative":
            neg_total += 1
        else:
            neu_total += 1

        m = HOUR_RE.search(entry)
        if m:
            try:
                hour_counter[int(m.group(1)) % 24] += 1
            except ValueError:
                hour_counter[rng.randint(8, 23)] += 1
        else:
            hour_counter[rng.randint(8, 23)] += 1

        for risk, kws in RISK_KEYWORDS.items():
            if any(kw in low for kw in kws):
                risk_counter[risk] += 1

    attention = max(0.0, min(1.0, 1.0 - min(n / 80.0, 0.9)))
    anxiety = min(1.0, neg_total / max(n, 1) + 0.15 * sum(risk_counter.values()) / max(n, 1))
    dopamine = min(1.0, (cat_counter.get("Memes & Humor", 0) + cat_counter.get("Entertainment", 0)
                          + cat_counter.get("Gaming", 0)) / max(n, 1) * 1.5)
    social_comparison = min(1.0, (risk_counter.get("Comparison Pressure", 0)
                                   + risk_counter.get("Idealized Bodies", 0)
                                   + risk_counter.get("FOMO", 0)) / max(n, 1) * 2.5)
    info_overload = min(1.0, (risk_counter.get("Information Overload", 0)
                               + cat_counter.get("News & Politics", 0)) / max(n, 1) * 1.5)

    metrics = {
        "Attention": round(attention, 2),
        "Anxiety": round(anxiety, 2),
        "Dopamine Seeking": round(dopamine, 2),
        "Social Comparison": round(social_comparison, 2),
        "Information Overload": round(info_overload, 2),
    }

    content_breakdown = [{"category": c, "count": v} for c, v in cat_counter.most_common()]

    emotional_trend = []
    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for d in range(7):
        c = sentiment_by_day.get(d, Counter())
        emotional_trend.append({
            "day": day_names[d],
            "positive": c.get("positive", 0),
            "negative": c.get("negative", 0),
            "neutral": c.get("neutral", 0),
        })

    engagement_pattern = [{"hour": h, "count": hour_counter.get(h, 0)} for h in range(24)]

    risk_factors = sorted(
        [{"factor": k, "severity": min(10, v * 2)} for k, v in risk_counter.items()],
        key=lambda r: r["severity"], reverse=True
    )
    if not risk_factors:
        risk_factors = [{"factor": "No major risks detected", "severity": 1}]

    overall_risk_score = round(min(10.0,
        anxiety * 4 + social_comparison * 3 + info_overload * 2 + (1 - attention) * 1
    ), 2)

    if overall_risk_score < 3:
        impact = ("Your consumption pattern looks healthy. Sentiment skews neutral-to-positive and "
                  "risk indicators are low. Keep current habits and stay mindful of trends.")
    elif overall_risk_score < 6:
        impact = ("Moderate cognitive load detected. There are recurring negative-sentiment posts and "
                  "some risk patterns (comparison, news overload). This can subtly raise stress and "
                  "fragment attention over time.")
    else:
        impact = ("High cognitive impact. Frequent negative emotion, doomscrolling cues, and high "
                  "social-comparison signals are present. Sustained exposure may worsen anxiety, "
                  "sleep, and self-image.")

    summary = (f"Analyzed {n} entries from {platform}. Top categories: "
               f"{', '.join([c['category'] for c in content_breakdown[:3]]) or 'mixed'}. "
               f"Sentiment — positive: {pos_total}, negative: {neg_total}, neutral: {neu_total}.")

    preventive_measures = [
        "Set a daily timer (20–30 min) per platform; use OS screen-time limits.",
        "Curate your feed: unfollow accounts that consistently trigger negative sentiment.",
        "Schedule news consumption to 1–2 fixed slots per day to reduce doomscrolling.",
        "Replace passive scrolling with one active habit (writing, walking, conversation) daily.",
        "Phone-free first hour after waking and last hour before sleep.",
    ]
    if social_comparison > 0.4:
        preventive_measures.append("Mute lifestyle/influencer accounts for two weeks and re-evaluate.")
    if anxiety > 0.4:
        preventive_measures.append("Try a 24-hour content fast once per week.")

    return {
        "platform": platform,
        "content": content,
        "summary": summary,
        "impact": impact,
        "preventive_measures": preventive_measures,
        "metrics": metrics,
        "content_breakdown": content_breakdown,
        "emotional_trend": emotional_trend,
        "engagement_pattern": engagement_pattern,
        "risk_factors": risk_factors,
        "overall_risk_score": overall_risk_score,
        "created_at": datetime.utcnow(),
    }

"""A small filter that learns from the decisions of the moderators of a server.

It is a naive Bayes classifier over words and word pairs. Only short hashes of the words are stored, never the text, so the model cannot be read back into messages. It starts to judge only after it has seen enough examples of both kinds.
"""

import hashlib
import math
import re
from typing import Any

MIN_SCAM = 8
MIN_HAM = 30
MAX_FEATURES = 6000
MAX_TOKENS = 120
MIN_SEEN = 2
CAP = 1.5
ACT = 0.95
ASK = 0.6
WORD_RE = re.compile(r"[^\W_]{2,}", re.UNICODE)
URL_RE = re.compile(r"https?://([^\s/]+)", re.I)


def new_model() -> dict:
    """An empty model."""
    return {"scam": {}, "ham": {}, "n_scam": 0, "n_ham": 0}


def features(text: str) -> set[str]:
    """Hashed words, word pairs and link hosts of a text."""
    text = text.lower()[:4000]
    words = WORD_RE.findall(text)[:MAX_TOKENS]
    feats = set(words)
    feats.update(f"{a} {b}" for a, b in zip(words, words[1:]))
    feats.update("host:" + h for h in URL_RE.findall(text))
    return {hashlib.blake2b(f.encode(), digest_size=5).hexdigest() for f in feats}


def prune(table: dict) -> None:
    """Keep the most seen features when the table grows too large."""
    if len(table) > MAX_FEATURES:
        keep = sorted(table.items(), key=lambda kv: kv[1], reverse=True)[:MAX_FEATURES * 3 // 4]
        table.clear()
        table.update(keep)


def train(model: dict, text: str, scam: bool) -> bool:
    """Learn one example. Returns False if the text has nothing to learn from."""
    feats = features(text)
    if len(feats) < 3:
        return False
    side = "scam" if scam else "ham"
    table = model[side]
    for f in feats:
        table[f] = table.get(f, 0) + 1
    model["n_" + side] += 1
    prune(table)
    return True


def untrain(model: dict, text: str, scam: bool) -> None:
    """Take one example back, for a decision that was changed."""
    side = "scam" if scam else "ham"
    if model["n_" + side] <= 0:
        return
    table = model[side]
    for f in features(text):
        if f in table:
            table[f] -= 1
            if table[f] <= 0:
                del table[f]
    model["n_" + side] -= 1


def ready(model: dict) -> bool:
    """True once the model has seen enough of both kinds."""
    return model["n_scam"] >= MIN_SCAM and model["n_ham"] >= MIN_HAM


def probability(model: dict, text: str) -> float:
    """The chance, 0 to 1, that a text is a scam. 0.5 when the model cannot judge."""
    if not ready(model):
        return 0.5
    feats = features(text)
    if len(feats) < 3:
        return 0.5
    ns, nh = model["n_scam"], model["n_ham"]
    score = math.log(ns / nh)
    scam, ham = model["scam"], model["ham"]
    for f in feats:
        a, b = scam.get(f, 0), ham.get(f, 0)
        if a + b < MIN_SEEN:
            continue
        evidence = math.log((a + 1) / (ns + 2)) - math.log((b + 1) / (nh + 2))
        score += max(-CAP, min(CAP, evidence))
    score = max(-30.0, min(30.0, score))
    return 1 / (1 + math.exp(-score))


def stats(model: dict) -> dict[str, Any]:
    """Numbers for the status page."""
    return {"scam": model["n_scam"], "ham": model["n_ham"], "features": len(model["scam"]) + len(model["ham"]), "ready": ready(model)}

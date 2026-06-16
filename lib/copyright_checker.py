"""
copyright_checker.py
====================
Local, offline originality / copyright-infringement checker (Problem 2).

This module performs **text recognition** entirely on-device — no OpenAI, no
external API keys, and no network calls. It combines three classic information
retrieval signals to flag potential overlap between a writer's draft and a
database of known works:

1. TF-IDF cosine similarity
   Each document (the draft + every reference summary) is turned into a
   term-frequency / inverse-document-frequency vector. Cosine similarity ranks
   which existing works are most lexically similar to the draft.

2. N-gram phrase recognition
   Overlapping word trigrams are compared to recognize shared multi-word
   phrases. This is the "text recognition" core: it surfaces the *actual*
   matching spans of text, which is what copied/paraphrased passages look like.

3. Fuzzy sequence matching
   difflib.SequenceMatcher finds the longest verbatim matching block, catching
   near-identical sentences even when surrounded by different text.

The three signals are blended into a single similarity score and mapped to a
risk level, with concrete, human-readable explanations. Generic story tropes
are detected separately and reported as *non-infringing* shared elements.

The reference database is stored in the JSON store under the "reference_works"
collection and seeded from data/seed_reference_works.json on first run.
Writers' own published stories are ALSO checked, so the platform protects
everyone's intellectual property — including its own community.
"""

from __future__ import annotations

import json
import math
import os
import re
from collections import Counter
from difflib import SequenceMatcher

from lib import storage

REFERENCE = "reference_works"

# Extremely common English words that carry little discriminative signal.
_STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "if", "then", "of", "to", "in", "on",
    "at", "by", "for", "with", "about", "as", "into", "like", "through", "after",
    "over", "between", "out", "against", "during", "without", "before", "under",
    "around", "among", "is", "are", "was", "were", "be", "been", "being", "am",
    "his", "her", "its", "their", "our", "your", "my", "he", "she", "it", "they",
    "we", "you", "i", "him", "them", "us", "this", "that", "these", "those",
    "who", "whom", "which", "what", "when", "where", "why", "how", "all", "any",
    "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor",
    "not", "only", "own", "same", "so", "than", "too", "very", "can", "will",
    "just", "from", "up", "down", "off", "again", "once", "here", "there",
    "while", "has", "have", "had", "do", "does", "did", "would", "could",
    "should", "may", "might", "must", "shall", "also", "upon", "two",
}

# A small library of common, non-infringing storytelling tropes. Sharing these
# is NOT copyright infringement — ideas and tropes are free for everyone to use.
_TROPES = {
    "chosen one": ["chosen one", "prophecy", "destined hero", "the one"],
    "hero's journey": ["journey home", "long voyage", "perilous quest", "epic quest"],
    "enemies to lovers": ["despise", "rivalry turns", "initially hate", "sworn enemies"],
    "forbidden love": ["forbidden love", "star-crossed", "across class"],
    "coming of age": ["coming of age", "grows up", "loses innocence"],
    "good vs evil": ["good versus evil", "dark lord", "ancient evil"],
    "the monster within": ["monster", "creature", "created life", "reanimated"],
    "detective mystery": ["detective", "solves crimes", "deduction", "investigates"],
    "time travel": ["time machine", "travels through time", "future society"],
    "redemption arc": ["seeks redemption", "atone", "redeems himself"],
}


# --------------------------------------------------------------------------- #
# Capability flag (kept for backwards compatibility with the UI)
# --------------------------------------------------------------------------- #
def ai_enabled() -> bool:
    """
    The originality checker now runs fully offline, so it is ALWAYS available.

    The name is retained so existing views keep working; it simply reports that
    the local text-recognition engine is ready.
    """
    return True


def engine_name() -> str:
    return "Local text-recognition engine (TF-IDF + n-gram + fuzzy match)"


# --------------------------------------------------------------------------- #
# Reference database
# --------------------------------------------------------------------------- #
def _seed_reference_if_empty() -> None:
    if storage.read_collection(REFERENCE):
        return
    seed_path = os.path.join("data", "seed_reference_works.json")
    if os.path.exists(seed_path):
        try:
            with open(seed_path, "r", encoding="utf-8") as fh:
                seed = json.load(fh)
            storage.write_collection(REFERENCE, seed)
        except Exception:
            pass


def reference_works() -> list[dict]:
    _seed_reference_if_empty()
    works = list(storage.read_collection(REFERENCE))
    # Also compare against community-published stories.
    for story in storage.find_many("stories", status="published"):
        works.append(
            {
                "id": f"story:{story.get('id')}",
                "title": story.get("title", "Untitled"),
                "author": story.get("author_name", "Community author"),
                "summary": (story.get("synopsis") or story.get("body", ""))[:1500],
                "source": "Inkverse community",
            }
        )
    return works


# --------------------------------------------------------------------------- #
# Text-recognition primitives
# --------------------------------------------------------------------------- #
def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9']+", (text or "").lower())


def _content_tokens(text: str) -> list[str]:
    return [t for t in _tokenize(text) if t not in _STOPWORDS and len(t) > 2]


def _tfidf_vectors(docs: list[list[str]]) -> list[dict[str, float]]:
    """Build L2-normalized TF-IDF vectors for a list of tokenized documents."""
    n = len(docs)
    df: Counter = Counter()
    for tokens in docs:
        for term in set(tokens):
            df[term] += 1

    vectors: list[dict[str, float]] = []
    for tokens in docs:
        tf = Counter(tokens)
        total = max(len(tokens), 1)
        vec: dict[str, float] = {}
        for term, count in tf.items():
            idf = math.log((1 + n) / (1 + df[term])) + 1.0
            vec[term] = (count / total) * idf
        norm = math.sqrt(sum(w * w for w in vec.values())) or 1.0
        vectors.append({term: w / norm for term, w in vec.items()})
    return vectors


def _cosine(a: dict[str, float], b: dict[str, float]) -> float:
    if len(a) > len(b):
        a, b = b, a
    return sum(weight * b.get(term, 0.0) for term, weight in a.items())


def _ngrams(tokens: list[str], n: int = 3) -> set[tuple[str, ...]]:
    if len(tokens) < n:
        return {tuple(tokens)} if tokens else set()
    return {tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)}


def _phrase_overlaps(draft: str, work_summary: str, max_phrases: int = 5) -> list[str]:
    """Recognize concrete multi-word phrases shared by both texts."""
    d_tokens = _content_tokens(draft)
    w_tokens = _content_tokens(work_summary)
    shared = _ngrams(d_tokens, 3) & _ngrams(w_tokens, 3)
    phrases = sorted({" ".join(g) for g in shared})
    return phrases[:max_phrases]


def _longest_match_ratio(draft: str, work_summary: str) -> float:
    """Fuzzy verbatim overlap via the longest common contiguous block."""
    a = " ".join(_tokenize(draft))
    b = " ".join(_tokenize(work_summary))
    if not a or not b:
        return 0.0
    matcher = SequenceMatcher(None, a, b, autojunk=False)
    block = matcher.find_longest_match(0, len(a), 0, len(b))
    return block.size / max(len(a), 1)


def _detect_tropes(draft: str, work_summary: str) -> list[str]:
    haystack = (draft + " " + work_summary).lower()
    found = []
    for trope, cues in _TROPES.items():
        if any(cue in haystack for cue in cues):
            found.append(trope)
    return found


# --------------------------------------------------------------------------- #
# Per-work analysis (local, deterministic)
# --------------------------------------------------------------------------- #
def _risk_from_scores(cosine: float, ngram: float, fuzzy: float) -> str:
    blended = 0.5 * cosine + 0.3 * ngram + 0.2 * fuzzy
    if blended >= 0.55 or fuzzy >= 0.35:
        return "high"
    if blended >= 0.32 or ngram >= 0.18:
        return "medium"
    if blended >= 0.16:
        return "low"
    return "none"


def _analyze_pair(draft: str, work: dict, cosine: float) -> dict:
    summary = work.get("summary", "")
    d_grams = _ngrams(_content_tokens(draft), 3)
    w_grams = _ngrams(_content_tokens(summary), 3)
    union = len(d_grams | w_grams) or 1
    ngram_overlap = len(d_grams & w_grams) / union
    fuzzy = _longest_match_ratio(draft, summary)

    risk = _risk_from_scores(cosine, ngram_overlap, fuzzy)
    overlaps_phrases = _phrase_overlaps(draft, summary)
    tropes = _detect_tropes(draft, summary)

    overlaps: list[str] = []
    for phrase in overlaps_phrases:
        overlaps.append(f'Shared phrasing recognized: "{phrase}"')
    if fuzzy >= 0.2:
        overlaps.append(
            f"A long passage is {round(fuzzy * 100)}% verbatim-similar to this work."
        )

    explanation = (
        f"Lexical (TF-IDF) similarity {round(cosine * 100)}%, "
        f"shared-phrase overlap {round(ngram_overlap * 100)}%, "
        f"longest verbatim block {round(fuzzy * 100)}%."
    )

    if risk == "high":
        recommendation = (
            "Strong textual overlap detected. Revise the flagged passages and "
            "distinctive phrasing substantially, or confirm you hold the rights, "
            "before publishing."
        )
    elif risk == "medium":
        recommendation = (
            "Some recognizable overlap. Review the shared phrases and rework them "
            "in your own voice to keep your work clearly original."
        )
    elif risk == "low":
        recommendation = (
            "Minor lexical similarity, most likely shared vocabulary or common "
            "tropes. Generally safe, but a quick review never hurts."
        )
    else:
        recommendation = "No meaningful textual overlap with this work."

    return {
        "risk_level": risk,
        "similarity_explanation": explanation,
        "overlaps": overlaps,
        "common_tropes": tropes,
        "recommendation": recommendation,
        "scores": {
            "tfidf_cosine": round(cosine, 3),
            "ngram_overlap": round(ngram_overlap, 3),
            "fuzzy_block": round(fuzzy, 3),
        },
    }


# --------------------------------------------------------------------------- #
# Public entry point
# --------------------------------------------------------------------------- #
def check_draft(draft: str, top_k: int = 3, threshold: float = 0.10) -> dict:
    """
    Run the full local originality check on a draft.

    Returns a dict:
    {
      "ai_enabled": bool,          # True (engine is always available)
      "engine": str,               # human-readable engine name
      "message": str | None,
      "candidates": [ {work fields..., "similarity": float, "analysis": {...}} ],
      "overall_risk": "none|low|medium|high",
    }
    """
    if not draft or len(draft.strip()) < 40:
        return {
            "ai_enabled": True,
            "engine": engine_name(),
            "message": "Please paste at least a few sentences of your draft.",
            "candidates": [],
            "overall_risk": "none",
        }

    works = reference_works()
    if not works:
        return {
            "ai_enabled": True,
            "engine": engine_name(),
            "message": "No reference works available to compare against yet.",
            "candidates": [],
            "overall_risk": "none",
        }

    # 1) TF-IDF cosine similarity to rank candidates.
    doc_tokens = [_content_tokens(draft)] + [
        _content_tokens(w.get("summary", "")) for w in works
    ]
    vectors = _tfidf_vectors(doc_tokens)
    draft_vec, work_vecs = vectors[0], vectors[1:]

    scored = []
    for work, vec in zip(works, work_vecs):
        scored.append((_cosine(draft_vec, vec), work))
    scored.sort(key=lambda t: t[0], reverse=True)

    # 2) Detailed phrase/fuzzy analysis for the top candidates above threshold.
    candidates = []
    risk_rank = {"none": 0, "low": 1, "medium": 2, "high": 3}
    overall = "none"
    for similarity, work in scored[:top_k]:
        if similarity < threshold:
            continue
        analysis = _analyze_pair(draft, work, similarity)
        candidates.append(
            {**work, "similarity": round(similarity, 3), "analysis": analysis}
        )
        lvl = analysis.get("risk_level", "low")
        if risk_rank.get(lvl, 0) > risk_rank.get(overall, 0):
            overall = lvl

    message = None
    if not candidates:
        message = "No significant overlaps detected against the reference database."

    return {
        "ai_enabled": True,
        "engine": engine_name(),
        "message": message,
        "candidates": candidates,
        "overall_risk": overall,
    }

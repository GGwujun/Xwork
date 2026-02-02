from __future__ import annotations

import math
import re

from .models import Skill


_TOKEN_RE = re.compile(r"[A-Za-z0-9_]+")


def _tokenize(text: str) -> list[str]:
    tokens = [token.lower() for token in _TOKEN_RE.findall(text)]
    try:
        import jieba  # type: ignore
    except Exception:
        return tokens
    chinese_tokens = [token.strip() for token in jieba.lcut(text) if token.strip()]
    return tokens + chinese_tokens


def _tf(tokens: list[str]) -> dict[str, float]:
    counts: dict[str, int] = {}
    for token in tokens:
        counts[token] = counts.get(token, 0) + 1
    total = max(1, len(tokens))
    return {token: count / total for token, count in counts.items()}


def _idf(corpus: list[list[str]]) -> dict[str, float]:
    doc_count = len(corpus)
    df: dict[str, int] = {}
    for tokens in corpus:
        for token in set(tokens):
            df[token] = df.get(token, 0) + 1
    return {token: math.log((doc_count + 1) / (freq + 1)) + 1 for token, freq in df.items()}


def keyword_score(query: str, skill: Skill, corpus_tokens: list[list[str]]) -> float:
    query_tokens = _tokenize(query)
    if not query_tokens:
        return 0.0
    doc_tokens = _tokenize(skill.content + " " + skill.name + " " + skill.description)
    tf = _tf(doc_tokens)
    idf = _idf(corpus_tokens)
    score = 0.0
    for token in query_tokens:
        score += tf.get(token, 0.0) * idf.get(token, 0.0)
    return score

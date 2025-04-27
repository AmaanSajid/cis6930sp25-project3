"""
Decide whether a message is intelligible English (“human”) or gibberish (“alien”).
"""
from __future__ import annotations
import importlib.util, pathlib, re
from loguru import logger


def _load_words() -> set[str]:
    """Return a set of English words from data/words.txt or the wordfreq lexicon."""
    local = pathlib.Path(__file__).parent.parent / "data" / "words.txt"
    if local.exists():
        logger.info("Loading local word list {}", local)
        return set(local.read_text(encoding="utf8").split())

    if importlib.util.find_spec("wordfreq"):
        logger.info("Falling back to wordfreq top-50 000 list")
        from wordfreq import top_n_list
        return set(top_n_list("en", 50_000))

    raise FileNotFoundError(
        "No word list found. Add data/words.txt or `uv pip install wordfreq`."
    )


EN_WORDS: set[str] = _load_words()


def label(msg: str) -> str:
    """Return 'human' if at least 50 % of tokens are in EN_WORDS, else 'alien'."""
    tokens = re.findall(r"[A-Za-z']+", msg.lower())
    if not tokens:
        return "alien"
    ratio = sum(t in EN_WORDS for t in tokens) / len(tokens)
    decision = "human" if ratio >= 0.5 else "alien"
    logger.debug("ratio {:.2f}  →  {}", ratio, decision)
    return decision

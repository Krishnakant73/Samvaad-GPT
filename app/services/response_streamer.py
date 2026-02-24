from __future__ import annotations

import time
from typing import Iterable, Iterator


def stream_words(full_text: str, *, delay_seconds: float = 0.02) -> Iterator[str]:
    text = (full_text or "").strip()
    if not text:
        yield ""
        return

    words = text.split(" ")
    partial = ""

    for i, w in enumerate(words):
        if i == 0:
            partial = w
        else:
            partial += " " + w
        yield partial
        if delay_seconds > 0:
            time.sleep(delay_seconds)


def stream_chars(full_text: str, *, delay_seconds: float = 0.005) -> Iterable[str]:
    text = full_text or ""
    partial = ""
    for ch in text:
        partial += ch
        yield partial
        if delay_seconds > 0:
            time.sleep(delay_seconds)

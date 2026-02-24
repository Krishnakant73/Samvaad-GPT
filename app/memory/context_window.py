from __future__ import annotations

from typing import Dict, List, Sequence


def last_n_messages(messages: Sequence[Dict[str, str]], *, n: int) -> List[Dict[str, str]]:
    if n <= 0:
        return []
    return list(messages[-n:])

"""Mesopt wrapper for LIT components"""
from dataclasses import dataclass
from typing import Any, Callable, List, Dict

import mesop.labs as mel

from wsd.models import Token


@mel.web_component(path="../lit/dist/linpop.js")
def lin_doc(
    *,
    tokens: List[Dict],
    cur: int,
    on_pop: Callable[[mel.WebEvent], Any],
    key: str | None = None,
):
    """Wrapper for the LIT LinDoc component."""
    return mel.insert_web_component(
        name="lin-doc",
        key=key,
        events={"popEvent": on_pop},
        properties={"tokens": tokens, "cur": cur},
    )


@mel.web_component(path="../lit/dist/linpop.js")
def lin_entry(
    *,
    entry: Dict,
    selected: bool,
    on_chosen: Callable[[mel.WebEvent], Any],
    key: str | None = None
):
    """Wrapper for the LIT LinEntry component."""
    return mel.insert_web_component(
        name="lin-entry",
        key=key,
        properties={"entry": entry, "selected": selected},
        events={"chosenEvent": on_chosen},
    )


__all__ = ["lin_doc", "lin_entry", "Token"]

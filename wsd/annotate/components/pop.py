from dataclasses import dataclass
from typing import Any, Callable, List, Dict

import mesop.labs as mel


@dataclass
class Token:
    text: str = ''
    lemma: str = ''
    pos: str = ''


@mel.web_component(path="../lit/dist/linpop.js")
def LinDoc(
    *,
    tokens: List[Dict],
    cur: int,
    on_pop: Callable[[mel.WebEvent], Any],
    key: str | None = None,
):
    return mel.insert_web_component(
        name="lin-doc",
        key=key,
        events={"popEvent": on_pop},
        properties={"tokens": tokens, "cur": cur},
    )


@mel.web_component(path="../lit/dist/linpop.js")
def LinEntry(
    *,
    entry: Dict,
    selected: bool,
    on_chosen: Callable[[mel.WebEvent], Any],
    key: str | None = None
):
    return mel.insert_web_component(
        name="lin-entry",
        key=key,
        properties={"entry": entry, "selected": selected},
        events={"chosenEvent": on_chosen},
    )


__all__ = ["LinDoc", "LinEntry", "Token"]

from typing import Any, Callable

import mesop.labs as mel


@mel.web_component(path="./pop.js")
def linpop_component(
  *,
  text: str,
  on_pop: Callable[[mel.WebEvent], Any],
  key: str | None = None,
):
  return mel.insert_web_component(
    name="linpop-component",
    key=key,
    events={
      "popEvent": on_pop,
    },
    properties={
      "text": text,
    },
  )

__all__ = [
  "linpop_component",
]
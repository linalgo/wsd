from dataclasses import field
from typing import List
import mesop as me
import mesop.labs as mel
from mesop.server.wsgi_app import create_app

from wsd.parsers import XLWSDParser
from wsd.parsers.jmdict import Entry
from wsd.models import JMDict
from wsd.annotate.components import linpop_component

xlwsd = XLWSDParser()
X, y = xlwsd.parse("ja")

jmdict = JMDict()

style_grid = me.Style(
    display="grid",
    grid_template_rows="auto 1fr auto",
    height="100%"
)
style_header = me.Style(
    background="#f0f0f0",
    padding=me.Padding.all(24)
)
style_body = me.Style(
    padding=me.Padding.all(24),
    overflow_y="auto"
)
style_card = me.Style(
    padding=me.Padding.all(24),
    overflow_y="auto",
    z_index=100,
    box_shadow="0 0 10px rgba(0, 0, 0, 0.1)"
)
style_group = me.Style(
    display="flex",
    gap=8
)

@me.stateclass
class State:
  candidates: List[Entry] = field(default_factory=list)

@me.page(
    path="/",
    security_policy=me.SecurityPolicy(
        allowed_script_srcs=[
            "https://cdn.jsdelivr.net",
        ]
    ),
)
def app():
    with me.box(style=style_grid):
        with me.box(style=style_header):
            me.text("SEMCOR WSD")

        with me.box(style=style_body):
            with  me.box(style=style_card):
                for tok in X[0]:
                    linpop_component(
                        text=tok,
                        on_pop=on_pop
                    )
            state = me.state(State)
            for candidate in state.candidates:
                with me.box(style=style_card):
                    me.text(candidate.ent_seq)
                    with me.box(style=style_group):
                        for kanji in candidate.k_ele:
                            me.text(kanji.keb)
                    with me.box(style=style_group):
                        for reading in candidate.r_ele:
                            me.text(reading.reb)
                    with me.box():
                        for sense in candidate.sense:
                            for gloss in sense.gloss:
                                me.text(gloss.text)


def on_pop(event: mel.WebEvent):
    state = me.state(State)
    query = event.value['text']
    state.candidates = jmdict.search(query)


if __name__ == "__main__":
    app = create_app(prod_mode=True)
    app._flask_app.run(host="localhost", port=8080, use_reloader=True)

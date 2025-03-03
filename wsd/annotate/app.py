import os
from typing import List
from dataclasses import asdict, field

import mesop as me
from mesop.server.wsgi_app import create_app

from fugashi import Tagger

from linalgo.hub.client import LinalgoClient

from wsd.parsers.jmdict import Entry
from wsd.annotate.lindict import LinDictAPI
from wsd.annotate import LinDoc, LinEntry, Token


LINHUB_TOKEN = os.getenv('LINHUB_TOKEN')
LINHUB_URL = os.getenv('LINHUB_URL')
LINHUB_TASK = os.getenv('LINHUB_TASK')

linhub = LinalgoClient(api_url=LINHUB_URL, token=LINHUB_TOKEN)
lindict = LinDictAPI()

tagger = Tagger('-Owakati')


def get_document():
    doc = linhub.get_next_document(LINHUB_TASK)
    tokens = []
    for word in tagger(doc.content):
        token = Token(
            text=word.surface,
            lemma=word.feature.lemma,
            pos=word.pos
        )
        tokens.append(token)
    return tokens


@me.stateclass
class State:
    tokens: List[Token] = field(default_factory=get_document)
    entries: List[Entry] = field(default_factory=list)
    cur: int = 0
    loading: bool = True


def get_entries(state):
    state = me.state(State)
    state.loading = True
    lemma = state.tokens[state.cur].lemma
    state.loading = False
    return lindict.search(lemma)


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
    overflow_y="wrap"
)
style_entry = me.Style(
    padding=me.Padding.all(24),
    margin=me.Margin.all(8),
    overflow_y="auto",
    z_index=100,
    box_shadow="0 0 10px rgba(0, 0, 0, 0.1)"
)
style_group = me.Style(
    display="flex",
    gap=8
)
    


@me.page(
    path="/",
    security_policy=me.SecurityPolicy(
        allowed_script_srcs=[
            "https://cdn.jsdelivr.net",
        ]
    ),
)
def app():
    state = me.state(State)
    state.entries = get_entries(state)
    with me.box(style=style_grid):
        with me.box(style=style_header):
            me.text("Japanese Word Sense Disambiguation")

        with me.box(style=style_body):
            me.text("Document", type="headline-5")
            tokens = [asdict(t) for t in state.tokens]
            LinDoc(tokens=tokens, on_pop=_on_pop, cur=state.cur)
            me.text("Entries", type="headline-5", style=me.Style(padding=me.Padding(top=24)))
            with me.box(style=me.Style(display='flex', gap=16, flex_wrap='wrap')):
                for entry in state.entries:
                    LinEntry(entry=asdict(entry), on_chosen=_on_chosen)

def _on_pop(event):
    print(event)

def _on_chosen(event):
    state = me.state(State)
    if not state.loading:
        state.cur += 1
        if state.cur < len(state.tokens):
            state.entries = get_entries(state)



if __name__ == "__main__":
    app = create_app(prod_mode=True)
    app._flask_app.run(host="localhost", port=8080, use_reloader=True)

"""Annotation UI for Japanese Word Sense Disambiguation."""
# pylint: disable=unused-argument,no-member,bare-except,no-name-in-module
import os
from dataclasses import asdict, field

import mesop as me
from fugashi import Tagger
from linalgo.annotate.models import Annotation, Target
from linalgo.hub.client import LinalgoClient

from wsd.annotate import lin_doc, lin_entry
from wsd.annotate.lindict import LinDictAPI
from wsd.exceptions import NoDocumentsAvailableException
from wsd.models import Token
from wsd.parsers.jmdict import Entry

LINHUB_TOKEN = os.getenv('LINHUB_TOKEN')
LINHUB_URL = os.getenv('LINHUB_URL')
LINHUB_TASK = os.getenv('LINHUB_TASK')

linhub = LinalgoClient(api_url=LINHUB_URL, token=LINHUB_TOKEN)
linhub.task = linhub.get_task(LINHUB_TASK, lazy=False)
linhub.annotator = linhub.get_current_annotator()
linhub.entity = linhub.task.entities[0]
linhub.annotations = {}
linhub.document = None

lindict = LinDictAPI()

tagger = Tagger('-Owakati')


@me.stateclass
class State:
    """Application state class."""
    tokens: list[Token] = field(default_factory=list)
    entries: list[Entry] = field(default_factory=list)
    cur: int = 0
    selected = None
    done = False


def get_next_document():
    """Get the next document for annotation."""
    try:
        linhub.document = linhub.get_next_document(LINHUB_TASK)
        return linhub.document
    except NoDocumentsAvailableException("No more documents to process."):
        state = me.state(State)
        state.done = True
        return None


def get_tokens():
    """Tokenize the current document."""
    doc = linhub.document
    tokens = []
    for word in tagger(doc.content):
        token = Token(
            text=word.surface,
            lemma=word.feature.lemma,
            pos=word.pos
        )
        tokens.append(token)
    return tokens


def get_entries():
    """Retrieve dictionary entries for the current token."""
    state = me.state(State)
    lemma = state.tokens[state.cur].lemma
    return lindict.search(lemma)


def on_load(e=None):
    """Prepare application state."""
    state = me.state(State)
    get_next_document()
    if linhub.document is not None:
        state.tokens = get_tokens()
        state.entries = get_entries()


header = me.Style(
    background="#f0f0f0",
    padding=me.Padding.all(24)
)
body = me.Style(
    padding=me.Padding.all(24),
    text_align='center',
    display='flex',
    flex_direction='column',
    justify_content='center',
)
entries = me.Style(
    padding=me.Padding(top=24),
    justify_content='center',
    gap=16,
    display='flex',
    flex_wrap='wrap'
)
footer = me.Style(
    position='fixed',
    bottom=0,
    width='100%',
    text_align='center',
    justify_content='center',
    padding=me.Padding.all(24),
)


@me.page(
    path="/",
    on_load=on_load
)
def app():
    """Japanese Word Sense Disambiguation UI."""
    state = me.state(State)

    with me.box(style=header):
        me.text("Japanese Word Sense Disambiguation")

    if state.done:
        with me.box(style=body):
            me.text("All done!")
    else:
        with me.box(style=body):
            tokens = [asdict(t) for t in state.tokens]
            lin_doc(tokens=tokens, on_pop=_on_pop, cur=state.cur)

        me.divider()

        with me.box(style=entries):
            for entry in state.entries:
                lin_entry(
                    entry=asdict(entry),
                    selected=state.selected == entry.ent_seq,
                    on_chosen=_on_chosen
                )

        with me.box(style=footer):
            label = "Next" if state.cur < len(state.tokens) - 1 else "Complete"
            me.button(
                label,
                on_click=_next,
                type="flat",
            )


def _on_pop(event):
    pass


def _on_chosen(event):
    state = me.state(State)
    state.selected = event.value['text']
    start = sum(len(t.text) for t in state.tokens[:state.cur])
    end = start + len(state.tokens[state.cur].text)
    annotation = Annotation(
        entity=linhub.entity,
        document=linhub.document.id,
        body=event.value['text'],
        annotator=linhub.annotator,
        target=Target(
            source=linhub.document,
            selector=[{
                'startContainer': '/',
                'endContainer': '/',
                'startOffset': start,
                'endOffset': end
            }]
        ),
        task=linhub.task
    )
    linhub.annotations[state.cur] = annotation


def _complete_document(event=None):
    linhub.create_annotations(linhub.annotations.values())
    linhub.annotations = {}
    linhub.complete_document(linhub.document, linhub.task)
    state = me.state(State)
    try:
        linhub.document = linhub.get_next_document(linhub.task.id)
        state.cur = 0
        state.selected = None
        state.tokens = get_tokens()
    except ValueError:
        state.done = True


def _next(event):
    state = me.state(State)
    if state.cur == len(state.tokens) - 1:
        _complete_document()
    else:
        state.cur += 1
        state.selected = None
    state.entries = get_entries()

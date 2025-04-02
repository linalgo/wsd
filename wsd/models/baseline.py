# pylint: disable=no-name-in-module,too-few-public-methods
"""A simple dictionary interface for JMDict."""
import json
import os
import uuid
from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import asdict, dataclass
from typing import Any

from fugashi import Tagger
from linalgo.annotate import Annotation, Annotator, Document, Entity, Task

from wsd.parsers import JMDictParser
from wsd.parsers.jmdict import Entry


@dataclass
class Token:
    """Token dataclass."""
    text: str = ''
    lemma: str = ''
    pos: str = ''


data_dir = os.path.join(os.path.dirname(__file__), '../../data')


class RankingModel(ABC):
    """Base class for the ranking models"""

    @abstractmethod
    def _rank(self, candidates: list[Entry], context: Any = None):
        """Rank results based on the given context.

        Parameters
        ----------
        candidates : List[Entry]
            A list of entries to rank
        context : any
            The context to use for ranking

        Returns
        -------
        List[Entry]
            The ranked list of entries
        """
        raise NotImplementedError


class JMDict(RankingModel):
    """A simple dictionary interface for JMDict."""

    entries = JMDictParser().parse(os.path.join(data_dir, 'JMdict_en.gz'))
    indexed = False

    def __init__(
        self,
        dictionary: str = None,
        annotator: Annotator = None
    ):
        if dictionary is not None:
            self.entries = JMDictParser.parse(dictionary)
        self.index = defaultdict(set)
        self.annotator = annotator or Annotator(
            id=uuid.uuid3(uuid.NAMESPACE_URL, 'jmdict-v3').hex,
            name='jmdict-v3',
            model='MACHINE',
            entity=Entity(id=os.getenv('LINHUB_ENTITY')),
            task=Task(id=os.getenv('LINHUB_TASK'))
        )
        self._index()

    def _index(self):
        """Create an index to speed up lookups."""
        if self.indexed:
            return
        for entry in self.entries:
            self.index[entry.ent_seq] = entry
            for k_ele in entry.k_ele:
                self.index[k_ele.keb].add(entry)
            for r_ele in entry.r_ele:
                self.index[r_ele.reb].add(entry)
        self.indexed = True

    def annotate(
        self,
        documents: Document | list[Document],
        feeling_lucky=False
    ) -> Document:
        """Annotate each token in a document with its (candidate) definitions.

        Parameters
        ----------
        doc : Document | List[Document]
            The documents to annotate.

        Returns
        -------
        Document | List[Document]
            The annotated documents.
        """
        if isinstance(documents, Document):
            documents = [documents]
        for doc in documents:
            start = 0
            for token in self.tokenize(doc.content):
                if feeling_lucky:
                    body = asdict(self.feeling_lucky(token.feture.lemma))
                else:
                    entries = self.search(token.feature.lemma)
                    body = [asdict(entry) for entry in entries]
                if body is not None:
                    a = Annotation(
                        document=doc,
                        body=json.dumps(body, ensure_ascii=False).encode('utf-8'),
                        start=start,
                        end=start + len(token.surface),
                        annotator=self.annotator,
                        entity=self.annotator.entity,
                        task=self.annotator.task
                    )
                    doc.annotations.add(a)
                start += len(token.surface)
        if len(documents) == 1:
            return documents[0]
        return documents

    def tokenize(self, sentence):
        """Tokenize a sentence.
        Parameters
        ----------
        sentence : str
            The sentence to tokenize

        Returns
        -------
        List[Token]
            A list of tokens.
        """
        tagger = Tagger('-Owakati')
        tokens = []
        for token in tagger(sentence):
            tokens.append(
                Token(
                    text=token.surface,
                    lemma=token.feature.lemma,
                    pos=token.pos
                )
            )
        return tokens

    def predict(self, sentences):
        """Predict the `ent_seq` for each token in a sentence.

        Parameters
        ----------
        sentences : Union[str, List[str]]
            The sentences to parse and query with the dictionary

        Returns
        -------
        preds : List[int]
            A list of predicted `ent_seq`.
        """
        if not hasattr(sentences, '__len__'):
            sentences = [sentences]
        preds = []
        for sentence in sentences:
            pred = []
            for token in self.tokenize(sentence):
                entry = self.feeling_lucky(token.lemma, context=token)
                ent_seq = entry.ent_seq if entry else None
                pred.append(ent_seq)
            preds.append(pred)
        return preds

    def get(self, ent_seq: str) -> Entry:
        """Get an entry by its `ent_seq`.

        Parameters
        ----------
        ent_seq : str
            The `ent_seq` of the entry to get

        Returns
        -------
        Entry
            The entry with the given `ent_seq`.
        """
        for entry in self.entries:
            if entry.ent_seq == ent_seq:
                return entry
        return None

    def _rank(self, candidates, context=None):
        """A base ranking function that does nothing.

        Parameters
        ----------
        candidates: List[Entry]
            The candidates to rank
        context : Any
            A contet to inform the ranking

        Returns
        -------
        candidates: List[Entry]
            The ranked candidates
        scores: List[float]
            The score of each candidate
        """
        return candidates, [1] * len(candidates)

    def _lookup(self, text):
        """Lookup an entry by text.

        Currently returns all entries that contain the text in either the kanji
        or reading.

        Parameters
        ----------
        text : str
            The text to search for

        Returns
        -------
        List[Entry]
            A list of entries that contain the query.
        """
        return list(self.index[text])

    def search(self, text: str, context=None) -> list[Entry]:
        """Search for an entry by text and rank the results.

        Currently returns all entries that contain the text in either the kanji
        or reading.

        Parameters
        ----------
        text : str
            The text to search for

        Returns
        -------
        List[Entry]
            A list of entries that contain the query.
        """
        return self._rank(self._lookup(text), context)

    def feeling_lucky(self, text: str, context=None) -> Entry:
        """Return the first entry found.

        Currently returns the first entry that contains the text in either the
        kanji or reading.

        Parameters
        ----------
        text : str
            The text to search for

        Returns
        -------
        Entry
            The first entry that contains the query.
        """
        entries = self.search(text, context)
        return entries[0] if entries else None


__all__ = ['JMDict', 'Token', 'RankingModel']

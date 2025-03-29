# pylint: disable=no-name-in-module,too-few-public-methods
"""A simple dictionary interface for JMDict."""
import os
from collections import defaultdict
from dataclasses import asdict, dataclass
from typing import Any

from fugashi import Tagger
from linalgo.annotate import Annotation, Document

from wsd.parsers import JMDictParser
from wsd.parsers.jmdict import Entry


@dataclass
class Token:
    """Token dataclass."""
    text: str = ''
    lemma: str = ''
    pos: str = ''


data_dir = os.path.join(os.path.dirname(__file__), '../../data')


class RankingModel:
    """Base class for the ranking models"""

    def rank(self, results: list[Entry], context: Any = None):
        """Rank results based on the given context.

        Parameters
        ----------
        results : List[Entry]
            A list of entries to rank
        context : any
            The context to use for ranking

        Returns
        -------
        List[Entry]
            The ranked list of entries
        """
        raise NotImplementedError


class JMDict:
    """A simple dictionary interface for JMDict."""

    def __init__(
        self,
        dictionary: str = 'JMdict_en.gz',
        ranking_model: RankingModel = None
    ):
        jmdict_file = os.path.join(data_dir, dictionary)
        self.entries = JMDictParser().parse(jmdict_file)
        self.ranking_model = ranking_model
        self.index = defaultdict(set)
        self._index()

    def _index(self):
        """Create an index to speed up lookups."""
        for entry in self.entries:
            self.index[entry.ent_seq] = entry
            for k_ele in entry.k_ele:
                self.index[k_ele.keb].add(entry)
            for r_ele in entry.r_ele:
                self.index[r_ele.reb].add(entry)

    def annotate(self, doc: Document) -> Document:
        """Annotate a document with entry definitions.

        Parameters
        ----------
        doc : Document
            The document to annotate

        Returns
        -------
        Document
            The annotated document
        """
        start = 0
        for token in self.tokenize(doc.content):
            entry = self.feeling_lucky(token.feature.lemma)
            if entry is not None:
                a = Annotation(
                    document=doc,
                    body=asdict(entry),
                    start=start,
                    end=start + len(token.surface)
                    )
                doc.annotations.add(a)
            start += len(token.surface)
        return doc

    def tokenize(self, sentence, form='all'):
        """Tokenize a sentence.
        Parameters
        ----------
        sentence : str
            The sentence to tokenize
        form : str, optional {'all', 'surface', 'lemma', 'pos'}, default 'all'
            The type of token to return. By default 'surface'

        Returns
        -------
        List[Token]
            A list of tokens.
        """
        tagger = Tagger('-Owakati')
        tokens = []
        for token in tagger(sentence):
            if form == 'all':
                tokens.append(token)
            elif form == 'lemma':
                tokens.append(token.feature.lemma)
            elif form == 'pos':
                tokens.append(token.pos)
            elif form == 'surface':
                tokens.append(token.surface)
            else:
                raise ValueError(f'Invalid form: {form}')
        return tokens

    def predict(self, sentence):
        """Predict the `ent_seq` for each token in a sentence.

        Parameters
        ----------
        sentence : str
            The sentence to parse and query with the dictionary

        Returns
        -------
        preds : List[int]
            A list of predicted `ent_seq`.
        """
        preds = []
        for token in self.tokenize(sentence, form='lemma'):
            entry = self.feeling_lucky(token)
            ent_seq = entry.ent_seq if entry else None
            preds.append(ent_seq)
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

    def search(self, text: str) -> list[Entry]:
        """Search for an entry by text.

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
        results = list(self.index[text])
        if self.ranking_model is not None:
            results = self.ranking_model.rank(results)
        return results

    def feeling_lucky(self, text: str) -> Entry:
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
        entries = self.search(text)
        return entries[0] if entries else None


__all__ = ['JMDict', 'Token']

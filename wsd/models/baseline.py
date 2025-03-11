"""A simple dictionary interface for JMDict."""
import os
from dataclasses import dataclass

from fugashi import Tagger  # pylint: disable=no-name-in-module

from wsd.parsers import JMDictParser
from wsd.parsers.jmdict import Entry


@dataclass
class Token:
    """Token dataclass."""
    text: str = ''
    lemma: str = ''
    pos: str = ''


data_dir = os.path.join(os.path.dirname(__file__), '../../data')


class JMDict:
    """A simple dictionary interface for JMDict."""

    def __init__(self, dictionary='JMdict_en.gz'):
        jmdict_file = os.path.join(data_dir, dictionary)
        self.entries = JMDictParser().parse(jmdict_file)

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

        tagger = Tagger('-Owakati')

        preds = []
        for word in tagger(sentence):
            entry = self.feeling_lucky(word.feature.lemma)
            ent_seq = entry.ent_seq if entry else None
            preds.append(ent_seq)
        return preds

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
        res = []
        for entry in self.entries:
            for k_ele in entry.k_ele:
                if k_ele.keb == text:
                    res.append(entry)
            for r_ele in entry.r_ele:
                if r_ele.reb == text:
                    res.append(entry)
        return res

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

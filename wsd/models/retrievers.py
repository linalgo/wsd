"""A collection of retrievers for WSD."""
from collections import defaultdict
from abc import ABC

from wsd.parsers import Entry, JMDictParser


class Retriever(ABC):
    """Base class for the searcher models"""

    def retrieve(self, text: str) -> list[Entry]:
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
        raise NotImplementedError("Subclasses must implement this method")

class LocalRetriever(Retriever):
    entries = None
    indexed = False

    def __init__(self, file=None, **kwargs):
        self.file = file
        self._index(self.file)

    def _index(self, filename):
        """Create an index to speed up lookups."""
        if self.indexed:
            return
        self.index = defaultdict(set)
        self.entries = JMDictParser.parse(filename)
        for entry in self.entries:
            self.index[entry.ent_seq] = entry
            for k_ele in entry.k_ele:
                self.index[k_ele.keb].add(entry)
            for r_ele in entry.r_ele:
                self.index[r_ele.reb].add(entry)
        self.indexed = True

    def retrieve(self, text) -> list[Entry]:
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

__all__ = ['LocalRetriever', 'Retriever']
"""A simple dictionary interface for JMDict."""
import os
from typing import List
from wsd.parsers import JMDictParser
from wsd.parsers.jmdict import Entry

data_dir = os.path.join(os.path.dirname(__file__), '../../data')

class JMDict:
    """A simple dictionary interface for JMDict"""

    def __init__(self):
        jmdict_file = os.path.join(data_dir, 'JMdict_en.gz')
        self.entries = JMDictParser().parse(jmdict_file)

    def search(self, text: str) -> List[Entry]:
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


__all__ = ['JMDict']

"""A simple dictionary interface for JMDict."""
from wsd.parsers import JMDictParser


class JMDict:
    """A simple dictionary interface for JMDict"""

    def __init__(self):
        self.entries = JMDictParser().parse('../data/JMdict_en.gz')

    def search(self, text):
        """Search for an entry by text.

        Currently returns all entries that contain the text in either the kanji 
        or reading.

        Parameters
        ----------
        text : str
            The text to search for
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

    def feeling_lucky(self, text):
        """Return the first entry found.

        Currently returns the first entry that contains the text in either the
        kanji or reading.

        Parameters
        ----------
        text : str
            The text to search for
        """
        entries = self.search(text)
        return entries[0] if entries else None


__all__ = ['JMDict']

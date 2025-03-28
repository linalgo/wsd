# pylint: disable=too-few-public-methods
"""A simple interface for the LinDict API."""

import requests

from wsd.parsers import Entry


class LinDictAPI:
    """A simple interface for the LinDict API."""

    @staticmethod
    def search(query) -> list[Entry]:
        """Search the dictionary using for the given query.

        Parameters
        ----------
        query : str
            The query string.

        Return
        ------
        entries : List[Entry]
            A list of entries.
        """
        url = f"https://lindict.api.linalgo.com/v1/ja/search/?query={query}"
        response = requests.get(url)  # pylint: disable=missing-timeout
        response.raise_for_status()
        if response.status_code != 200:
            return []
        data = response.json()
        entries = []
        for entry in data['results']:
            entries.append(Entry.from_dict(entry))
        return entries

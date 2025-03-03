import requests

from wsd.parsers import Entry

class LinDictAPI:
    """A simple interface for the LinDict API"""

    def search(self, query) -> Entry:
        url = f"https://lindict.api.linalgo.com/v1/ja/search/?query={query}"
        response = requests.get(url)
        response.raise_for_status()
        if response.status_code != 200:
            return []
        data = response.json()
        entries = []
        for entry in data['results']:
            entries.append(Entry.from_dict(entry))
        return entries
    
if __name__ ==  "__main__":
    lindict = LinDictAPI()
    entries = lindict.search('馬酔木')
    for entry in entries:
        print(entry)
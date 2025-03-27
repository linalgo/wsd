![main](https://github.com/linalgo/wsd/actions/workflows/trigger.yml/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![PyPI - Version](https://img.shields.io/pypi/v/wsd)

# Word Sense Disambiguation

## Installation

The easiest way to install `wsd` is to use pip:

```
pip install wsd
```

You will also need the [The JMDict Project](https://www.edrdg.org/jmdict/j_jmdict.html) dictionary. You can use the following helper to download the file:

```
python -m wsd download jmdict
```

## Getting Started

Currently, only `JMDict` model is available.
The model has not been trained yet and will currently returns all matching
entries found in the [The JMDict Project](https://www.edrdg.org/jmdict/j_jmdict.html).

The `JMDict` model can be imported from the `wsd.models` module:

```python
from wsd.models import JMDict

jmdict = JMDict()
```

From there, you can use it to search all relevant entries in the dictionary:

```python
for entry in jmdict.search("かんじ"):
    print(entry)
# Output:
# Entry(ent_seq='1210280', ...
# Entry(ent_seq='1211690', ...
# ...
```

Alternatively, you can use the `predict` method to get the unique `ent_seq` of
the best entry:

```python
jmdict.search("かんじ")
# Output:
# '1210280'
```

## Adding more data

The training data for `JMDict` is sourced from the [WSD Data Annotation Project](https://hub.linalgo.com/project/823b4545-5c97-4a22-b5f9-1bf75e620e4e).

To contribute more data:

- Create an account on [Linhub](https://hub.linalgo.com)
- Add your Linhub token to the `.env` file as `LINHUB_TOKEN`
- Run the annotation interface with the following command: `task annotate`

The annotation interface will be available at `https://localhost:32123/`.

## Training a model from scratch

TODO: Add instructions.

## Build using Docker

See [Using Docker](docker/README.md)

## Attribution and LICENSE

- [The JMDict Project](https://www.edrdg.org/jmdict/j_jmdict.html)
- [XL-WSD](https://sapienzanlp.github.io/xl-wsd/docs/data/)
- [Kanban](https://github.com/orgs/linalgo/projects/5)

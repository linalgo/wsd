![main](https://github.com/linalgo/wsd/actions/workflows/trigger.yml/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![PyPI - Version](https://img.shields.io/pypi/v/wsd)

# Practical Word Sense Disambiguation

Fast, efficient, open source & open data Word Sense Disambiguation models for practial use.

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
jmdict.predict("かんじ")
# Output:
# '1210280'
```

## Adding more data

To contribute more data:

- Create an account on [Linhub](https://hub.linalgo.com)
- Start reviewing entries using this [interface](https://hub.linalgo.com/interfaces/rank/ranking/a5040509-de9c-4757-8cb3-9087b5191a2e)

The interface has been designed to work on mobile phones to make it easy to
contribute whenever you have 5mn available.

## Training a model

First, you will need some data to train on. Currently, only the Japanese dataset
is available. You can download it with:

```shell
python -m wsd download dataset
```

Once the data is available locally. You can read it and train a model.

```python
import os

from sklearn.linear_model import LogisticRegression

from wsd.models import JMDictWithPointWiseRanking
from wsd.utils import load_dataset

basedir = os.getenv("PJ_DIR")
X, y = load_dataset(f"{basedir}/data/dataset.xml")
X = ["".join(x) for x in X]  # The baseline model already has a tokenizer.

model = LogisticRegression(C=10, penalty="l1", solver="liblinear")
jmdict = JMDictWithPointWiseRanking(ranking_model=model)
jmdict.fit(X, y)
jmdict.search("感じ")

# Output:
# Entry(ent_seq='1210280', ...
# Entry(ent_seq='1211690', ...
# ...
```

## Build using Docker

See [Using Docker](docker/README.md)

## Attribution and LICENSE

- [The JMDict Project](https://www.edrdg.org/jmdict/j_jmdict.html)
- [XL-WSD](https://sapienzanlp.github.io/xl-wsd/docs/data/)
- [Kanban](https://github.com/orgs/linalgo/projects/5)

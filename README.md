![main](https://github.com/linalgo/wsd/actions/workflows/trigger.yml/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![PyPI - Version](https://img.shields.io/pypi/v/wsd)

# Word Sense Disambiguation

## Installation

The easiest way to install `wsd` is to use pip:

```
pip install wsd
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

TODO: Add instructions.                               |

## Build the docker image

### Prerequisites

Before you begin, `deactivate your virtual environment if any` and  ensure you have met the following requirements:
Before you begin, `deactivate your virtual environment if any` and  ensure you have met the following requirements:

- [Git](https://git-scm.com)

- [Python](https://www.python.org/downloads/)

- [NPM](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)

- [Docker Desktop](https://docs.docker.com/desktop/install/linux-install/)

- [Python](https://www.python.org/downloads/)

- [NPM](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)

- [Docker Desktop](https://docs.docker.com/desktop/install/linux-install/)

  - [Install Docker Desktop on Mac](https://docs.docker.com/docker-for-mac/install/)
  - [Install Docker Desktop on Windows](https://docs.docker.com/desktop/install/windows-install/)
  - [Install Docker Desktop on Linux](https://docs.docker.com/desktop/install/linux-install/)

  * Make sure the following command doesn't return an error:

    ```bash
    docker image ls
    ```

- [Task](https://taskfile.dev/)

  - Install task

    ```bash
    sudo sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b /usr/local/bin
    ```

  - Make sure the following command doesn't return an error

    ```bash
    which task
    ```

- [uv](https://docs.astral.sh/uv/getting-started/installation/)

  - Install the `uv` package if not already installed:

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    sudo mv $HOME/.local/bin/uv /usr/local/bin/
    ```

  - Make sure the following command doesn't return an error

    ```bash
    which uv
    ```

### Installation

To set up the project, follow these steps:

1. **Clone the repository**:

   ```bash
   git clone git@github.com:linalgo/wsd.git
   cd wsd
   ```

2. **Copy environment variables and update as needed**:

   ```bash
   cp .env.example .env
   ```

3. **Create the virtual environment with uv**:

   ```bash
   uv venv --python=3.10 && source .venv/bin/activate
   ```

4. **Install [pre-commit](https://pre-commit.com/)**:

   If `pre-commit` is not already installed, you can install it using the following command:

   ```bash
    uv pip install pre-commit
    pre-commit run -a
   ```

5. **Build the wheel**:

   ```bash
   task build.wheel
   ```

6. **Build docker image**:

   ```bash
   task build.docker
   ```

7. **Access the Docker Container**:

   ```bash
   docker compose up dev -d
   docker exec -it wsd-dev bash
   ```

## Attribution and LICENSE

- [The JMDict Project](https://www.edrdg.org/jmdict/j_jmdict.html)
- [XL-WSD](https://sapienzanlp.github.io/xl-wsd/docs/data/)
- [Kanban](https://github.com/orgs/linalgo/projects/5)

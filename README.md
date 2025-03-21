<h1 align="center">
  <br>
  Word Sense Disambiguation
  </br>
</h1>

<p align="center">
  <a href="#modules">Modules</a> •
  <a href="#development">Development</a> •
  <a href="#resources">Resources</a>
</p>

# Modules

This repository consists of the following components:

| Component        | Description                                                                   |
| ---------------- | ----------------------------------------------------------------------------- |
| **wsd**          | Contains the implementation of Word Sense Disambiguation models               |
| **wsd.annotate** | Includes the annotation user interface and related logic                      |
| **wsd.lindict**  | A simple interface for the LinDict API, used to search for dictionary entries |
| **wsd.parsers**  | Contains parsers for various data sources, including JMDict and XL-WSD        |
| **wsd.models**   | Contains data models such as Token and Entry used within the WSD framework    |
| **wsd.configs**  | Contains all configurations for the annotation procedure                      |
| **wsd.tests**    | Unit tests for the application                                                |

# Development

## Prerequisites

Before you begin, ensure you have met the following requirements:

- [Git](https://git-scm.com)
- Docker Desktop
  - [Install Docker Desktop on Mac](https://docs.docker.com/docker-for-mac/install/)
  - [Install Docker Desktop on Windows](https://docs.docker.com/desktop/install/windows-install/)
  - [Install Docker Desktop on Linux](https://docs.docker.com/desktop/install/linux-install/)
- [Python](https://www.python.org/downloads/)
- [NPM](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Task](https://taskfile.dev/)

## Installation

To set up the project, follow these steps:

1. Clone the repository:

   ```bash
   git clone git@github.com:linalgo/wsd.git
   cd wsd
   ```

2. Install the `uv` package if not already installed:

   ```bash
   if ! which uv > /dev/null 2>&1; then
     echo "Installing uv...";
     curl -LsSf https://astral.sh/uv/install.sh | sh;
     sudo mv $HOME/.local/bin/uv /usr/local/bin/
   else
     echo "uv is already installed.";
   fi
   ```

3. Install pre-commit for the code formatting

   ```bash
   uv pip install pre-commit=='3.8.0'
   pre-commit install
   pre-commit run --all-files
   ```

4. Install `task` by following instructions [here](https://taskfile.dev/).

5. Build and launch the dev container:

   ```bash
   task build && docker compose up dev -d
   ```

6. Connect to the container:

   ```bash
   docker exec -it wsd-dev
   ```

## Annotate New Data

### Requirements

- Get a developer token from [Linhub](https://hub.linalgo.com) and add it to the `.env` file as `LINHUB_TOKEN`.

### Start Annotation Server

After setting up, you can start the annotation interface by running:

```bash
task annotate
```

The annotation interface will be available at `https://localhost:32123/`.

# Resources

## Attribution and LICENSE

- [The JMDict Project](https://www.edrdg.org/jmdict/j_jmdict.html)
- [XL-WSD](https://sapienzanlp.github.io/xl-wsd/docs/data/)
- [Kanban](https://github.com/orgs/linalgo/projects/5)

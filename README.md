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

## Installation

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
- [Kanban](https://github.com/orgs/linalgo/projects/5)
- [Kanban](https://github.com/orgs/linalgo/projects/5)

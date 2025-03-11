# Word Sense Disambiguation

Let's build a state-of-the-art multi-lingual Word Sense Disambiguation model.

## Project resources
- [Kanban](https://github.com/orgs/linalgo/projects/5)


## Build dev environemtn

Run `task build && docker compose up dev -d`.
Connect to the container using Visual Code.

## Installation

Run `task install`.

## Annotate new data

### Requirements

- [Install NPM](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
- Get a developper token from [Linhub](https://hub.linalgo.com) and add it to the `.env` file as `LINHUB_TOKEN`.

### Start annotation server
Then, run `task annotate`. The annotation interface will be available at 
`https://localhost:32123/`.

## Attribution and LICENSE
- [The JMDict Project](https://www.edrdg.org/jmdict/j_jmdict.html)
- [XL-WSD](https://sapienzanlp.github.io/xl-wsd/docs/data/)

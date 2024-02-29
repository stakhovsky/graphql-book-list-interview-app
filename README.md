# graphql-book-list-interview-app

Example project that provides dummy read-only graphql API.

## Development

Development is aimed to use on-host `python` and containerized environment.

So you have to install `python 3.12` (and other required packages) locally (see [pyenv](https://github.com/pyenv/pyenv)).

### Environment and requirements

- `python 3.12`, `poetry`, `strawberry` and so on (see [pyproject.toml](./pyproject.toml) and [Dockerfile](./Dockerfile))
- `postgresql 15` (see [docker-compose.yml](./docker-compose.yml))
- `docker 24.0.x+` with `compose` plugin

### Useful commands

> See [Makefile](./Makefile)

- `make run` - run local development server
- `make lint` - linting
- `make migrate` - run migrations for db
- `docker compose --profile infra up` - run project infrastructure
- `python -m pytest`/`poetry run pytest` - run tests

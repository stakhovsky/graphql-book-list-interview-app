FROM python:3.12.2-slim-bookworm as application

WORKDIR /app

RUN apt-get update && \
    apt-get install -y \
        libpq-dev && \
    rm -rf /var/lib/apt/lists/*
RUN pip install \
        pip==24.0 \
        poetry==1.7.1

ADD graphql_book_list_interview_app graphql_book_list_interview_app
ADD pyproject.toml pyproject.toml
ADD poetry.lock poetry.lock
ADD README.md README.md
RUN poetry install --without dev

CMD ["poetry", "run", "uvicorn", "--factory", "graphql_book_list_interview_app.app:make_app"]

FROM application as tests

WORKDIR /app

ADD tests tests
RUN poetry install --only dev

CMD ["poetry", "run", "pytest", "tests"]

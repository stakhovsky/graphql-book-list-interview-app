import os

import pytest
import pytest_asyncio
import starlette.testclient
import strawberry.test
import strawberry.asgi.test
import yoyo  # type: ignore[import-untyped]

import graphql_book_list_interview_app.app as app
import graphql_book_list_interview_app.settings as settings


@pytest.fixture(
    scope="session",
)
def config() -> settings.Settings:
    return settings.Settings()  # type: ignore[call-arg]


@pytest_asyncio.fixture
async def http_client(
    config: settings.Settings,
) -> starlette.testclient.TestClient:
    with starlette.testclient.TestClient(
        app=app.make_app(
            config=config,
        ),
    ) as client:
        yield client


@pytest.fixture
def graphql_client(
    http_client: starlette.testclient.TestClient,
) -> strawberry.test.BaseGraphQLTestClient:
    return strawberry.asgi.test.GraphQLTestClient(
        client=http_client,
        url="/graphql",
    )


@pytest.fixture(
    scope="session",
    autouse=True,
)
def _migrate(
    config: settings.Settings,
) -> None:
    database = yoyo.get_backend(
        uri=config.migration_db_dsn,
    )
    migrations = yoyo.read_migrations(
        os.path.join(os.path.dirname(app.__file__), "migrations"),
    )
    for migration in database.to_apply(migrations):
        database.apply_one(migration)

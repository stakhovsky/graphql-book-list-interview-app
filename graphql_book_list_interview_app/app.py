import contextlib
import functools
import typing

import databases
import fastapi

import graphql_book_list_interview_app.router as router
import graphql_book_list_interview_app.settings as settings
import graphql_book_list_interview_app.version as version


def setup_routes(
    app: fastapi.FastAPI,
    db: databases.Database,
) -> None:
    app.include_router(
        router.create_router(
            db=db,
        ),
        prefix="/graphql",
    )


@contextlib.asynccontextmanager
async def lifespan(
    app: fastapi.FastAPI,
    config: settings.Settings,
):
    db = databases.Database(
        url=config.db_dsn,
    )

    async with db:
        try:
            setup_routes(
                app=app,
                db=db,
            )

            yield
        finally:
            await db.disconnect()


def make_app(
    config: typing.Optional[settings.Settings] = None,
) -> fastapi.FastAPI:
    if config is None:
        config = settings.Settings()  # type: ignore[call-arg]
    app = fastapi.FastAPI(
        title=version.__app__,
        version=version.__version__,
        lifespan=functools.partial(
            lifespan,
            config=config,
        ),
    )
    return app

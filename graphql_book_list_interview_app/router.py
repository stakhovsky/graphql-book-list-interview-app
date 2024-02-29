import databases
import strawberry
import strawberry.types as strawberry_types
import strawberry.fastapi as strawberry_fastapi

import graphql_book_list_interview_app.constant as constant
import graphql_book_list_interview_app.entity as entity
import graphql_book_list_interview_app.usecase as usecase


class Context(strawberry_fastapi.BaseContext):
    db: databases.Database

    def __init__(
        self,
        db: databases.Database,
    ) -> None:
        super().__init__()
        self.db = db


@strawberry.type
class Query:

    @strawberry.field
    async def authors(
        self,
        info: strawberry_types.Info[Context, None],
        limit: int = constant.MAX_PER_PAGE,
        offset: int = 0,
    ) -> entity.PaginationWindow[entity.Author]:
        return await usecase.index_authors(
            db=info.context.db,
            pagination=entity.PaginationConfig(
                limit=limit,
                offset=offset,
            ),
        )

    @strawberry.field
    async def books(
        self,
        info: strawberry_types.Info[Context, None],
        author_ids: list[int] | None = None,
        search: str | None = None,
        limit: int = constant.MAX_PER_PAGE,
        offset: int = 0,
    ) -> entity.PaginationWindow[entity.Book]:
        return await usecase.index_books(
            db=info.context.db,
            filters=entity.BookFilters(
                author_ids=author_ids,
                search=search,
            ),
            pagination=entity.PaginationConfig(
                limit=limit,
                offset=offset,
            ),
        )


def create_router(
    db: databases.Database,
) -> strawberry_fastapi.GraphQLRouter:
    schema = strawberry.Schema(query=Query)
    return strawberry_fastapi.GraphQLRouter(
        schema,
        context_getter=lambda: Context(db=db),
    )


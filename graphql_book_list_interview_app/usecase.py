import databases

import graphql_book_list_interview_app.entity as entity


async def index_books(
    db: databases.Database,
    pagination: entity.PaginationConfig,
    filters: entity.BookFilters,
) -> entity.PaginationWindow[entity.Book]:
    # TODO:
    return entity.PaginationWindow(
        items=[],
        total=0,
    )

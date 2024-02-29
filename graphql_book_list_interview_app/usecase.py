import dataclasses

import databases

import graphql_book_list_interview_app.entity as entity


async def index_authors(
    db: databases.Database,
    pagination: entity.PaginationConfig,
) -> entity.PaginationWindow[entity.Author]:
    items_query = """
        SELECT 
            id, name
        FROM 
            authors
        ORDER BY id
        LIMIT :limit
        OFFSET :offset
    """
    total_query = """
        SELECT 
            COUNT(id)
        FROM 
            authors
    """

    items = []
    async for record in db.iterate(
        query=items_query,
        values=dataclasses.asdict(pagination),
    ):
        items.append(
            entity.Author(
                id=record["id"],
                name=record["name"],
            ),
        )
    total = await db.fetch_val(
        query=total_query,
    )

    return entity.PaginationWindow(
        items=items,
        total=total,
    )


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

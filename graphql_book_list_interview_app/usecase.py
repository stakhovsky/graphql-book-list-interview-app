import typing
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
    items_query = """
        SELECT 
            books.id AS book_id,
            books.title AS book_title,
            authors.id AS author_id,
            authors.name AS author_name
        FROM 
            books INNER JOIN authors ON books.author_id = authors.id
    """
    items_values = dataclasses.asdict(pagination)
    total_query = """
        SELECT 
            COUNT(id)
        FROM 
            books
    """
    total_values: dict[str, typing.Any] = {}

    where_filters = []
    if filters.author_ids:
        where_filters.append("books.author_id = ANY(:author_ids)")
        items_values["author_ids"] = filters.author_ids
        total_values["author_ids"] = filters.author_ids
    if filters.search:
        where_filters.append("books.title ~* :search")
        items_values["search"] = filters.search
        total_values["search"] = filters.search

    if where_filters:
        where_clause = f"\nWHERE {' AND '.join(where_filters)}"
        items_query += where_clause
        total_query += where_clause

    items_query += """
        ORDER BY book_id
        LIMIT :limit
        OFFSET :offset
    """

    items = []
    async for record in db.iterate(
        query=items_query,
        values=items_values,
    ):
        items.append(
            entity.Book(
                id=record["book_id"],
                title=record["book_title"],
                author=entity.Author(
                    id=record["author_id"],
                    name=record["author_name"],
                ),
            ),
        )
    total = await db.fetch_val(
        query=total_query,
        values=total_values,
    )

    return entity.PaginationWindow(
        items=items,
        total=total,
    )

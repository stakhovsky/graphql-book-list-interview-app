import pytest
import strawberry.test


@pytest.mark.parametrize(
    "query, expected_data",
    (
        pytest.param(
            """
                query TestIndexNoFilter {
                  books(limit: 2) {
                    items {
                      id
                    }
                    total
                  }
                }
            """,
            {
                "books": {
                    "items": [
                        {
                            "id": 1,
                        },
                        {
                            "id": 2,
                        },
                    ],
                    "total": 7,
                },
            },
            id="no-filter",
        ),
        pytest.param(
            """
                query TestIndexByTitle {
                  books(search: "dorian") {
                    items {
                      id
                    }
                  }
                }
            """,
            {
                "books": {
                    "items": [
                        {
                            "id": 1,
                        },
                    ],
                },
            },
            id="by-title",
        ),
        pytest.param(
            """
                query TestIndexByAuthor {
                  books(authorIds: [3]) {
                    items {
                      id
                    }
                  }
                }
            """,
            {
                "books": {
                    "items": [
                        {
                            "id": 6,
                        },
                        {
                            "id": 7,
                        },
                    ],
                },
            },
            id="by-author-id",
        ),
    ),
)
def test_index(
    graphql_client: strawberry.test.BaseGraphQLTestClient,
    query: str,
    expected_data: dict,
) -> None:
    response: strawberry.test.Response = graphql_client.query(  # type: ignore[assignment]
        query=query,
    )

    assert response.data == expected_data

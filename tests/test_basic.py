import starlette.testclient
import strawberry.test


def test_http_openapi_version(
    http_client: starlette.testclient.TestClient,
) -> None:
    response = http_client.get("/openapi.json")

    assert response.status_code == 200
    assert response.json()["info"]["version"] is not None


def test_graphql_endpoint(
    graphql_client: strawberry.test.BaseGraphQLTestClient,
) -> None:
    response: strawberry.test.Response = graphql_client.query(  # type: ignore[assignment]
        query="""
            query test {
              __typename
            }
        """,
    )

    assert response.data == {"__typename": "Query"}

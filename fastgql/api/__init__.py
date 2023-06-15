from strawberry.asgi import GraphQL


def create_graphql() -> GraphQL:
    from .schema import schema

    return GraphQL(schema)  # type: ignore[var-annotated]

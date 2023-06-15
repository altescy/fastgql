from fastapi import FastAPI
from strawberry.asgi import GraphQL


def create_app() -> FastAPI:
    from fastgql.api.schema import schema
    from fastgql.database import init_database

    graphql_app = GraphQL(schema)  # type: ignore[var-annotated]

    app = FastAPI()
    app.mount("/graphql", graphql_app)

    @app.on_event("startup")
    async def startup() -> None:
        await init_database()

    return app

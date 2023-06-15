from fastapi import FastAPI

from fastgql.api import create_graphql
from fastgql.database import init_database


def create_app() -> FastAPI:
    app = FastAPI()
    app.mount("/graphql", create_graphql())

    @app.on_event("startup")
    async def startup() -> None:
        await init_database()

    return app

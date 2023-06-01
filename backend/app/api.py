"""Main code for backend api"""

from typing import Dict

from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
import uvicorn

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from automap import automap_db

import utils.db_parameters as db


# from routes.crud.tenders import TendersRouter


# FastAPI app instance:
app = FastAPI()

origins = ["http://localhost:3000", "localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create engine to connect to the database:
engine = create_engine(
    f"cockroachdb://{db.USERNAME}:{db.PASSWORD}@{db.HOST}:{db.PORT}/{db.DB_NAME}"
)

# Mapping data model from database:
dm = automap_db(engine, db.SCHEMA)


# Register the routes with the app:
# app.include_router(TendersRouter(dm), prefix="/api/crud/tenders", tags=["tender"])


# async def create_pool() -> asyncpg.pool.Pool:
#     """Create a PostgreSQL connection pool."""
#     return await asyncpg.create_pool(
#         min_size=1,
#         max_size=10,
#         host=db.HOST,
#         port=db.PORT,
#         database=db.DB_NAME,
#         user=db.USERNAME,
#         password=db.PASSWORD,
#     )


# @app.on_event("startup")
# async def startup_event():
#     """Create a connection pool on startup and store it in the app state."""
#     app.state.pool = await create_pool()


# @app.on_event("shutdown")
# async def shutdown_event():
#     """Close all connections in the connection pool when the application shuts down."""
#     await app.state.pool.close()


# @app.exception_handler(asyncpg.PostgresError)
# def database_exc_handler(*args) -> JSONResponse:  # pylint: disable=unused-argument
#     """Handles database errors returning a database error message."""
#     # pylint: disable=unused-import
#     return JSONResponse(status_code=500, content={"message": "Database error"})


# async def get_conn() -> asyncpg.Connection:
#     """Get a connection from the connection pool."""
#     async with app.state.pool.acquire() as conn:
#         yield conn


# @app.get("/example/rds")
# async def example_rds(
#     conn: asyncpg.Connection = Depends(get_conn),
# ) -> Dict[str, str]:
#     """An example endpoint that requires a database connection"""
#     # return {"version": await conn.fetchval("SELECT version()")}
#     return {
#         "schemas": await conn.fetchval(
#             "SELECT schema_name FROM information_schema.schemata;"
#         )
#     }


@app.get("/actuator/health")
def heartbeat():
    """Method to test app endpoint during deployment"""

    return {"status": "up"}


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """Method to return favicon"""

    return FileResponse("favicon.ico")


# Mounting the static files directory (serving frontend from backend):
app.mount("/", StaticFiles(directory="static/", html=True), name="static")


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)

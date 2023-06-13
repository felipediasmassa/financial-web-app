"""Main code for backend api"""


from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import utils.database as db

from routes.crud.transactions import TransactionsRouter


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
engine = create_engine(db.get_db_url())

# Mapping data model from database:
dm = db.automap_db(engine)


@app.middleware("http")
async def db_session_middleware(request, call_next):
    """
    Middleware to automatically open database session before each API method is executed and to
    close it as soon as method returns response

    This method is called before every other request
    """

    response = None

    try:
        # Create a new database session for each request:
        session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        request.state.db = session()
        response = await call_next(request)  # here the actual method is triggered
    finally:
        # Close the database session after each request:
        request.state.db.close()

    return response


@app.get("/actuator/health")
def heartbeat():
    """Method to test app endpoint during deployment"""
    return {"status": "up"}


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """Method to return favicon"""
    return FileResponse("favicon.ico")


# Register the routes with the app:
app.include_router(
    TransactionsRouter(dm),
    prefix="/api/crud/transactions",
    tags=["transaction"],
)

# Mounting the static files directory (serving frontend from backend):
app.mount("/", StaticFiles(directory="static/", html=True), name="static")


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)

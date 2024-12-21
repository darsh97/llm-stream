from fastapi import FastAPI
from router import router
from logger import Logger

logger = Logger()

# Initialize the FastAPI app
app = FastAPI(
    title="Poem Generator API",

)

app.include_router(router, prefix="/api", tags=["generatez"])

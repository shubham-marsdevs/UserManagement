from fastapi import FastAPI
from dotenv import load_dotenv

from app.users import user_router
from app.authentication import authentication_router


load_dotenv()

app = FastAPI()
app.include_router(user_router, prefix="/api")
app.include_router(authentication_router, prefix="/api")


@app.get("/")
async def root():
    return {
        "Message": "User Create API's",
        "To use OpenAPI": "use this endpoint /docs"
    }
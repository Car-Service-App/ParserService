import uvicorn
from fastapi import FastAPI

from routes import routes

app = FastAPI()

app.include_router(routes)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)

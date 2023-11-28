import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import default, tags, statements, users, connections
import load_env

app = FastAPI()

for router in [default.router, tags.router, statements.router, users.router, connections.router]:
    app.include_router(router)

app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], )


def run():
    settings = load_env.load_settings_from_env("API_HOST", "API_PORT")
    uvicorn.run(app, host=settings["API_HOST"], port=int(settings["API_PORT"]))

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import default, tags, statements, users, connections

app = FastAPI()

for router in [default.router, tags.router, statements.router, users.router, connections.router]:
    app.include_router(router)

app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], )


def run(host, port):
    uvicorn.run(app, host=host, port=port)








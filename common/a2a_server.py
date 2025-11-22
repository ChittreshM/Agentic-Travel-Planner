from fastapi import FastAPI
import uvicorn

def create_app(agent):
    app = FastAPI()

    @app.get("/health")
    async def health():
        return {"status": "healthy"}

    @app.post("/run")
    async def run(payload: dict):
        return await agent.execute(payload)

    return app

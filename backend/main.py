import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from routes.llm_routes import router
app=FastAPI(title="AI Job Coach Assistant ")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router,prefix="/api")
@app.get("/")
def serve_homepage():
    frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "index.html")
    print(frontend_path)
    return FileResponse(frontend_path)


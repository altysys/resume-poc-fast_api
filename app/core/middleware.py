# app/core/middleware.py

from fastapi.middleware.cors import CORSMiddleware

def add_cors_middleware(app):
    origins = [
    "https://resume-ai-frontend-flame.vercel.app",  # Your frontend URL
    "http://localhost",  # Base for localhost
    "http://localhost:3000",  # Additional local port
]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins (for development; restrict in production)
        allow_credentials=True,
        allow_methods=["*"],  # Allow all HTTP methods
        allow_headers=["*"],  # Allow all headers
    )

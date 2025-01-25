from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.resume_router import router as resume_router
from app.core.middleware import add_cors_middleware

# Initialize FastAPI application
app = FastAPI(
    title="Resume Parser API",
    description="API for parsing and analyzing resumes against job descriptions",
    version="1.0.0"
)

# List of origins that are allowed to make requests to the backend
origins = [
    "https://resume-ai-frontend-flame.vercel.app",  # Your frontend URL
    "http://localhost",  # Base for localhost
    "http://localhost:3000",  # Additional local port
]

# Function to dynamically add origins if needed
def dynamic_allow_origins():
    return origins + [
        f"{origin}:{port}" for origin in origins for port in range(3000, 3100)
    ]

# Add CORSMiddleware to the FastAPI app
def add_cors_middleware(app):
    """
    Adds CORS middleware to the FastAPI application.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=dynamic_allow_origins(),  # Dynamically add allowed origins
        allow_credentials=True,
        allow_methods=["*"],  # Allow all HTTP methods
        allow_headers=["*"],  # Allow all headers
    )

# Apply the CORS middleware to the app
add_cors_middleware(app)

# Register the resume router
app.include_router(resume_router)

# Print registered routes during startup
@app.on_event("startup")
async def startup_event():
    print("Startup: Listing all available routes...")
    for route in app.routes:
        methods = ", ".join(route.methods)
        print(f"{methods} {route.path}")

# Prevent unnecessary duplicate route registration
if __name__ == "__main__":  # Corrected the typo here
    print("FastAPI application is ready.")

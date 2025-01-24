from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.resume_router import router as resume_router

app = FastAPI(
    title="Resume Parser API",
    description="API for parsing and analyzing resumes against job descriptions",
    version="1.0.0"
)

# Middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust the origins as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
if __name__ == "__main__":
    print("FastAPI application is ready.")

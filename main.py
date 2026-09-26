from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from api.contacts import router as contacts_router
from api.auth import router as auth_router
from api.users import limiter, router as users_router


app = FastAPI(
    title="Contacts API",
    description="API for managing contacts",
    version="1.0.0",
)

# allow cross-origin requests to the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"error": "Request limit exceeded. Please try again later."},
    )

app.include_router(auth_router)
app.include_router(contacts_router)
app.include_router(users_router)
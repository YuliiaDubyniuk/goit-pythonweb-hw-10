from fastapi import FastAPI

from api.contacts import router as contacts_router
from api.auth import router as auth_router


app = FastAPI(
    title="Contacts API",
    description="API for managing contacts",
    version="1.0.0",
)

app.include_router(auth_router)
app.include_router(contacts_router)
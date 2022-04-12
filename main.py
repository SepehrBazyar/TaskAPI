import uvicorn
from core import AuthStaticFiles, VersionFastAPI
from db import (
    connect_to_postgresql,
    close_postgresql_connection,
)
from api import latest, versions, dependencies


app = VersionFastAPI()()
app.include_router(latest)


# Event Handlers
# Startup
app.add_event_handler("startup", connect_to_postgresql)

# Shutdown
app.add_event_handler("shutdown", close_postgresql_connection)


# Mount SubAPI Versions
for version in versions:
    app.mount(f"/v{version.version}", version)


# Mount Media Static Files
app.mount(
    name="media",
    path="/media",
    app=AuthStaticFiles(
        directory="media",
        authorizes=dependencies,
    ),
)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="debug")

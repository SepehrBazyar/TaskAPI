import uvicorn
from core import VersionFastAPI
from db import (
    connect_to_postgresql,
    close_postgresql_connection,
)
from api import (
    v1_0_0,
)


app = VersionFastAPI()()


# Event Handlers
# Startup
app.add_event_handler("startup", connect_to_postgresql)

# Shutdown
app.add_event_handler("shutdown", close_postgresql_connection)


# Mount SubAPI Versions
app.mount(f"/v{v1_0_0.version}", v1_0_0)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="debug")

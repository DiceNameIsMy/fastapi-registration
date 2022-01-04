import fastapi

from settings import settings

import api_v1


app = fastapi.FastAPI(
    debug=settings.debug,
    title=settings.title,
)
app.include_router(api_v1.router)

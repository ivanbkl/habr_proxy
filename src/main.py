from typing import Any

from aiohttp import ClientSession
from fastapi import FastAPI, Request, Response
from uvicorn import run

from proxy import get_response
from settings import ProxySettings

app = FastAPI(
    docs_url=None,
    redoc_url=None
)


@app.on_event("startup")
async def startup_event() -> None:
    """Add client session connector to app's state"""
    app.state.client_session = ClientSession()


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Close client session connector in app's state"""
    await app.state.client_session.close()


@app.get("/{path:path}", response_class=Response)
async def proxy_get(path: str, request: Request) -> Any:
    return await get_response(request)


if __name__ == '__main__':
    run(
        app,
        host=ProxySettings.HOST,
        port=ProxySettings.PORT,
        server_header=False,
        date_header=False
    )

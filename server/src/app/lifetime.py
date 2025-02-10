from fastapi import FastAPI
from typing import Awaitable, Callable


def register_startup_event(app: FastAPI,) -> Callable[[], Awaitable [None]]: # pragma: no cove
    """
    Actions to run on application startup.

    This function uses fastAPI app to store data in the state, such as db_engine.

    :param app: the fastAPI application.

    return: function that actually performs actions.

    """

    @app.on_event("startup")
    async def _startup() ->None:
        pass
    
    return _startup


def register_shutdown_event(app: FastAPI,) -> Callable[[], Awaitable [None]]: # pragma: no cove
    """
    Actions to run on application startup.

    This function uses fastAPI app to store data in the state, such as db_engine.

    :param app: the fastAPI application.

    return: function that actually performs actions.

    """

    @app.on_event("shutdown")
    async def _shutdown() ->None:
        pass
    
    return _shutdown
import os
import logging
import functools
from dataclasses import dataclass
from contextlib import asynccontextmanager
from typing import AsyncIterator, Callable
from mcp.server.fastmcp import FastMCP
from cterasdk import AsyncEdge, settings
from cterasdk.exceptions import SessionExpired


logger = logging.getLogger('ctera.mcp.edge')
logger.info("Starting CTERA Edge Model Context Protocol [MCP] Server.")


@dataclass
class Env:

    __namespace__ = 'ctera.mcp.edge.settings'

    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.port = int(os.environ.get(f'{Env.__namespace__}.port', 443))
        # Handle SSL setting as either boolean or string
        ssl_env = os.environ.get(f'{Env.__namespace__}.connector.ssl', 'True')
        if isinstance(ssl_env, bool):
            self.ssl = ssl_env
        else:
            # Convert string to boolean - handle 'False', 'false', '0', etc.
            self.ssl = ssl_env.lower() not in ('false', '0', 'no', 'off')

    @staticmethod
    def load():
        host = os.environ.get(f'{Env.__namespace__}.host', None)
        user = os.environ.get(f'{Env.__namespace__}.user', None)
        password = os.environ.get(f'{Env.__namespace__}.password', None)
        return Env(host, user, password)


@dataclass
class EdgeContext:

    def __init__(self, edge, env: Env):
        settings.edge.asyn.settings.connector.ssl = env.ssl
        self._session = edge(env.host, env.port)
        self._user = env.user
        self._password = env.password

    @property
    def session(self):
        return self._session

    async def login(self):
        """
        Login.
        """
        await self.session.login(self._user, self._password)

    async def logout(self):
        """
        Logout.
        """
        await self.session.logout()

    @staticmethod  
    def initialize(env: Env):
        """
        Initialize Edge Context.
        """
        return EdgeContext(AsyncEdge, env)


@asynccontextmanager
async def ctera_lifespan(mcp: FastMCP) -> AsyncIterator[EdgeContext]:   
    env = Env.load()
    user = EdgeContext.initialize(env)
    try:
        await user.login()
        yield user
    finally:
        await user.logout()


mcp = FastMCP("ctera-edge-mcp-server", lifespan=ctera_lifespan)


def with_session_refresh(function: Callable) -> Callable:
    """
    Decorator to handle session expiration and automatic refresh.

    Args:
        function: The function to wrap with session refresh logic

    Returns:
        Wrapped function that handles session refresh
    """
    @functools.wraps(function)
    async def wrapper(*args, **kwargs):
        # Extract context from kwargs or args
        ctx = kwargs.get('ctx')
        if ctx is None:
            # Look for Context in args
            from mcp.server.fastmcp import Context
            for arg in args:
                if isinstance(arg, Context):
                    ctx = arg
                    break

        if ctx is None:
            raise ValueError("Context not found in function arguments")

        # Get the edge context which contains the session and credentials
        edge_context = ctx.request_context.lifespan_context
        if edge_context is None:
            raise Exception("Edge connection not available. Please check environment variables.")

        try:
            return await function(*args, **kwargs)
        except SessionExpired:
            await edge_context.login()
            # Try the original function
            return await function(*args, **kwargs)
        except Exception as e:
            logger.error(f'Uncaught exception: {e}')

            # Check if it's a session expired error (multiple ways to detect)
            error_msg = str(e).lower()
            is_session_error = (
                isinstance(e, SessionExpired) or
                "session expired" in error_msg or 
                "session invalid" in error_msg or
                "unauthorized" in error_msg or
                "authentication" in error_msg or
                "401" in error_msg
            )

            if is_session_error:
                logger.info(f"Session expired or authentication error detected: {e}")
                logger.info("Attempting to refresh session...")
                try:
                    # Re-authenticate using the stored credentials in edge_context
                    await edge_context.login()
                    logger.info("Session refreshed successfully, retrying operation...")
                    # Retry the function
                    return await function(*args, **kwargs)
                except Exception as refresh_error:
                    logger.error(f"Failed to refresh session: {refresh_error}")
                    raise Exception(f"Session refresh failed: {refresh_error}") from e
            else:
                # If it's another error, log and re-raise it
                logger.error(f'Uncaught exception in {function.__name__}: {e}')
                raise

    return wrapper

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
logger.info("Starting CTERA Edge Filer Model Context Protocol [MCP] Server.")


@dataclass
class Env:

    __namespace__ = 'ctera.mcp.edge.settings'

    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.port = int(os.environ.get(f'{Env.__namespace__}.port', 443))
        ssl = os.environ.get(f'{Env.__namespace__}.ssl', None)
        self.ssl = False if ssl in ['false', False] else True

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
        self._session = edge(base=env.host) if env.host.startswith('https') else edge(env.host, env.port)
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
        ctx = kwargs.get('ctx')
        if not ctx:
            raise ValueError("Context is required")
        user = ctx.request_context.lifespan_context.session
        try:
            return await function(*args, **kwargs)
        except SessionExpired:
            await user.login()
            return await function(*args, **kwargs)
        except Exception as e:
            logger.error(f'Uncaught exception: {e}')

    return wrapper

from common import mcp, with_session_refresh
from mcp.server.fastmcp import Context


@mcp.tool()
@with_session_refresh
async def ctera_edge_filer_who_am_i(ctx: Context) -> str:
    edge = ctx.request_context.lifespan_context.session
    session = await edge.api.get('/currentuser')
    username = session.username
    return f'Authenticated as {username}'


@mcp.tool()
@with_session_refresh
async def ctera_edge_filer_list_dir(path: str, ctx: Context) -> list[dict]:
    edge = ctx.request_context.lifespan_context.session
    return [{
        'name': f.name,
        'type': f.type,
        'fullpath': f.fullpath,
        'hasSubfolders': f.hasSubfolders,
        'last_modified': f.modificationTime,
    } for f in await edge.files.listdir(path)]


@mcp.tool()
@with_session_refresh
async def ctera_edge_filer_create_directory(path: str, ctx: Context) -> str:
    edge = ctx.request_context.lifespan_context.session
    await edge.files.mkdir(path)
    return f"Created: {path}"


@mcp.tool()
@with_session_refresh
async def ctera_edge_filer_makedirs(path: str, ctx: Context) -> str:
    edge = ctx.request_context.lifespan_context.session
    await edge.files.makedirs(path)
    return f"Created: {path}"


@mcp.tool()
@with_session_refresh
async def ctera_edge_filer_copy_item(
    source: str, destination: str, ctx: Context
) -> str:
    edge = ctx.request_context.lifespan_context.session
    await edge.files.copy(source, destination)
    return f"Copied: {source} to: {destination}"


@mcp.tool()
@with_session_refresh
async def ctera_edge_filer_move_item(
    source: str, destination: str, ctx: Context
) -> str:
    edge = ctx.request_context.lifespan_context.session
    await edge.files.move(source, destination)
    return f"Moved: {source} to: {destination}"


@mcp.tool()
@with_session_refresh
async def ctera_edge_filer_delete_item(paths: list[str], ctx: Context) -> str:
    edge = ctx.request_context.lifespan_context.session
    await edge.files.delete(*paths)
    return f"Deleted: {list(paths)}"


@mcp.tool()
@with_session_refresh
async def ctera_edge_filer_upload_item(
    path: str, destination: str, ctx: Context
) -> str:
    edge = ctx.request_context.lifespan_context.session
    await edge.files.upload_file(path, destination)
    return f"Uploaded: {path} to: {destination}"


@mcp.tool()
@with_session_refresh
async def ctera_edge_filer_read_file(path: str, ctx: Context) -> str:
    edge = ctx.request_context.lifespan_context.session
    handle = await edge.files.handle(path)
    text_content = await handle.text()
    return text_content

from common import mcp, with_session_refresh
from mcp.server.fastmcp import Context


@mcp.tool()
@with_session_refresh
async def ctera_edge_list_dir(
    path: str, ctx: Context
) -> list[dict]:
    """
    List the contents of a specified directory on CTERA Edge Filer.
    
    Args:
        path (str): The path to the directory to list (e.g. 'cloud/users' or '/cloud/users').
        ctx: Request context
        
    Returns:
        list[dict]: A list of dictionaries containing file information.
    """
    edge = ctx.request_context.lifespan_context.session
    
    path = path.lstrip('/')
    
    files = await edge.files.listdir(path)

    return [{
        'name': f.name,
        'last_modified': f.modificationTime,
        'deleted': getattr(f, 'isDeleted', False),
        'is_dir': f.type == 'folder',
        'id': getattr(f, 'fileId', None),
        'type': f.type,
        'full_path': f.fullpath,
        'has_subfolders': getattr(f, 'hasSubfolders', None)
    } for f in files]

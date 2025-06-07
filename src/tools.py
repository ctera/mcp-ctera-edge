from common import mcp, with_session_refresh
from mcp.server.fastmcp import Context


@mcp.tool()
@with_session_refresh
async def ctera_edge_filer_who_am_i(ctx: Context) -> str:
    """
    Get the currently authenticated user information from the CTERA Edge Filer.
    
    Args:
        ctx: The MCP context containing the session information
        
    Returns:
        str: A formatted string showing the authenticated username
    """
    edge = ctx.request_context.lifespan_context.session
    session = await edge.api.get('/currentuser')
    username = session.username
    return f'Authenticated as {username}'


@mcp.tool()
@with_session_refresh
async def ctera_edge_filer_list_dir(path: str, ctx: Context) -> list[dict]:
    """
    List the contents of a directory on the CTERA Edge Filer.
    
    Args:
        path: The directory path to list
        ctx: The MCP context containing the session information
        
    Returns:
        list[dict]: A list of dictionaries containing file/folder 
                   information with keys: path, name, is_dir, is_file,
                   created_at, last_modified, size
    """
    edge = ctx.request_context.lifespan_context.session
    return await edge.files.listdir(path)


@mcp.tool()
@with_session_refresh
async def ctera_edge_filer_create_directory(path: str, ctx: Context) -> str:
    """
    Create a single directory on the CTERA Edge Filer.
    
    Args:
        path: The directory path to create
        ctx: The MCP context containing the session information
        
    Returns:
        str: Confirmation message indicating the directory was created
    """
    edge = ctx.request_context.lifespan_context.session
    await edge.files.mkdir(path)
    return f"Created: {path}"


@mcp.tool()
@with_session_refresh
async def ctera_edge_filer_makedirs(path: str, ctx: Context) -> str:
    """
    Create a directory and all necessary parent directories on the 
    CTERA Edge Filer.
    
    Args:
        path: The directory path to create (including parent 
              directories)
        ctx: The MCP context containing the session information
        
    Returns:
        str: Confirmation message indicating the directory structure 
             was created
    """
    edge = ctx.request_context.lifespan_context.session
    await edge.files.makedirs(path)
    return f"Created: {path}"


@mcp.tool()
@with_session_refresh
async def ctera_edge_filer_copy_item(
    source: str, 
    destination: str, 
    ctx: Context
) -> str:
    """
    Copy a file or directory from source to destination on the 
    CTERA Edge Filer.
    
    Args:
        source: The source path of the item to copy
        destination: The destination path where the item will be copied
        ctx: The MCP context containing the session information
        
    Returns:
        str: Confirmation message indicating the copy operation was 
             successful
    """
    edge = ctx.request_context.lifespan_context.session
    await edge.files.copy(source, destination)
    return f"Copied: {source} to: {destination}"


@mcp.tool()
@with_session_refresh
async def ctera_edge_filer_move_item(
    source: str, 
    destination: str, 
    ctx: Context
) -> str:
    """
    Move a file or directory from source to destination on the 
    CTERA Edge Filer.
    
    Args:
        source: The source path of the item to move
        destination: The destination path where the item will be moved
        ctx: The MCP context containing the session information
        
    Returns:
        str: Confirmation message indicating the move operation was 
             successful
    """
    edge = ctx.request_context.lifespan_context.session
    await edge.files.move(source, destination)
    return f"Moved: {source} to: {destination}"


@mcp.tool()
@with_session_refresh
async def ctera_edge_filer_delete_item(paths: list[str], ctx: Context) -> str:
    """
    Delete one or more files or directories on the CTERA Edge Filer.
    
    Args:
        paths: A list of file/directory paths to delete
        ctx: The MCP context containing the session information
        
    Returns:
        str: Confirmation message indicating the delete operation was 
             successful
    """
    edge = ctx.request_context.lifespan_context.session
    await edge.files.delete(*paths)
    return f"Deleted: {list(paths)}"


@mcp.tool()
@with_session_refresh
async def ctera_edge_upload_from_content(
    filepath: str, 
    content: str | bytes, 
    ctx: Context = None
) -> str:
    """
    Upload content directly to a file on the CTERA Edge Filer.
    
    Args:
        filepath: The destination file path on the Edge Filer
        content: The content to upload (string or bytes)
        ctx: The MCP context containing the session information
        
    Returns:
        str: Confirmation message indicating the upload was successful
    """
    edge = ctx.request_context.lifespan_context.session
    await edge.files.upload('', filepath, content)
    return f"Uploaded: {filepath}"


@mcp.tool()
@with_session_refresh
async def ctera_edge_filer_upload_file(
    path: str, 
    destination: str, 
    ctx: Context
) -> str:
    """
    Upload a local file to the CTERA Edge Filer.
    
    Args:
        path: The local file path to upload
        destination: The destination path on the Edge Filer
        ctx: The MCP context containing the session information
        
    Returns:
        str: Confirmation message indicating the upload was successful
    """
    edge = ctx.request_context.lifespan_context.session
    await edge.files.upload_file(path, destination)
    return f"Uploaded: {path} to: {destination}"


@mcp.tool()
@with_session_refresh
async def ctera_edge_filer_download_file(
    path: str, 
    destination: str, 
    ctx: Context = None
) -> str:
    """
    Download a file from the CTERA Edge Filer to a local destination.
    
    Args:
        path: The file path on the Edge Filer to download
        destination: The local destination path where the file will be saved
        ctx: The MCP context containing the session information
        
    Returns:
        str: Confirmation message indicating the download was 
             successful
    """
    edge = ctx.request_context.lifespan_context.session
    await edge.files.download(path, destination=destination)
    return f"Downloaded: {path} to: {destination}"


@mcp.tool()
@with_session_refresh
async def ctera_edge_filer_read_file(path: str, ctx: Context) -> str:
    """
    Read the contents of a text file from the CTERA Edge Filer.
    
    Args:
        path: The file path on the Edge Filer to read
        ctx: The MCP context containing the session information
        
    Returns:
        str: The text content of the file
    """
    edge = ctx.request_context.lifespan_context.session
    handle = await edge.files.handle(path)
    text_content = await handle.text()
    return text_content

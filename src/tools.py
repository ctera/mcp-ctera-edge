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


@mcp.tool()
@with_session_refresh
async def ctera_edge_create_directory(
    path: str, ctx: Context
) -> dict:
    """
    Create a new directory on CTERA Edge Filer.
    
    Args:
        path (str): The path of the directory to create (e.g. 'cloud/users/ron/MCP Demo/test1234').
        ctx: Request context
        
    Returns:
        dict: A dictionary containing the result of the directory creation.
    """
    edge = ctx.request_context.lifespan_context.session
    
    path = path.lstrip('/')
    
    try:
        await edge.files.mkdir(path)
        
        return {
            'success': True,
            'message': f'Directory created successfully: {path}',
            'path': path
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to create directory: {str(e)}',
            'path': path,
            'error': str(e)
        }


@mcp.tool()
@with_session_refresh
async def ctera_edge_copy_item(
    source_path: str, destination_directory: str, ctx: Context
) -> dict:
    """
    Copy a file or directory to a destination directory on CTERA Edge Filer.
    
    Args:
        source_path (str): The path of the source file/directory to copy (e.g. 'cloud/users/ron/MCP Demo/Service Delivery/weekly-report.txt').
        destination_directory (str): The destination directory where to copy the item (e.g. 'cloud/users/ron/MCP Demo/test').
        ctx: Request context
        
    Returns:
        dict: A dictionary containing the result of the copy operation.
    """
    edge = ctx.request_context.lifespan_context.session
    
    # Normalize paths - remove leading slash if present for CTERA API
    source_path = source_path.lstrip('/')
    destination_directory = destination_directory.lstrip('/')
    
    try:
        # Copy the file or directory into the destination directory
        # CTERA API copies the source INTO the destination directory
        await edge.files.copy(source_path, destination_directory)
        
        # Extract the source item name for the result message
        source_name = source_path.split('/')[-1]
        final_destination = f"{destination_directory}/{source_name}"
        
        return {
            'success': True,
            'message': f'Item copied successfully from {source_path} to {final_destination}',
            'source_path': source_path,
            'destination_directory': destination_directory,
            'final_destination': final_destination
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to copy item: {str(e)}',
            'source_path': source_path,
            'destination_directory': destination_directory,
            'error': str(e)
        }


@mcp.tool()
@with_session_refresh
async def ctera_edge_move_item(
    source_path: str, destination_directory: str, ctx: Context
) -> dict:
    """
    Move a file or directory to a destination directory on CTERA Edge Filer.
    
    Args:
        source_path (str): The path of the source file/directory to move (e.g. 'cloud/users/ron/MCP Demo/move_test_123').
        destination_directory (str): The destination directory where to move the item (e.g. 'cloud/users/ron/MCP Demo/test').
        ctx: Request context
        
    Returns:
        dict: A dictionary containing the result of the move operation.
    """
    edge = ctx.request_context.lifespan_context.session
    
    # Normalize paths - remove leading slash if present for CTERA API
    source_path = source_path.lstrip('/')
    destination_directory = destination_directory.lstrip('/')
    
    try:
        # Move the file or directory into the destination directory
        # CTERA API moves the source INTO the destination directory (like copy)
        await edge.files.move(source_path, destination_directory)
        
        # Extract the source item name for the result message
        source_name = source_path.split('/')[-1]
        final_destination = f"{destination_directory}/{source_name}"
        
        return {
            'success': True,
            'message': f'Item moved successfully from {source_path} to {final_destination}',
            'source_path': source_path,
            'destination_directory': destination_directory,
            'final_destination': final_destination
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to move item: {str(e)}',
            'source_path': source_path,
            'destination_directory': destination_directory,
            'error': str(e)
        }


@mcp.tool()
@with_session_refresh
async def ctera_edge_delete_item(
    path: str, ctx: Context
) -> dict:
    """
    Delete a file or directory on CTERA Edge Filer.
    
    Args:
        path (str): The path of the file/directory to delete (e.g. 'cloud/users/ron/MCP Demo/test/weekly-report.txt').
        ctx: Request context
        
    Returns:
        dict: A dictionary containing the result of the delete operation.
    """
    edge = ctx.request_context.lifespan_context.session
    
    # Normalize path - remove leading slash if present for CTERA API
    path = path.lstrip('/')
    
    try:
        # Delete the file or directory
        await edge.files.delete(path)
        
        return {
            'success': True,
            'message': f'Item deleted successfully: {path}',
            'path': path
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to delete item: {str(e)}',
            'path': path,
            'error': str(e)
        }


@mcp.tool()
@with_session_refresh
async def ctera_edge_upload_item(
    local_path: str, destination_directory: str, ctx: Context
) -> dict:
    """
    Upload a file from local path to a destination directory on CTERA Edge Filer.
    
    Args:
        local_path (str): The local file path to upload (e.g. 'Playground/av.py').
        destination_directory (str): The destination directory on CTERA Edge where to upload the file (e.g. 'cloud/users/ron/MCP Demo/test').
        ctx: Request context
        
    Returns:
        dict: A dictionary containing the result of the upload operation.
    """
    edge = ctx.request_context.lifespan_context.session
    
    # Normalize destination path - remove leading slash if present for CTERA API
    destination_directory = destination_directory.lstrip('/')
    
    try:
        # Upload the file to the destination directory
        await edge.files.upload_file(local_path, destination_directory)
        
        # Extract the filename from local path for the result message
        filename = local_path.split('/')[-1]  # Works for both Unix and Windows paths
        final_destination = f"{destination_directory}/{filename}"
        
        return {
            'success': True,
            'message': f'File uploaded successfully from {local_path} to {final_destination}',
            'local_path': local_path,
            'destination_directory': destination_directory,
            'final_destination': final_destination,
            'filename': filename
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to upload file: {str(e)}',
            'local_path': local_path,
            'destination_directory': destination_directory,
            'error': str(e)
        }


@mcp.tool()
@with_session_refresh
async def ctera_edge_download_item(
    remote_path: str, local_path: str, ctx: Context
) -> dict:
    """
    Download a file from CTERA Edge Filer to a local path.
    
    Args:
        remote_path (str): The path of the file on CTERA Edge to download (e.g. 'cloud/users/ron/MCP Demo/test/av.py').
        local_path (str): The local path where to save the downloaded file (e.g. 'Playground/av2.py').
        ctx: Request context
        
    Returns:
        dict: A dictionary containing the result of the download operation.
    """
    edge = ctx.request_context.lifespan_context.session
    
    # Normalize remote path - remove leading slash if present for CTERA API
    remote_path = remote_path.lstrip('/')
    
    try:
        # Download the file from CTERA Edge to local path
        await edge.files.download(remote_path, local_path)
        
        # Extract the filename from remote path for the result message
        filename = remote_path.split('/')[-1]
        
        return {
            'success': True,
            'message': f'File downloaded successfully from {remote_path} to {local_path}',
            'remote_path': remote_path,
            'local_path': local_path,
            'filename': filename
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to download file: {str(e)}',
            'remote_path': remote_path,
            'local_path': local_path,
            'error': str(e)
        }

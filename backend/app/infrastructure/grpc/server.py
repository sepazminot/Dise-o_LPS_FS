"""
gRPC server setup and lifecycle management.
"""
import asyncio
import grpc
from concurrent import futures
import structlog

from app.infrastructure.config.settings import get_settings

logger = structlog.get_logger(__name__)
settings = get_settings()


async def start_grpc_server() -> asyncio.Task:
    """Start gRPC server in background task."""
    server = grpc.aio.server(
        futures.ThreadPoolExecutor(max_workers=10),
        options=[
            ("grpc.max_send_message_length", 50 * 1024 * 1024),
            ("grpc.max_receive_message_length", 50 * 1024 * 1024),
        ],
    )
    
    # Add services here once implemented
    # from app.interfaces.grpc.auth_service import AuthServiceServicer
    # from generated.auth.v1 import auth_pb2_grpc
    # auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthServiceServicer(), server)
    
    listen_addr = f"{settings.GRPC_HOST}:{settings.GRPC_PORT}"
    server.add_insecure_port(listen_addr)
    
    await server.start()
    logger.info("grpc_server_started", address=listen_addr)
    
    # Return task that waits for termination
    async def wait_for_termination():
        await server.wait_for_termination()
    
    task = asyncio.create_task(wait_for_termination())
    return task


async def stop_grpc_server(task: asyncio.Task) -> None:
    """Stop gRPC server gracefully."""
    if task and not task.done():
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
    logger.info("grpc_server_stopped")
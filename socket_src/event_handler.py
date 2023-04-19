import asyncio

from socket_src.socket_consumer import socket_consumer, send_consumer_message
from socket_src.log_manager import socket_logger

async def consume():
    asyncio.create_task(send_consumer_message())

async def startup_event_app():
    await socket_consumer()
    await consume()

def shutdown_event_app():
    socket_logger.info("shutdown socket app")
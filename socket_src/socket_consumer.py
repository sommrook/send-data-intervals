import asyncio
import os
import aiokafka
import json

from socket_src.settings import CONSUMER_SOCKET_GROUP, KAFKA_SOCKET_TOPIC, KAFKA_BOOTSTRAP
from socket_src.log_manager import socket_logger
# from socket_src.socket_handler import sio, progress_namespace


async def socket_consumer():
    loop = asyncio.get_event_loop()
    global consumer
    consumer_group = f"{CONSUMER_SOCKET_GROUP}_{os.getpid()}"
    consumer = aiokafka.AIOKafkaConsumer(KAFKA_SOCKET_TOPIC, loop=loop, bootstrap_servers=KAFKA_BOOTSTRAP, group_id=consumer_group)
    socket_logger.info(f"consumer group start {consumer_group} | {KAFKA_SOCKET_TOPIC}")
    await consumer.start()

def success():
    socket_logger.info("success test")

async def send_consumer_message():
    socket_logger.info(f"send consumer message start")
    try:
        async for msg in consumer:
            value = json.loads(msg.value)
            await consumer.commit()
    finally:
        socket_logger.warning("Stopping consumer")
        await consumer.stop()

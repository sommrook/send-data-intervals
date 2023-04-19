import socketio
from socket_src.log_manager import socket_logger
from socket_src.settings import PROGRESS_CHECK

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')

progress_namespace = "/training-progress"

def training_socket_handler():
    @sio.event(namespace=progress_namespace)
    async def connect(sid, environ):
        socket_logger.info(f"socket connect - {sid}")

    @sio.event(namespace=progress_namespace)
    async def disconnect(sid):
        socket_logger.info(f"socket disconnect - {sid}")

    @sio.on("progress", namespace=progress_namespace)
    async def progress_check(sid, data):
        socket_logger.info(f"data is {data}")
        count = 1
        while True:
            await sio.emit(event="progress-check", data=count, to=sid, namespace=progress_namespace, callback=None)
            count += 1
            # sio.sleep을 써야지만 disconnection을 제대로 잡아낼 수 있음
            # 일반적인 time.sleep함수로 했을 때 브라우저를 닫아서 disconnect가 되어야함에도 불구하고 disconnect가 제대로 되지 않는 이슈가 있었음
            # disconnect가 되어도 sleep시간동안 while문을 돌고 emit을 하려고 하기 때문이다.
            await sio.sleep(PROGRESS_CHECK)

    @sio.on("callback", namespace=progress_namespace)
    async def callback_check(sid, data):
        # 한 sid socket connection에 대해 progress_check함수로 무한루프를 돌아도 다른 event를 받을 수 있음
        socket_logger.info(f"callback data is {data}")
        await sio.emit(event="callback-success", data="success", to=sid, namespace=progress_namespace, callback=None)

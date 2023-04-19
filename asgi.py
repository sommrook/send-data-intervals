import uvicorn
from socket_src.settings import API_HOST, API_PORT, API_WORKERS


if __name__ == "__main__":
    uvicorn.run(
        "socket_src.app:socket_app",
        host=API_HOST,
        port=API_PORT,
        workers=API_WORKERS
    )
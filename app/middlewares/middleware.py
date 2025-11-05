import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)  # обязательно передаём app

    async def dispatch(self, request: Request, call_next):
        # Записываем время начала обработки запроса
        start_time = time.time()

        # Выполнение запроса
        response = await call_next(request)

        # Время обработки запроса в миллисекундах
        process_time = (time.time() - start_time) * 1000
        print(f"{request.method} {request.url.path} - {process_time:.2f} ms")

        # Добавляем в заголовок ответа время обработки
        response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
        return response
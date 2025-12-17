import logging
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Dict, Any, Awaitable, Callable

logger = logging.getLogger(__name__)

class LoggingInfoMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        
        if isinstance(event, Message) and event.from_user:
            user_id = event.from_user.id
            logger.info(f"User {user_id} отправил сообщение: {event.text}")
        elif isinstance(event, CallbackQuery) and event.from_user:
            user_id = event.from_user.id
            logger.info(f"User {user_id} нажал кнопку: {event.data}")

        return await handler(event, data)
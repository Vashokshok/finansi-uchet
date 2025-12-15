import logging
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Dict, Any, Awaitable, Callable

class LoggingfInfoMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[Any, str]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[Any, str]
                    ) -> Any:

        result = await handler(event, data)
        return result
        
    

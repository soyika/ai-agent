import asyncio
from typing import Callable, Optional, Any
from loguru import logger


class EventBus:
    def __init__(self):
        self._subscribers: dict[str, list[Callable]] = {}
        self._history: list[dict[str, Any]] = []
        self._max_history = 1000

    def subscribe(self, event_type: str, handler: Callable):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)
        logger.info(f"订阅事件: {event_type}")

    def unsubscribe(self, event_type: str, handler: Callable):
        if event_type in self._subscribers:
            self._subscribers[event_type].remove(handler)

    async def publish(self, event_type: str, data: dict[str, Any]):
        event = {"type": event_type, "data": data}
        self._history.append(event)
        if len(self._history) > self._max_history:
            self._history = self._history[-self._max_history:]

        logger.info(f"发布事件: {event_type}")

        tasks = []
        if event_type in self._subscribers:
            for handler in self._subscribers[event_type]:
                try:
                    result = handler(data)
                    if asyncio.iscoroutine(result):
                        tasks.append(asyncio.create_task(result))
                except Exception as e:
                    logger.error(f"事件处理器执行失败: {e}")

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    def get_history(self, event_type: Optional[str] = None) -> list[dict]:
        if event_type:
            return [e for e in self._history if e["type"] == event_type]
        return self._history


# 全局事件总线实例
event_bus = EventBus()

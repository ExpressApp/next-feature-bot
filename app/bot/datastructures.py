"""Datastructures to help testing."""

from typing import Dict, Set
from uuid import UUID


class CTSEventsListeners:
    def __init__(self) -> None:
        self._chats: Dict[str, Set[UUID]] = {}

    def add(self, host: str, chat_id: UUID) -> None:
        self._chats.setdefault(host, set()).add(chat_id)

    def remove(self, host: str, chat_id: UUID) -> None:
        self._chats[host].remove(chat_id)

    def get(self, host: str) -> Set[UUID]:
        return self._chats.get(host, set())


class DebugSubscribers:
    def __init__(self) -> None:
        self._subscribers: Dict[UUID, Set[UUID]] = {}

    def toggle(self, subscriber_id: UUID, chat_id: UUID) -> bool:
        if chat_id not in self._subscribers:
            self._subscribers[chat_id] = {subscriber_id}
            return True

        if subscriber_id not in self._subscribers[chat_id]:
            self._subscribers[chat_id].add(subscriber_id)
            return True

        self._subscribers[chat_id].remove(subscriber_id)
        return False

    def get_subscribers_by_chat(self, chat_id: UUID) -> Set[UUID]:
        if chat_id not in self._subscribers:
            return set()

        return self._subscribers[chat_id].copy()

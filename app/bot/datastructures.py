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

    def add(self, subscriber_id: UUID, chat_id: UUID) -> None:
        self._subscribers.setdefault(chat_id, set()).add(subscriber_id)

    def remove(self, subscriber_id: UUID, chat_id: UUID) -> None:
        self._subscribers.setdefault(chat_id, set()).discard(subscriber_id)

    def get(self, chat_id: UUID) -> Set[UUID]:
        return self._subscribers.setdefault(chat_id, set()).copy()

    def toggle(self, subscriber_id: UUID, chat_id: UUID) -> bool:
        if subscriber_id in self._subscribers.setdefault(chat_id, set()):
            self.remove(subscriber_id, chat_id)
            return False

        self.add(subscriber_id, chat_id)
        return True

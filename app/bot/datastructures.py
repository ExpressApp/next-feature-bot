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

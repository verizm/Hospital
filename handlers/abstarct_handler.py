from __future__ import annotations
from abc import (
    ABC,
    abstractmethod,
)
from typing import Optional
from dto.patient import PatientDto


class Handler(ABC):

    @abstractmethod
    def set_next(self, handler: Handler) -> Handler:
        pass

    @abstractmethod
    def handle(self, command: str, patient: PatientDto) -> Optional[str]:
        pass


class AbstractHandler(Handler):
    _next_handler: Handler = None

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, command: str, patient: PatientDto) -> PatientDto | None:
        if self._next_handler:
            return self._next_handler.handle(command, patient)

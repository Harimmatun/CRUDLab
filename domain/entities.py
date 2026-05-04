from dataclasses import dataclass
from typing import Optional
from domain.errors import DomainError
from domain.value_objects import Email

@dataclass
class User:
    _id: Optional[int]
    _email: Email
    _hashed_password: str

    @property
    def id(self) -> Optional[int]:
        return self._id

    @property
    def email(self) -> Email:
        return self._email

    @property
    def hashed_password(self) -> str:
        return self._hashed_password

@dataclass
class Task:
    _id: Optional[int]
    _title: str
    _description: str
    _assignee_id: int
    _status: str = "TODO"

    @property
    def id(self) -> Optional[int]:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str:
        return self._description

    @property
    def assignee_id(self) -> int:
        return self._assignee_id

    @property
    def status(self) -> str:
        return self._status

    def mark_as_in_progress(self) -> None:
        if self._status == "DONE":
            raise DomainError("Cannot move task from DONE to IN_PROGRESS directly")
        self._status = "IN_PROGRESS"

    def mark_as_done(self) -> None:
        if not self._assignee_id:
            raise DomainError("Cannot mark task as DONE without an assignee")
        self._status = "DONE"
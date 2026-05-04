from dataclasses import dataclass
from domain.errors import DomainError

@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        if "@" not in self.value or "." not in self.value.split("@")[-1]:
            raise DomainError(f"Invalid email: {self.value}")
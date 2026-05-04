from domain.entities import User, Task
from domain.value_objects import Email
from domain.repositories import UserRepository
from domain.errors import DomainError

class UserFactory:
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    def create(self, email_str: str, hashed_password: str) -> User:
        email = Email(email_str)
        if self._user_repo.find_by_email(email):
            raise DomainError("User with this email already exists")
        return User(_id=None, _email=email, _hashed_password=hashed_password)

class TaskFactory:
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    def create(self, title: str, description: str, assignee_id: int) -> Task:
        if not title.strip():
            raise DomainError("Task title cannot be empty")
        if not self._user_repo.find_by_id(assignee_id):
            raise DomainError(f"Assignee with id {assignee_id} does not exist")
        return Task(_id=None, _title=title, _description=description, _assignee_id=assignee_id)
from domain.entities import User, Task
from domain.value_objects import Email
from infrastructure.orm_models import UserEntity, TaskEntity

class UserMapper:
    @staticmethod
    def to_domain(entity: UserEntity) -> User:
        return User(
            _id=entity.id,
            _email=Email(entity.email),
            _hashed_password=entity.hashed_password
        )

    @staticmethod
    def to_entity(user: User) -> UserEntity:
        return UserEntity(
            id=user.id,
            email=user.email.value,
            hashed_password=user.hashed_password
        )

class TaskMapper:
    @staticmethod
    def to_domain(entity: TaskEntity) -> Task:
        return Task(
            _id=entity.id,
            _title=entity.title,
            _description=entity.description,
            _assignee_id=entity.assignee_id,
            _status=entity.status
        )

    @staticmethod
    def to_entity(task: Task) -> TaskEntity:
        return TaskEntity(
            id=task.id,
            title=task.title,
            description=task.description,
            assignee_id=task.assignee_id,
            status=task.status
        )
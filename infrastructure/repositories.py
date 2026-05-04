from typing import Optional, List
from sqlalchemy.orm import Session
from domain.entities import User, Task
from domain.value_objects import Email
from domain.repositories import UserRepository, TaskRepository
from infrastructure.orm_models import UserEntity, TaskEntity
from infrastructure.mappers import UserMapper, TaskMapper

class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session):
        self._session = session

    def save(self, user: User) -> None:
        entity = UserMapper.to_entity(user)
        if entity.id is None:
            self._session.add(entity)
            self._session.flush()
            user._id = entity.id
        else:
            self._session.merge(entity)
        self._session.commit()

    def find_by_email(self, email: Email) -> Optional[User]:
        entity = self._session.query(UserEntity).filter(UserEntity.email == email.value).first()
        if entity:
            return UserMapper.to_domain(entity)
        return None

    def find_by_id(self, user_id: int) -> Optional[User]:
        entity = self._session.query(UserEntity).filter(UserEntity.id == user_id).first()
        if entity:
            return UserMapper.to_domain(entity)
        return None

class SqlAlchemyTaskRepository(TaskRepository):
    def __init__(self, session: Session):
        self._session = session

    def save(self, task: Task) -> None:
        entity = TaskMapper.to_entity(task)
        if entity.id is None:
            self._session.add(entity)
            self._session.flush()
            task._id = entity.id
        else:
            self._session.merge(entity)
        self._session.commit()

    def find_by_id(self, task_id: int) -> Optional[Task]:
        entity = self._session.query(TaskEntity).filter(TaskEntity.id == task_id).first()
        if entity:
            return TaskMapper.to_domain(entity)
        return None

    def get_all(self) -> List[Task]:
        entities = self._session.query(TaskEntity).all()
        return [TaskMapper.to_domain(entity) for entity in entities]
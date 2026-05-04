from sqlalchemy import Column, Integer, String, ForeignKey
from infrastructure.database import Base

class UserEntity(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class TaskEntity(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    assignee_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String)
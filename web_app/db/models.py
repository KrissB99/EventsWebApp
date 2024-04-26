import datetime
from flask import session
from sqlalchemy import DateTime, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

from web_app.main import db

class DBManager:
    
    @classmethod
    def get_all(cls) -> list[db.Model]:
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id: int) -> db.Model:
        return cls.query.filter(cls.id == id).first()

    def add(self) -> db.Model:
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
        
    @classmethod
    def add_all(cls, db_objects: list[db.Model]) -> None:
        db.session.add_all(db_objects)
        db.session.commit()

    def update(self, attr: dict) -> None:
        for name, value in attr.items():
            setattr(self, name, value)
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def create(cls, form: dict) -> object:
        for date in ['date_from', 'date_to']:
            form[date] = datetime.strptime(form[date], "%Y-%m-%d")
        event = cls(**form).add()
        return event

    def get_attrs(self):
        return ', '.join(f'{key}: {getattr(self, key)!r}' for key in self.__table__.columns.keys())


class Users(db.Model, DBManager):
    
    __tablename__ = 'users'
    __allow_unmapped__ = True
    
    # Columns
    id: Mapped[int] = mapped_column(primary_key=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    is_vege: Mapped[bool] = mapped_column(Boolean, nullable=True)
    password_hash: Mapped[str] = mapped_column(String(512), nullable=False)
    salt: Mapped[str] = mapped_column(String(20), nullable=False)
    
    # Relationships
    events  = relationship(
        'UsersOnEvents', 
        back_populates='user',  
        cascade="all, delete-orphan",
        lazy="subquery",
    )
    hosted_events = relationship(
        'Events', 
        back_populates='author',
        cascade="all, delete-orphan",
        lazy="subquery",
    ) 
    
    @classmethod
    def exists(cls, email: str) -> bool:
        return cls.query.filter(cls.email == email).first()
        
    def to_dict(self):
        return {
            'id': self.id, 
            'is_admin': self.is_admin, 
            'email': self.email, 
            'is_vege': self.is_vege,
        }
    
    def __repr__(self):
        return f'User({self.get_attrs()})'
    
    
class Events(db.Model, DBManager):
    
    __tablename__ = 'events'
    __allow_unmapped__ = True
    
    # Columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    date_from: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    date_to: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Foreign Keys
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    
    # Relationships
    author: Mapped['User'] = relationship(
        'Users', 
        foreign_keys='Events.author_id',
        lazy="subquery"
    )
    attendee_list: Mapped[list['Users']] =  relationship(
        'UsersOnEvents', 
        lazy='subquery'
    )
    
    def to_dict(self) -> dict:
        return {
            'id': self.id, 
            'name': self.name,
            'date_from': self.date_from, 
            'date_to': self.date_to, 
            'author': self.author.to_dict() if self.author else None, 
            'atendee_list': [element.to_dict() for element in self.attendee_list]
        }
    
    def __repr__(self):
        return f'Events({self.get_attrs()})'


class UsersOnEvents(db.Model, DBManager):
    
    __tablename__ = 'users_on_events'
    __allow_unmapped__ = True
    
    # Columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date_from: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    date_to: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    breakfast: Mapped[bool] = mapped_column(Boolean, default=False)
    lunch: Mapped[bool] = mapped_column(Boolean, default=False)
    dinner: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Foreign Keys
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey('events.id'))
    
    # Relations
    user: Mapped['Users'] = relationship('Users', lazy="subquery")
    
    def to_dict(self) -> dict: 
        return {
            'id': self.id, 
            'date_from': self.date_from, 
            'date_to': self.date_to,
            'breakfast': self.breakfast, 
            'lunch': self.lunch, 
            'dinner': self.dinner,
            'user': self.user.to_dict() if self.user else None, 
        }
        
    def __repr__(self) -> str:
        return f'UsersOnEvents({self.get_attrs()})'
    
    
class Logs(db.Model, DBManager):
    
    __tablename__ = 'logs'
    __allow_unmapped__ = True
    
    # Columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=True)
    endpoint: Mapped[str] = mapped_column(String, nullable=True)
    status_code: Mapped[int] = mapped_column(Integer, nullable=False)
    time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    
    @classmethod
    def new(cls, endpoint: str, status_code: int) -> None:
        cls(user_id=session['user_id'] if session else None, 
            endpoint=endpoint, 
            status_code=status_code).add()
    
    def to_dict(self) -> dict: 
        return {
            'id': self.id, 
            'user_id': self.user_id,
            'action': self.action,
            'time': self.datetime
        }
        
    def __repr__(self) -> str:
        return f'Logs({self.get_attrs()})'
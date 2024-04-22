import datetime
from flask import session
from sqlalchemy import DateTime, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from web_app.const_vars import PEPPER
from web_app.main import db

class DBManager:
    """CRUD class"""
    
    session = db.session
    
    @classmethod
    def get_all(cls) -> list[db.Model]:
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls, id: int) -> db.Model:
        return cls.query.filter(cls.id == id).first()
    
    def add(self) -> db.Model:
        session.add(self)
        session.commit()
        return self
    
    @classmethod
    def add_all(cls, db_objects: list[db.Model]) -> None:
        session.add_all(db_objects)
        session.commit()
        
    def update(self, attr: dict) -> None:
        for name, value in attr.items():
            setattr(self, name, value)
        session.commit()
        
    def delete(self) -> None:
        session.delete(self)
        session.commit()
        
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
    events: object  = relationship(
        'UsersOnEvents', back_populates='user',  cascade="all, delete-orphan"
    )
    hosted_events = relationship('Events', back_populates='author_id') 
    
    @classmethod
    def exists(cls, email: str) -> bool:
        return cls.query.filter(cls.email == email).first()
        
    def to_dict(self):
        return {
            'id': self.id, 
            'admin': self.is_admin, 
            'email': self.email, 
            'is_vege': self.is_vege,
            'evets': [event.to_dict() for event in self.events],
            'hosted_events': [event.to_dict() for event in self.hosted_events]
        }
    
    def __repr__(self):
        return f'User({self.get_attrs()})'
    
    
class Events(db.Model, DBManager):
    
    __tablename__ = 'events'
    __allow_unmapped__ = True
    
    # Columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date_from: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    date_to: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    
    # Foreign Keys
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    
    # Relationships
    author: Mapped['User'] = relationship('Users', back_populates='events')
    attendee_list: Mapped[list] =  relationship(
        'UsersOnEvents', back_populates='event',  cascade="all, delete-orphan"
    )
    
    def to_dict(self) -> dict:
        return {
            'id': self.id, 
            'date_from': self.date_from, 
            'date_to': self.date_to, 
            'author': self.author.to_dict() if self.author else None, 
            'atendee_list': [user.to_dict() for user in self.attendee_list]
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
    user: Mapped['Users'] = relationship('Users', back_populates='events')
    event: Mapped['Events'] = relationship('Events', back_populates='attendee_list')
    
    def to_dict(self) -> dict: 
        return {
            'id': self.id, 
            'date_from': self.date_from, 
            'date_to': self.date_to,
            'meals': {
                'breakfast': self.breakfast, 
                'lunch': self.lunch, 
                'dinner': self.dinner
            }, 
            'user': self.user.to_dict() if self.user else None, 
            'event': self.event.to_dict() if self.event else None
        }
        
    def __repr__(self) -> str:
        return f'UsersOnEvents({self.get_attrs()})'
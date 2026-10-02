from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    notes = relationship("Note", back_populates="owner")
    comments = relationship("Comment", back_populates="author")

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="notes")
    comments = relationship("Comment", back_populates="note", cascade="all, delete-orphan")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(500), nullable=False)
    note_id = Column(Integer, ForeignKey("notes.id"))
    author_id = Column(Integer, ForeignKey("users.id"))

    note = relationship("Note", back_populates="comments")
    author = relationship("User", back_populates="comments")
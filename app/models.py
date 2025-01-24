from .database import Base
from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, text

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Integer, server_default='TRUE', nullable=False)  # Use Integer with default=1 for compatibility
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('CURRENT_TIMESTAMP'))  # Corrected the default function to use CURRENT_TIMESTAMP
    
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), 
        nullable=False, 
        server_default=text("(datetime('now', 'localtime'))")  # Ensure SQLite uses local time
    )


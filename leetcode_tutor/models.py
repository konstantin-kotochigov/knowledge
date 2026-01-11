"""
Database models for LeetCode tutor application
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class Problem(Base):
    """Model for storing LeetCode problems"""
    __tablename__ = 'problems'
    
    id = Column(Integer, primary_key=True)
    leetcode_id = Column(Integer, unique=True, nullable=False)
    title = Column(String(500), nullable=False)
    difficulty = Column(String(50))
    description = Column(Text, nullable=False)
    hint = Column(Text)
    solution = Column(Text)
    has_solution = Column(Boolean, default=False)
    has_hint = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Problem {self.leetcode_id}: {self.title}>"


class DailyProblem(Base):
    """Model for tracking daily problems shown to user"""
    __tablename__ = 'daily_problems'
    
    id = Column(Integer, primary_key=True)
    problem_id = Column(Integer, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<DailyProblem {self.problem_id} on {self.date}>"


class RateLimit(Base):
    """Model for tracking rate limits"""
    __tablename__ = 'rate_limits'
    
    id = Column(Integer, primary_key=True)
    service = Column(String(50), unique=True, nullable=False)  # 'leetcode_parser' or 'llm_generator'
    count = Column(Integer, default=0)
    last_reset = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<RateLimit {self.service}: {self.count}>"


# Database setup
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///leetcode.db')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        return db
    except Exception:
        db.close()
        raise

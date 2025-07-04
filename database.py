import os
from sqlalchemy import create_engine, Column, String, DateTime, Integer, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import uuid

# Database configuration - using SQLite (override any PostgreSQL env vars)
DATABASE_URL = 'sqlite:///./data/approval_workflow.db'
print(f"Using SQLite database: {DATABASE_URL}")
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Submission(Base):
    __tablename__ = "submissions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    purpose = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    data_approval = Column(String, default='Pending')
    security_approval = Column(String, default='Pending')
    legal_approval = Column(String, default='Pending')
    overall_status = Column(String, default='Pending')

def init_db():
    """Initialize the database tables"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def add_submission_to_db(name, description, purpose):
    """Add a new submission to the database"""
    db = SessionLocal()
    try:
        submission = Submission(
            name=name,
            description=description,
            purpose=purpose
        )
        db.add(submission)
        db.commit()
        db.refresh(submission)
        return submission
    finally:
        db.close()

def get_all_submissions():
    """Get all submissions from database"""
    db = SessionLocal()
    try:
        submissions = db.query(Submission).order_by(Submission.timestamp.desc()).all()
        return submissions
    finally:
        db.close()

def update_approval_in_db(submission_id, team, status):
    """Update approval status for a specific team"""
    db = SessionLocal()
    try:
        submission = db.query(Submission).filter(Submission.id == submission_id).first()
        if submission:
            if team == 'Data':
                setattr(submission, 'data_approval', status)
            elif team == 'Security':
                setattr(submission, 'security_approval', status)
            elif team == 'Legal':
                setattr(submission, 'legal_approval', status)
            
            # Update overall status
            overall_status = calculate_overall_status_db(submission)
            setattr(submission, 'overall_status', overall_status)
            db.commit()
            return submission
        return None
    finally:
        db.close()

def calculate_overall_status_db(submission):
    """Calculate overall status based on team approvals"""
    approvals = [
        submission.data_approval,
        submission.security_approval,
        submission.legal_approval
    ]
    
    if 'Rejected' in approvals:
        return 'Rejected'
    elif all(approval == 'Approved' for approval in approvals):
        return 'Fully Approved'
    else:
        return 'Pending'

def get_pending_submissions_for_team(team):
    """Get submissions that need approval from a specific team"""
    db = SessionLocal()
    try:
        if team == 'Data':
            submissions = db.query(Submission).filter(Submission.data_approval == 'Pending').all()
        elif team == 'Security':
            submissions = db.query(Submission).filter(Submission.security_approval == 'Pending').all()
        elif team == 'Legal':
            submissions = db.query(Submission).filter(Submission.legal_approval == 'Pending').all()
        else:
            submissions = []
        return submissions
    finally:
        db.close()

def clear_all_data():
    """Clear all submissions from database"""
    db = SessionLocal()
    try:
        db.query(Submission).delete()
        db.commit()
        return True
    finally:
        db.close()
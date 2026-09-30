from sqlalchemy import Column, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from app.database import Base
import uuid


class ScanHistory(Base):
    __tablename__ = "scan_history"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    scan_type = Column(String, nullable=False)
    target = Column(String, nullable=False)
    result = Column(String, nullable=False)
    score = Column(Float, default=0.0)
    details = Column(Text, default="{}")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Alert(Base):
    __tablename__ = "alerts"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, default="")
    severity = Column(String, default="info")
    source = Column(String, default="system")
    acknowledged = Column(String, default="false")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class WebsiteVisit(Base):
    __tablename__ = "website_visits"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    url = Column(String, nullable=False)
    domain = Column(String, default="")
    result = Column(String, default="safe")
    score = Column(Float, default=0.0)
    browser = Column(String, default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class EmailAnalysis(Base):
    __tablename__ = "email_analyses"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    subject = Column(String, default="")
    sender = Column(String, default="")
    body_preview = Column(Text, default="")
    result = Column(String, default="safe")
    score = Column(Float, default=0.0)
    indicators = Column(Text, default="[]")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

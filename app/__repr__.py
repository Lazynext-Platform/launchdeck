from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
from enum import Enum as PyEnum

class SubscriptionStatus(PyEnum):
    active = "active"
    inactive = "inactive"

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    plan_id = Column(String, nullable=False)
    status = Column(Enum(SubscriptionStatus), default=SubscriptionStatus.active)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"Subscription(id={self.id}, user_id={self.user_id}, plan_id={self.plan_id}, status={self.status})"
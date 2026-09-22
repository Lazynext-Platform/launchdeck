from fastapi import APIRouter, Depends, HTTPException
from app.services.stripe_service import create_customer, create_subscription, update_subscription, cancel_subscription
from app.schemas.subscription import SubscriptionCreate, SubscriptionUpdate
from app.models.subscription import Subscription
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/subscriptions/")
def create_subscription_endpoint(subscription: SubscriptionCreate, db: Session = Depends(get_db)):
    customer_id = create_customer(1)  # Replace with actual user ID
    subscription_id = create_subscription(customer_id, subscription.plan_id)
    db_subscription = Subscription(user_id=1, plan_id=subscription.plan_id, status="active")  # Replace with actual user ID
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription

@router.put("/subscriptions/{subscription_id}")
def update_subscription_endpoint(subscription_id: int, subscription: SubscriptionUpdate, db: Session = Depends(get_db)):
    db_subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not db_subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    if subscription.plan_id:
        update_subscription(db_subscription.plan_id, subscription.plan_id)
        db_subscription.plan_id = subscription.plan_id
    if subscription.status:
        db_subscription.status = subscription.status
    db.commit()
    db.refresh(db_subscription)
    return db_subscription

@router.delete("/subscriptions/{subscription_id}")
def cancel_subscription_endpoint(subscription_id: int, db: Session = Depends(get_db)):
    db_subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not db_subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    cancel_subscription(db_subscription.plan_id)
    db_subscription.status = "inactive"
    db.commit()
    db.refresh(db_subscription)
    return db_subscription
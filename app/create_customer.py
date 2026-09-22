import stripe
from app.config import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_customer(user_id: int) -> str:
    customer = stripe.Customer.create(
        email=f"user_{user_id}@example.com",
        description=f"Customer for user {user_id}"
    )
    return customer.id

def create_subscription(customer_id: str, plan_id: str) -> str:
    subscription = stripe.Subscription.create(
        customer=customer_id,
        items=[{"price": plan_id}],
        payment_settings={"payment_method_types": ["card"]},
        expand=["latest_invoice.payment_intent"]
    )
    return subscription.id

def update_subscription(subscription_id: str, plan_id: str) -> None:
    stripe.Subscription.modify(
        subscription_id,
        items=[{"price": plan_id}]
    )

def cancel_subscription(subscription_id: str) -> None:
    stripe.Subscription.delete(subscription_id)
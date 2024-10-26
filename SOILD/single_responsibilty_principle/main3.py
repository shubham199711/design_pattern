# Design an Order Processing System for an e-commerce application. The system should:

# Represent an Order that has a list of items and a total price.
# Handle payment processing, which involves charging the customer’s payment method.
# Send a confirmation email to the customer once the order is successful.
from typing import List
from abc import ABC, abstractmethod

class Items:
    def __init__(self, name: str, price: int):
        self.name = name
        self.price = price

class Order:
    def __init__(self, items: List[Items]):
        self.items =  items
        self.total_price = sum([x.price for x in self.items])

class Email:
    def send_mail_order_confirmation(self, to: str):
        # main mail logic
        print(f"Confirmation email sent to {to}")
        return

class Payment(ABC):
    @abstractmethod
    def payment(self, from_user: str, to_user, price: int):
        raise NotImplementedError

class PaymentByStrip(Payment):
    def payment(self, from_user: str, to_user, price: int):
        print(f"Stripe payment of {price} from {from_user} to {to_user}")
        return

class PaymentByPayPal(Payment):
    def payment(self, from_user: str, to_user, price: int):
        print(f"PayPal payment of {price} from {from_user} to {to_user}")
        return

class PaymentProcessing:
    INTERNAL_ACCOUNT = "<our_user>"

    def __init__(self, order: Order, method: Payment):
        self.order = order
        self.payment_method = method
    
    def change_method(self, method: Payment):
        self.payment_method = method
    
    def process_payment(self, from_user: str):
        self.payment_method.payment(from_user=from_user, to_user=self.INTERNAL_ACCOUNT, price=self.order.total_price)

class OrderConfirmation:
    def __init__(self, email_service: Email):
        self.email_service = email_service

    def send_confirmation(self, to: str):
        self.email_service.send_order_confirmation(to)
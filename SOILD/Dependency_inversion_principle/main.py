# Payment Processing System
from abc import ABC, abstractmethod

class PaymentType(ABC):
    @abstractmethod
    def payment(self):
        """Method to make payment"""

class CreditCard(PaymentType):
    def payment(self):
        print("Make payment using CreditCard") 


class PayPal(PaymentType):
    def payment(self):
        print("Make payment using PayPal") 
    
class Bitcoin(PaymentType):
    def payment(self):
        print("Make payment using Bitcoin") 


class PaymentManager:
    def __init__(self, payment_method: PaymentType):
        self.payment = payment_method
    
    def make_payment(self):
        self.payment.payment()
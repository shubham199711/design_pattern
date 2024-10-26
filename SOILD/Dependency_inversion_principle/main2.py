# Let's try applying the Dependency Inversion Principle (DIP) to a Messaging System.
# This system should be capable of sending messages through various channels, such as Email,
# SMS, or Push Notification

from abc import ABC, abstractmethod

class MessageType(ABC):
    @abstractmethod
    def send(self):
        """method to send message"""
        pass

class Email(MessageType):
    def send(self):
        print("Send message using Email")

class SMS(MessageType):
    def send(self):
        print("Send message using SMS")

class PushNotification(MessageType):
    def send(self):
        print("Send message using PushNotification")


class NotificationManager:
    def __init__(self, message_service: MessageType):
        self.message_type = message_service
    
    def send_notification(self):
        self.message_type.send()
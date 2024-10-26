# Your task is to design a Notification System for a platform that sends out notifications to users. The system should:

# Support different notification channels (e.g., email, SMS).
# Allow adding new notification channels (e.g., push notifications) without modifying existing code

from abc import ABC, abstractmethod
from typing import List

class Notify(ABC):
    def __init__(self, sending_to):
        self.sending_to = sending_to
        
    @abstractmethod
    def send_notification(self):
        raise NotImplementedError

class EmailNotify(Notify):
    def __init__(self, sending_to):
        super().__init__(sending_to)

    def send_notification(self):
        print(f"Send Email to email: {self.sending_to}")

class SMSNotify(Notify):
    def __init__(self, sending_to):
        super().__init__(sending_to)

    def send_notification(self):
        print(f"Send SMS to number: {self.sending_to}")

class NotificationSystem:
    def __init__(self):
        self.channels: List[Notify] = []
    
    def add_channel(self, new_channel: Notify):
        self.channels.append(new_channel)
    
    def send_notifications(self,):
        for channel in self.channels:
            channel.send_notification()

# Usage example:
notifier = NotificationSystem()
notifier.add_channel(EmailNotify(sending_to="user@example.com"))
notifier.add_channel(SMSNotify(sending_to="3048230498"))
notifier.send_notifications()
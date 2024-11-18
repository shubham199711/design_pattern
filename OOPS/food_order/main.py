# Design a Food Delivery System
# Problem Statement:
# Design a food delivery system like Swiggy or UberEats with the following requirements:

# Users: Users can search for restaurants, browse menus, place orders, and track their order status.
# Restaurants: Each restaurant has a menu, which includes multiple dishes. They should be able to update menu items and mark items as unavailable.
# Orders:
# Users can place an order containing multiple items.
# An order has a status: Pending, Preparing, Out for Delivery, Delivered.
# Delivery Agents: Delivery agents pick up orders from restaurants and deliver them to users. Their location is tracked in real-time.
# Notifications: The system should notify the user about order updates (e.g., when the status changes).
# Scalability: Design should support scalability for large numbers of users, orders, and restaurants.

from abc import ABC, abstractmethod
from typing import List
from uuid import uuid4

class Item(ABC):
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.available = True
    
    @abstractmethod
    def get_price(self):
        pass
    

class Pizza(Item):
    def __init__(self, name, price):
        super().__init__(name, price)
    
    def get_price(self):
        return super().get_price()
    

class Menu:
    def __init__(self):
        self.menu = []
    
    def add_item(self, item: Item) -> None:
        self.menu.append(item)
    
    def mark_inavailable(self, item:Item) -> bool:
        for menuItem in self.menu:
            if menuItem.name == item.name:
                menuItem.available = False
                return True
        return False

    def get_menu(self) -> List[Item]:
        result = []
        for menuItem in self.menu:
            if menuItem.available:
                result.append(menuItem)
        return result

class Restaurant:
    def __init__(self, menu: Menu):
        self.menu = menu

    def add_menu_item(self, item: Item):
        self.menu.add_item(item)
    
    def mark_inavailable(self, item: Item):
        self.menu.mark_inavailable(item)
    
    def get_menu(self):
        return self.menu.get_menu()
    
    def get_price(self, selected_item: List[Item]):
        price = 0
        for item in selected_item:
            price += item.price
        return price

class Payment(ABC):
    @abstractmethod
    def make_payment(self, amount):
        pass

class Notification(ABC):
    @abstractmethod
    def notify(self, order):
        pass

class SMSNotification(Notification):
    def notify(self, order):
        print("Notify user with order details")


class Paypal(Payment):
    def make_payment(self, amount):
        print(f"Payment of {amount} is done using paypal")

class Cart:
    def __init__(self):
        self.selected_item = []
    
    def add_item(self, item: Item):
        self.selected_item.append(item)
    
    def remove_item(self, item: Item):
        self.selected_item = list(filter(lambda x: item.name != x.name, self.selected_item))


class Order:
    def __init__(self, selected_item: List[Item], payment_stratergy: Payment, rest: Restaurant, notification_stratergy: Notification, user):
        self.order_id = uuid4()
        self.selected_item = selected_item
        self.selected_rest = rest
        self.user = user
        self.payment_stratergy = payment_stratergy
        self.notification_stratergy = notification_stratergy
        self.status = "Created"
        self.delivary_agent = None
    
    def make_payment(self):
        final_price = self.selected_rest.get_price(self.selected_item)
        succuss = self.payment_stratergy.make_payment(final_price)
        if succuss:
            print("Payment for order is created")
            self.status = "PaymentDone"
            self.notification_stratergy.notify(self)
            self.delivary_agent = DeliveryAgents(self, self.user, location="Order location")
            return True
        else:
            self.status = "PaymentFailed"
            return False
    
    def get_status(self):
        return self.status



class App:
    def __init__(self):
        self.rest: List[Restaurant] = []
    
    def add_restaurant(self, new_restaurant: Restaurant):
        self.rest.append(new_restaurant)
    
    def get_all_restaurant(self):
        return self.rest
    
    def get_menu_by_index(self, index: int):
        return self.rest[index].get_menu()

    
class User:
    def __init__(self, app: App, cart: Cart, payment: Payment, notification: Notification, address: str):
        self.app = app
        self.cart = cart
        self.payment = payment
        self.notification = notification
        self.orders: List[Order] = []
        self.address = address
    
    def search_restaurant(self):
        return self.app.get_all_restaurant()
    
    def get_menu_by_id(self, index: int):
        return self.app.get_menu_by_index(index)
    
    def add_to_cart(self, item: Item):
        self.cart.add_item(item)
    
    def remove_to_cart(self, item: Item):
        self.cart.remove_item(item)
    
    def create_order(self):
        order = Order(payment_stratergy=self.payment, selected_item=self.cart.selected_item, notification_stratergy=self.notification, user=self)
        order.make_payment()
        self.orders.append(order)
    

class DeliveryAgents:
    def __init__(self, order: Order, user: User, location: str):
        self.order = order
        self.user = user
        self.order.status = "Order_Picked"
        self.location = location
    
    def update_location(self, new_location):
        self.location = new_location
    
    def made_delivary(self):
        self.order.status = "Delivered"
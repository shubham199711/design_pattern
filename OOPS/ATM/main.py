from abc import ABC, abstractmethod
from threading import Lock

class Card(ABC):
    def __init__(self, card_number, account: Account):
        self.card_number = card_number
        self.account = account

    @abstractmethod
    def set_pin(self, pin):
        raise NotImplementedError
    
    def auth_pin(self, pin):
        raise NotImplementedError

def AuthStratergy(ABC):
    @abstractmethod
    def auth(self, card: Card, pin: str):
        pass

def PinAuthStratergy(AuthStratergy):
    def auth(self, card: Card, pin: str):
        pass


    
class CreditCard(Card):
    def __init__(self, card_number: str, pin: str, auth_stratergy: AuthStratergy, account: Account):
        self.card_number = card_number
        self.__pin = pin
        self.account = account
        self.auth_stratergy = auth_stratergy
    
    def set_pin(self, pin):
        self.__pin = pin
    
    def auth_pin(self, pin):
        return self.auth_stratergy.auth(card=self, pin=self.__pin)


class NotificationStratergy(ABC):
    def send_notification(self, user: User):
        raise NotImplementedError

class Account:
    def __init__(self, amount):
        self.amount = amount
        self.cards = {}
        self.lock = Lock()
    
    def add_card(self, card: Card):
        if card.card_number in self.cards:
            return
        self.cards[card.card_number] = card
    
    def remove_card(self, card: Card):
        if card.card_number in self.cards:
            del self.cards[card.card_number]
            return True
        return False
    
    def remove_money(self, amount, card, pin):
        with self.lock:
            if self.auth_card(card=card, pin=pin):
                if self.amount - amount < 0:
                    return False
                self.amount -= amount
                return True
            return False

    def add_money(self, amount, card, pin):
        with self.lock:
            if self.auth_card(card=card, pin=pin):
                self.amount += amount
                return True
            return False

    def auth_card(self, card: Card, pin: str):
        if card.card_number in self.cards:
            return card.auth_pin(pin)
        return False


        

class SMSNotification(NotificationStratergy):
    def send_notification(self, user):
        print("SMS notification send to user ", user)

class MoneyType(ABC):
    @abstractmethod
    def add_money(self, amount):
        pass

    @abstractmethod
    def remove_money(self, amount):
        pass


class Money(MoneyType):
    _instance = None
    AMOUNT_TYPE = [1000, 100, 10, 5]
    def __init__(self):
        self.thousand_count = 0
        self.hundrand_count = 0
        self.ten_count = 0
        self.five_count = 0
        self.arr_of_money = [self.thousand_count, self.hundrand_count, self.ten_count, self.five_count]
    
    def can_add_money(self, amount_to_add):
        add_array = [0] * len(self.AMOUNT_TYPE)
        for i, amount in enumerate(self.AMOUNT_TYPE):
            ans = amount_to_add // amount
            if ans == 0:
                continue
            add_array[i] = ans
            amount_to_add -= (amount * ans)
            if amount_to_add == 0:
                break
        
        if amount_to_add > 0:
            return False
        return add_array
        


    def add_money(self, add_array):
        for i, item in enumerate(add_array):
            self.arr_of_money[i] += item
        
        return True
        

    def remove_money(self, add_array):
        for i, item in enumerate(add_array):
            self.arr_of_money[i] -= item
        
        return True
    
    def remove_money(self, amount):
        add_array = [0] * len(self.AMOUNT_TYPE)
        for i, amount in enumerate(self.AMOUNT_TYPE):
            ans = amount_to_add // amount
            if ans == 0:
                continue
            if self.arr_of_money[i] < ans:
                ans = self.arr_of_money[i]
            add_array[i] = ans
            amount_to_add -= (amount * ans)
            if amount_to_add == 0:
                break
        
        if amount_to_add > 0:
            return False
        
        return add_array
        

        


class ATM:
    def __init__(self):
        self.money = Money()
        self.card = None

    def add_card(self, card: Card):
        if self.card is not None:
            return
        if card.auth_pin():
            self.card = card
        else:
            return


    def remove_card(self):
        self.card = None
    
    def add_money(self, amount):
        if self.card is None:
            return
        money_or_not = self.money.can_add_money(amount)
        if money_or_not:
            if self.card.account.add_money(amount):
                self.money.add_money(money_or_not)
                print("Money added!!")
            else:
                print("Some ERROR in money")
        else:
            print("Problem adding money!!")
        self.remove_card()
    
    def remove_money(self, amount: int):
        if self.card is None:
            return
        if self.card.account.amount < amount:
            print("You don't have that much money in your account!")
            return False
        money_or_not = self.money.can_remove_money(amount=amount)
        if money_or_not:
            if self.card.account.remove_money(amount):
                self.money.remove_money(money_or_not)
                print("money removed!")
            else:
                print("Some ERROR in money")
        else:
            print("Not able to remove given amount")
        self.remove_card()

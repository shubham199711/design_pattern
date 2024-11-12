from abc import abstractmethod, ABC
import datetime
from typing import List

class Seat:
    def __init__(self, seat_id):
        self.seat_id = seat_id
        self.is_booked = False

    def mark_as_booked(self):
        self.is_booked = True
    
    def mark_as_available(self):
        self.is_booked = False

class Movie:
    def __init__(self, title):
        self.name = title

class Showtime:
    def __init__(self, showtime_id, movie: Movie, start_time, screen):
        self.showtime_id = showtime_id
        self.movie = movie
        self.start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M")  # Convert to datetime
        self.screen = screen
        self.available_seats = screen.seats

class Screen:
    def __init__(self, screen_id, total_seats):
        self.screen_id = screen_id
        self.seats = [Seat(seat_id=f"{row}{num}") for row in "ABC" for num in range(1, total_seats+1)]
        self.showtimes = []
    
    def add_showtime(self, showtime: Showtime):
        self.showtimes.append(showtime)
    
    def get_available_seats(self):
        return [seat for seat in self.seats if not seat.is_booked]
    

class Theater:
    def __init__(self, name, screens: List[Screen] = []):
        self.name = name
        self.screens = screens
    
    def add_screen(self, screen):
        self.screens.append(screen)
    
    def get_movies(self):
        movies = []
        for screen in self.screens:
            for showtime in screen.showtimes:
                movies.append(showtime.movie)
        return movies
    
    def get_showtime(self, movie):
        showtimes = []
        for screen in self.screens:
            for showtime in screen.showtimes:
                if showtime.movie == movie:
                    showtimes.append(showtime)
        return showtimes


class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

class User:
    def __init__(self, name, payment_info: PaymentStrategy):
        self.name = name
        self.payment_info = payment_info
        self.bookings = []
    
    def make_payment(self, showtime, seats):
        booking = Booking(user=self, showtime=showtime, seats=seats, payment=self.payment_info)
        booking_done = booking.process_payment(self)
        if booking_done:
            self.bookings.append(booking)


    
class Booking:
    def __init__(self,user, showtime, seats, payment):
        self.booking_id = f"{user.user_id}-{showtime.showtime_id}"
        self.user = user
        self.showtime = showtime
        self.seats = seats
        self.status = "Pending"
        self.payment = Payment(strategy=payment, amount=self.calculate_total_cost())
        self.observers = []
    
    def process_payment(self):
        payment_successful = self.payment.process_payment(self.calculate_total_cost())
        if payment_successful:
            self.confirm_booking()
            self.notify_observers()
        else:
            self.cancel_booking()
        return payment_successful


    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self)
        
    
    def calculate_total_cost(self):
        return sum(seat.get_price() for seat in self.seats)
    
    def confirm_booking(self):
        self.status = "Confirmed"
        for seat in self.seats:
            seat.mark_as_booked()
    
    def cancel_booking(self):
        self.status = "Canceled"
        for seat in self.seats:
            seat.mark_as_available()
        self.payment.refund()
    

class CreditCardPayment(PaymentStrategy):
    def __init__(self, card_number, expiry_date, cvv):
        self.card_number = card_number
        self.expiry_date = expiry_date
        self.cvv = cvv

    def pay(self, amount):
        print(f"Processing Credit Card payment of ${amount}.")
        return True


class Payment:
    def __init__(self, strategy: PaymentStrategy, amount):
        self.strategy = strategy
        self.amount = amount

    def process_payment(self):
        return self.strategy.pay(self.amount)


class NotificationObserver(ABC):
    @abstractmethod
    def update(self, booking):
        pass


class EmailNotification(NotificationObserver):
    def update(self, booking):
        print(f"Sending email to {booking.user.email} for booking {booking.booking_id} with status {booking.status}.")


class SMSNotification(NotificationObserver):
    def update(self, booking):
        print(f"Sending SMS for booking {booking.booking_id} with status {booking.status}.")
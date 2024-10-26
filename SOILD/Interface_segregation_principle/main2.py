# You are tasked with creating a management system for different types of vehicles
# (e.g., cars, bicycles, trucks). Each vehicle type should have specific functionalities
# such as starting the engine, stopping, and refueling. However, not all vehicle types
# need to implement every functionality.

from abc import ABC, abstractmethod

class Startable(ABC):
    @abstractmethod
    def start(self):
        pass

class Stopable(ABC):
    @abstractmethod
    def stop(self):
        pass

class Refuelable(ABC):
    @abstractmethod
    def refuel(self):
        pass

class Car(Startable, Stopable, Refuelable):
    def start(self):
        print("Starting the Car")

    def stop(self):
        print("Stoping the Car")

    def refuel(self):
        print("Refueling the Car")
    
class Truck(Startable, Stopable, Refuelable):
    def start(self):
        print("Starting the Truck")

    def stop(self):
        print("Stoping the Truck")
        
    def refuel(self):
        print("Refueling the Truck")

class Bicycle(Startable, Stopable):
    def start(self):
        print("Starting the Bicycle")

    def stop(self):
        print("Stoping the Bicycle")
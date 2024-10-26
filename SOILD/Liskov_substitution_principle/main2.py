# You are tasked with creating a simple simulation of animal behaviors. 
# You need to define a base class for Animal that can be extended to specific
# types of animals, like Dog and Cat. Each animal should have a method for
# making a sound. The design should ensure that any subclass can be used interchangeably
# with the base class without altering the expected behavior.

from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def make_sound(self):
        raise NotImplementedError

class Dog(Animal):
    def make_sound(self):
        print("make sound from dog")

class Cat(Animal):
    def make_sound(self):
        print("make sound from cat")
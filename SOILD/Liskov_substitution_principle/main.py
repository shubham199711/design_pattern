# Your task is to design a Shape system for calculating the area of various geometric shapes. 
# The system should allow you to define shapes like Rectangle and Square, and the behavior should
# conform to the Liskov Substitution Principle.

from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def area(self) -> int:
        raise NotImplementedError

class Rectangle(Shape):
    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width

    def area(self) -> int:
        return self.width * self.height

class Square(Shape):
    def __init__(self, side_length: int):
        self.side_length = side_length
    
    def area(self) -> int:
        return self.side_length * self.side_length

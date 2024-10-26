# Your task is to design a Document Management System that allows for different types
# of documents (like text documents and images). Each document type should have its own set
# of operations (like printing, saving, etc.), and the design should adhere to the Interface Segregation Principle.

from abc import ABC, abstractmethod

class Printable(ABC):
    @abstractmethod
    def print(self):
        pass

class Saveable(ABC):
    @abstractmethod
    def save(self):
        pass


class TextDocument(Printable, Saveable):
    def __init__(self, content: str):
        self.content = content

    def save(self):
        print(f"save text: {self.content}")
    
    def print(self):
        print(f"print text: {self.content}")

class ImageDocument(Printable):
    def __init__(self, image_path: str):
        self.image_path = image_path

    def print(self):
        print(f"print text: {self.image_path}")
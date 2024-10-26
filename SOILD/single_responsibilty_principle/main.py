class Book:
    def __init__(self, title: str, author: str, ISBN: str):
        self.title = title
        self.author = author
        self.ISBN = ISBN

class Logger:
    def log_action(self, msg: str):
        print(msg)

class BookStorage:
    def __init__(self):
        self.books = {}

    def add_book(self, book: Book) -> bool:
        self.books[book.ISBN] = book
        return True

    def remove_book(self, ISBN: str) -> bool:
        if ISBN in self.books:
            del self.books[ISBN]
            return True
        return False

class ManageBook:
    def __init__(self, storage: BookStorage, logger: Logger):
        self.storage = storage
        self.logger = logger

    def add_book(self, book: Book):
        if self.storage.add_book(book):
            self.logger.log_action(f"Book '{book.title}' by {book.author} added.")

    def remove_book(self, ISBN: str):
        if self.storage.remove_book(ISBN):
            self.logger.log_action(f"Book with ISBN {ISBN} removed.")
        else:
            self.logger.log_action(f"Book with ISBN {ISBN} not found.")

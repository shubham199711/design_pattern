import re
from typing import List

class Book:
    DISALLOWED_TAGS = {"traditional-book", "magazine"}

    def __init__(self, title):
        self.title = title
        self.id = None
        self.borrowed_by = None
        self.tags = set()

    def add_tag(self, tag):
        if tag not in Book.DISALLOWED_TAGS:
            self.tags.add(tag)


class TraditionalBook(Book):
    def __init__(self, title, author):
        super().__init__(title)
        self.author = author
        self.tags.add("traditional-book")

    @staticmethod
    def parse_def(book_representation):
        match_result = re.fullmatch('"(.*)" by (.*)', book_representation)
        if match_result is None:
            raise KeyError()
        return TraditionalBook(match_result[1], match_result[2])

    def __str__(self):
        return f'"{self.title}" by {self.author}'

class Magazine(Book):
    def __init__(self, title, issue_number):
        super().__init__(title)
        self.issue_number = issue_number
        self.tags.add("magazine")

    @staticmethod
    def parse_def(book_representation):
        match_result = re.fullmatch('"(.*)" Issue (.*)', book_representation)
        if match_result is None:
            raise KeyError()
        return Magazine(match_result[1], match_result[2])

    def __str__(self):
        return f'"{self.title}" Issue {self.issue_number}'

class User:
    def __init__(self, name):
        self.name = name
        self.borrowed_book = None
        self.favorite_tags = set()

    def __str__(self):
        return self.name

    def borrow_book(self, book):
        if self.borrowed_book is None and book.borrowed_by is None:
            self.borrowed_book = book
            book.borrowed_by = self

    def return_book(self):
        if (
            self.borrowed_book is not None
            and self.borrowed_book.borrowed_by is not None
        ):
            self.borrowed_book.borrowed_by = None
            self.borrowed_book = None

    def add_favorite_tag(self, tag):
        self.favorite_tags.add(tag)

    def get_suggestion_score(self, book):
        count = 0
        for tag in book.tags:
            if tag in self.favorite_tags:
                count += 1
        return count

    def get_max_suggestion_score(self, books):
        return max((self.get_suggestion_score(book) for book in books), default=0)

class Library:
    def __init__(self):
        self.books = {}
        self.users = {}

    def register_book(self, book):
        if book.id not in self.books:
            self.books[book.id] = book

    def find_user(self, username):
        if username not in self.users:
            self.users[username] = User(username)
        return self.users[username]

    def lookup_book(self, lookup_fn):
        result = []
        for book in self.books.values():
            if lookup_fn(book):
                result.append(book)
        return result

def output_book(
    book_list,
    output,
    multiple_match_fn=None,
    no_match_output="No such book exists",
):
    if not book_list:
        output.append(no_match_output)
    elif len(book_list) == 1:
        output.append(str(book_list[0]))
        output.append(f"ID: {book_list[0].id}")
        if book_list[0].borrowed_by is not None:
            output.append(f"Borrowed by: {book_list[0].borrowed_by}")
    else:
        if multiple_match_fn is None:
            raise KeyError()
        output.append(multiple_match_fn(book_list))
        available_count = 0
        for book in book_list:
            if book.borrowed_by is None:
                available_count += 1
        output.append(f"{available_count} book(s) available")

def simulate_library(instructions: List[str]) -> List[str]:
    library = Library()
    output: List[str] = []

    for instruction in instructions:
        command, sub_instruction = instruction.split(" ", 1)
        if command == "register":
            subcommand, id, rest = sub_instruction.split(" ", 2)
            new_book = None
            if subcommand == "book":
                new_book = TraditionalBook.parse_def(rest)
            elif subcommand == "magazine":
                new_book = Magazine.parse_def(rest)
            if new_book is not None:
                new_book.id = id
                library.register_book(new_book)
        elif command == "lookup":
            subcommand, rest = sub_instruction.split(" ", 1)
            if subcommand == "id":
                book_list = library.lookup_book(lambda book: book.id == rest)
                output_book(book_list, output)
            elif subcommand == "title":
                book_list = library.lookup_book(lambda book: book.title == rest)
                output_book(
                    book_list,
                    output,
                    lambda book_list: f"{len(book_list)} books match the title: {rest}",
                )
            elif subcommand == "author":
                book_list = library.lookup_book(
                    lambda book: isinstance(book, TraditionalBook) and book.author == rest
                )
                output_book(
                    book_list,
                    output,
                    lambda book_list: f"{len(book_list)} books match the author: {rest}",
                )
            elif subcommand == "tags":
                tags = rest.split(" ")
                book_list = library.lookup_book(
                    lambda book: all(tag in book.tags for tag in tags)
                )
                output_book(
                    book_list,
                    output,
                    lambda book_list: f"{len(book_list)} books match the tag(s): {rest}",
                )
            elif subcommand == "suggestion":
                user = library.find_user(rest)
                max_score = user.get_max_suggestion_score(library.books.values())
                book_list = library.lookup_book(
                    lambda book: user.get_suggestion_score(book) > 0 and user.get_suggestion_score(book) == max_score
                )
                output_book(
                    book_list,
                    output,
                    lambda book_list: f"{len(book_list)} books are suggested for: {rest}",
                )
        elif command == "borrow":
            id, name = sub_instruction.split(" ", 1)
            if id in library.books:
                library.find_user(name).borrow_book(library.books[id])
        elif command == "return":
            library.find_user(sub_instruction).return_book()
        elif command == "tag":
            id, *tags = sub_instruction.split(" ")
            if id in library.books:
                for tag in tags:
                    library.books[id].add_tag(tag)
        elif command == "favorite":
            tag, name = sub_instruction.split(" ", 1)
            library.find_user(name).add_favorite_tag(tag)
    return output

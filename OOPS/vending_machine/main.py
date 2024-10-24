from enum import Enum
from typing import Dict, List, Tuple

class Coin(Enum):
    penny = 1
    nickel = 5
    dime = 10
    quarter = 25

class Product:
    def __init__(self, name: str, price: int) -> None:
        self.name = name
        self.price = price
        self.quantity = 0

    def __str__(self) -> str:
        return f"{self.name} {self.price} {self.quantity}"

class Machine:
    def __init__(self) -> None:
        self.products: Dict[str, Product] = {}
        self.balance = 0
        self.coins = sorted(Coin, key=lambda coin: coin.value, reverse=True)

    def new_product(self, name: str, price: int) -> None:
        product = Product(name, price)
        self.products[name] = product

    def print_products(self) -> List[str]:
        products = sorted(self.products.values(), key=lambda p: p.price)
        return [str(p) for p in products]

    def restock(self, name: str, quantity: int) -> None:
        self.products[name].quantity += quantity

    def insert_coin(self, coin: Coin) -> None:
        self.balance += coin.value

    def purchase(self, name: str) -> bool:
        product = self.products[name]
        if product.price <= self.balance and product.quantity >= 1:
            self.balance -= product.price
            product.quantity -= 1
            return True
        return False

    def checkout(self) -> List[Tuple[int, Coin]]:
        balance = self.balance
        self.balance = 0
        out: List[Tuple[int, Coin]] = []
        for coin in self.coins:
            n, balance = divmod(balance, coin.value)
            if n:
                out.append((n, coin))
        return out

def vending_machine(instructions: List[List[str]]) -> List[str]:
    output_lines = []
    machine = Machine()
    for instruction in instructions:
        if instruction[0] == "new_product":
            machine.new_product(instruction[1], int(instruction[2]))
        elif instruction[0] == "print_products":
            output_lines += machine.print_products()
        elif instruction[0] == "restock":
            machine.restock(instruction[1], int(instruction[2]))
        elif instruction[0] == "insert_coin":
            name = instruction[1]
            if name in Coin.__members__:
                machine.insert_coin(Coin[name])
                output_lines.append("accepted")
            else:
                output_lines.append("rejected")
        elif instruction[0] == "purchase":
            output_lines.append("true" if machine.purchase(instruction[1]) else "false")
        elif instruction[0] == "checkout":
            for n, coin in machine.checkout():
                output_lines.append(f"{n} {coin.name}")
    return output_lines
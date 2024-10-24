from enum import Enum
from typing import Optional, List

class CarSize(Enum):
    SMALL = 0
    MEDIUM = 1
    LARGE = 2

SIZE_STRING = {
    CarSize.SMALL: "Small",
    CarSize.MEDIUM: "Medium",
    CarSize.LARGE: "Large",
}

SIZES = {e: n for n, e in SIZE_STRING.items()}

class Car:
    def __init__(self, size: str, color: str, brand: str):
        self.brand = brand
        self.size = SIZES[size]
        self.color = color
    
    def __str__(self):
        return f"{SIZE_STRING[self.size]} {self.color} {self.brand}"

class ParkingSpot:
    def __init__(self, size: str):
        self.vehical_parked: Optional[Car] = None
        self.size = SIZES[size]
    
    def park(self, car: Car):
        if self.vehical_parked:
            return False
        if self.size.value < car.size.value:
            return False
        self.vehical_parked = car
        return True
    
    def leave(self):
        if self.vehical_parked:
            self.vehical_parked = None
            return True
        return False
    
    def __str__(self):
        if self.vehical_parked:
            return str(self.vehical_parked)
        return "Empty"

class ParkingLot:
    def __init__(self, spots: List[str]):
        self.parking_spots: list[ParkingSpot] = []
        for spot in spots:
            self.parking_spots.append(ParkingSpot(size=spot))
        self.__size = len(spots)
        self.__free_spot = len(spots)
    
    def free_spots(self) -> int:
        return self.__free_spot
    
    def leave(self, index: int):
        if self.parking_spots[index].leave():
            self.__free_spot += 1
    
    def park(self, index: int, car: Car):
        for i in range(index, self.__size):
            if self.parking_spots[i].park(car=car):
                self.__free_spot -= 1
                return True
        for i in range(index):
            if self.parking_spots[i].park(car=car):
                self.__free_spot -= 1
                return True
        return False

def parking_system(spots: List[str], instructions: List[List[str]]) -> List[str]:
    ans = []
    p = ParkingLot(spots=spots)
    for instruction in instructions:
        operation, *args = instruction
        if operation == "park":
            slot, *car_args = args
            p.park(int(slot), car=Car(*car_args))
        elif operation == "remove":
            p.leave(int(args[0]))
        elif operation == "print":
            output = str(p.parking_spots[int(args[0])])
            ans.append(output)
        elif operation == "print_free_spots":
            ans.append(str(p.free_spots()))
    return ans


instructions = [
  ["park", "1", "Small", "Silver", "BMW"],
  ["park", "1", "Large", "Black", "Nissan"],
  ["print", "1"],
  ["print", "2"],
  ["print", "3"],
]
n = 5
parking_system(instructions=instructions, n=n)
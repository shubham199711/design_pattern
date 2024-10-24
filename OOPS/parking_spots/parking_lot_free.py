from bisect import bisect_right
from enum import Enum
from typing import List, Optional

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
        self.size = SIZES[size]
        self.color = color
        self.brand = brand

    def __str__(self) -> str:
        return f"{SIZE_STRING[self.size]} {self.color} {self.brand}"

class ParkingSpot:
    def __init__(self, size: str):
        self.parked_car: Optional[Car] = None
        self.size = SIZES[size]

    def park(self, car: Car) -> bool:
        if self.parked_car:
            return False
        if self.size.value < car.size.value:
            return False
        self.parked_car = car
        return True

    def leave(self) -> bool:
        if self.parked_car:
            self.parked_car = None
            return True
        return False

    def __str__(self) -> str:
        if self.parked_car:
            return str(self.parked_car)
        return "Empty"

class ParkingInterval:
    def __init__(self, start: int, end: int, car: Optional[Car]) -> None:
        self.start = start
        self.end = end
        self.car = car

    @property
    def size(self):
        return self.end - self.start

    def __lt__(self, other):
        return self.start < other.start

    def get_max_slots(self, car_size: int) -> int:
        return self.size // car_size

    # Try to park a car at this interval.
    # If fail, return None
    # Otherwise, return a list representing the new interval.
    def park(self, car_interval):
        if self.car:
            return None
        if self.size < car_interval.size:
            return None
        if self.start > car_interval.start:
            car_interval = ParkingInterval(
                self.start,
                self.start + car_interval.size,
                car_interval.car,
            )
        return_list = []
        if self.start < car_interval.start:
            return_list.append(ParkingInterval(self.start, car_interval.start, None))
        return_list.append(car_interval)
        if self.end > car_interval.end:
            return_list.append(ParkingInterval(car_interval.end, self.end, None))
        return return_list

class ParkingLot:
    def free_spots(self) -> int:
        raise NotImplementedError

    def park(self, index: int, car: Car) -> bool:
        raise NotImplementedError

    def leave(self, index: int) -> None:
        raise NotImplementedError

    def get_spot(self, index: int) -> Optional[Car]:
        raise NotImplementedError

class RegularParkingLot(ParkingLot):
    def __init__(self, spots: List[str]) -> None:
        self.parking_spots: list[ParkingSpot] = []
        self.__size = len(spots)
        self.__free_spots = self.__size
        for entry in spots:
            self.parking_spots.append(ParkingSpot(entry))

    def free_spots(self) -> int:
        return self.__free_spots

    def park(self, index: int, car: Car) -> bool:
        for i in range(index, self.__size):
            if self.parking_spots[i].park(car):
                self.__free_spots -= 1
                return True
        return False

    def leave(self, index: int) -> None:
        if self.parking_spots[index].leave():
            self.__free_spots += 1

    def get_spot(self, index: int) -> Optional[Car]:
        return self.parking_spots[index].parked_car

class UnboundedParkingLot(ParkingLot):
    def __init__(
        self,
        length: int,
        small_size: int,
        med_size: int,
        large_size: int,
    ) -> None:
        self.length = length
        self.car_sizes = {
            CarSize.SMALL: small_size,
            CarSize.MEDIUM: med_size,
            CarSize.LARGE: large_size,
        }
        self.parking_spots = [ParkingInterval(0, length, None)]
        self.__free_spots = self.parking_spots[0].get_max_slots(large_size)

    def free_spots(self) -> int:
        return self.__free_spots

    def find_interval_index(self, index: int) -> int:
        temp_interval = ParkingInterval(index, index, None)
        return max(0, bisect_right(self.parking_spots, temp_interval) - 1)

    def park(self, index: int, car: Car) -> bool:
        car_size = self.car_sizes[car.size]
        car_interval = ParkingInterval(index, index + car_size, car)
        index = self.find_interval_index(index)
        for i in range(index, len(self.parking_spots)):
            spot = self.parking_spots[i]
            new_intervals = spot.park(car_interval)
            if new_intervals:
                self.__free_spots -= spot.get_max_slots(self.car_sizes[CarSize.LARGE])
                for entry in new_intervals:
                    if entry.car is None:
                        self.__free_spots += entry.get_max_slots(self.car_sizes[CarSize.LARGE])
                self.parking_spots[i : i + 1] = new_intervals
                return True
        return False

    def leave(self, index: int) -> None:
        start_index = self.find_interval_index(index)
        end_index = start_index + 1
        if self.parking_spots[start_index].car is None:
            return
        if (
            end_index < len(self.parking_spots)
            and self.parking_spots[end_index].car is None
        ):
            end_index += 1
        if start_index > 0 and self.parking_spots[start_index - 1].car is None:
            start_index -= 1
        for i in range(start_index, end_index):
            if self.parking_spots[i].car is None:
                self.__free_spots -= self.parking_spots[i].get_max_slots(self.car_sizes[CarSize.LARGE])
        new_interval = ParkingInterval(
            self.parking_spots[start_index].start,
            self.parking_spots[end_index - 1].end,
            None,
        )
        self.parking_spots[start_index:end_index] = [new_interval]
        self.__free_spots += new_interval.get_max_slots(self.car_sizes[CarSize.LARGE])

    def get_spot(self, index: int) -> Optional[Car]:
        interval_index = self.find_interval_index(index)
        return self.parking_spots[interval_index].car

def parking_system(lot_type: str, params: List[str], instructions: List[List[str]]) -> List[str]:
    output_lines = []
    parking_lot: ParkingLot
    if lot_type == "Regular":
        parking_lot = RegularParkingLot(params)
    elif lot_type == "Unbounded":
        parking_lot = UnboundedParkingLot(*(int(val) for val in params))
    else:
        raise ValueError(lot_type)
    for instruction in instructions:
        operation, *args = instruction
        if operation == "park":
            slot, *car_args = args
            parking_lot.park(int(slot), Car(*car_args))
        elif operation == "remove":
            parking_lot.leave(int(args[0]))
        elif operation == "print":
            car = parking_lot.get_spot(int(args[0]))
            output_lines.append(str(car) if car else "Empty")
        elif operation == "print_free_spots":
            output_lines.append(str(parking_lot.free_spots()))
    return output_lines
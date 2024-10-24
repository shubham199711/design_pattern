from collections import deque
from typing import List

MAX_RANKS = 3

class CallInstance:
    def __init__(self, number):
        self.number = number
        self.talking_to = None
        self.rank = 0

    def start_call(self, target, output):
        if self.talking_to is None and target.talking_to is None:
            self.talking_to = target
            target.talking_to = self
            output.append(f"Connecting {self} to {target}")
            if isinstance(target, Respondent):
                target.performance_rating += 1
            return True
        return False

    def end_call(self, output):
        if self.talking_to is not None:
            output.append(f"Call between {self} and {self.talking_to} ended")
            self.talking_to.talking_to = None
            self.talking_to = None
            return True
        return False

    def escalate(self, output):
        if self.talking_to is not None and self.rank < MAX_RANKS - 1:
            if self.end_call(output):
                self.rank += 1
                return True
        return False

    def __str__(self):
        return self.number

class Employee:
    def __init__(self, name):
        self.talking_to = None
        self.name = name

    def __str__(self):
        return f"{self.name}"

    @staticmethod
    def create_employee(role, name):
        if role == "Respondent":
            return Respondent(name)
        elif role == "Manager":
            return Manager(name)
        elif role == "Director":
            return Director(name)
        else:
            return None

    @property
    def rank(self):
        raise NotImplementedError()

    def work(self, call_center, output):
        raise NotImplementedError()

class Respondent(Employee):
    def __init__(self, name):
        super().__init__(name)
        self.performance_rating = 0

    def __str__(self):
        return f"Respondent {self.name}"

    @property
    def rank(self):
        return 0

    def work(self, call_center, output):
        self.performance_rating += 1

class Manager(Employee):
    def __str__(self):
        return f"Manager {self.name}"

    @property
    def rank(self):
        return 1

    def work(self, call_center, output):
        top_worker = None
        for respondent in call_center.employees[0]:
            if respondent.talking_to is None:
                if (
                    top_worker is None
                    or respondent.performance_rating > top_worker.performance_rating
                ):
                    top_worker = respondent
        if top_worker is not None:
            output.append(
                f"Respondent {top_worker.name} is promoted to Manager"
                f" under the authority of Manager {self.name}"
            )
            call_center.promote(top_worker, Manager)

class Director(Employee):
    def __str__(self):
        return f"Director {self.name}"

    @property
    def rank(self):
        return 2

    def work(self, call_center, output):
        output.append(f"{self} holds a meeting")

class CallCenter:
    def __init__(self):
        self.employees = []
        self.employee_map = {}
        self.call_queue = []
        for _ in range(MAX_RANKS):
            self.employees.append([])
            self.call_queue.append(deque())
        self.call_map = {}

    def hire(self, employee):
        self.employees[employee.rank].append(employee)
        self.employee_map[str(employee)] = employee

    def remove(self, employee):
        employee_list = self.employees[employee.rank]
        if employee in employee_list:
            employee_list.remove(employee)
            del self.employee_map[str(employee)]

    def promote(self, employee, new_class):
        self.remove(employee)
        new_employee = new_class(employee.name)
        self.hire(new_employee)

    def add_call_to_queue(self, number):
        if number not in self.call_map:
            self.call_map[number] = CallInstance(number)
            self.call_queue[0].append(self.call_map[number])

    def resolve_queue(self, output):
        for i in reversed(range(MAX_RANKS)):
            current_queue = self.call_queue[i]
            current_employees = self.employees[i]
            while current_queue:
                top = current_queue[0]
                resolved = False
                for employee in current_employees:
                    if top.start_call(employee, output):
                        resolved = True
                        break
                if resolved:
                    current_queue.popleft()
                else:
                    break

    def escalate(self, phone, output):
        if phone in self.call_map:
            current_call = self.call_map[phone]
            if current_call.escalate(output):
                self.call_queue[current_call.rank].append(current_call)
                return True
        return False

def simulate_call_center(instructions: List[List[str]]) -> List[str]:
    call_center = CallCenter()
    output: List[str] = []
    for instruction in instructions:
        command, *params = instruction
        if command == "hire":
            call_center.hire(Employee.create_employee(*params))
            call_center.resolve_queue(output)
        elif command == "end":
            number = params[0]
            if number in call_center.call_map:
                current_call = call_center.call_map[number]
                if current_call.end_call(output):
                    del call_center.call_map[number]
                    call_center.resolve_queue(output)
        elif command == "dispatch":
            number = params[0]
            call_center.add_call_to_queue(number)
            call_center.resolve_queue(output)
        elif command == "escalate":
            number = params[0]
            call_center.escalate(number, output)
            call_center.resolve_queue(output)
        elif command == "work":
            worker_id = " ".join(params)
            if worker_id in call_center.employee_map:
                worker = call_center.employee_map[worker_id]
                if worker.talking_to is None:
                    worker.work(call_center, output)
    return output
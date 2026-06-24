from dataclasses import dataclass


@dataclass
class PetTask:
    title: str
    duration_minutes: int
    priority: str
    frequency: str

    def priority_score(self) -> int:
        pass

    def __repr__(self) -> str:
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int

    def summary(self) -> str:
        pass


class Schedule:
    def __init__(self, pet: Pet, planned_tasks: list):
        self.pet = pet
        self.planned_tasks = planned_tasks

    def total_duration(self) -> int:
        pass

    def display(self) -> str:
        pass


class Scheduler:
    def __init__(self, pet: Pet):
        self.pet = pet
        self.tasks: list = []

    def add_task(self, task: PetTask) -> None:
        pass

    def remove_task(self, title: str) -> None:
        pass

    def build_schedule(self) -> Schedule:
        pass

    def _sort_tasks(self) -> list:
        pass

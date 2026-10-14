"""Core class skeletons for the PawPal+ pet care planner."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Owner:
    owner_name: str
    preference: str
    pets: list[Pet] = field(default_factory=list)
    schedules: list[Schedule] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass


@dataclass
class Pet:
    pet_name: str
    pet_breed: str
    tasks: list[Task] = field(default_factory=list)


@dataclass
class Task:
    task_name: str
    time_to_complete: int
    priority: str

    def create_task(self) -> None:
        pass


@dataclass
class Schedule:
    tasks: list[Task] = field(default_factory=list)

    def create_schedule(self) -> None:
        pass
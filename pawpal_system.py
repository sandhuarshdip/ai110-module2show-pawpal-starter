"""Core class skeletons for the PawPal+ pet care planner."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(eq=False)
class Owner:
    owner_name: str
    preference: str
    pets: list[Pet] = field(default_factory=list)
    schedules: list[Schedule] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's collection if it is not already present."""
        if not any(existing_pet is pet for existing_pet in self.pets):
            self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Return every task belonging to this owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]

    def create_schedule(self, available_minutes: int) -> Schedule:
        """Build and store a schedule using the given available time."""
        schedule = Schedule(available_minutes=available_minutes)
        schedule.create_schedule(self)
        self.schedules.append(schedule)
        return schedule


@dataclass(eq=False)
class Pet:
    pet_name: str
    pet_breed: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet while enforcing single-pet ownership."""
        if task.pet is not None and task.pet is not self:
            raise ValueError("A task can only belong to one pet.")
        if not any(existing_task is task for existing_task in self.tasks):
            task.pet = self
            self.tasks.append(task)


@dataclass(eq=False)
class Task:
    description: str
    time_to_complete: int
    priority: str
    frequency: str = "daily"
    completed: bool = False
    pet: Pet | None = field(default=None, repr=False)

    def __post_init__(self) -> None:
        """Validate the task description, duration, priority, and frequency."""
        if not self.description.strip():
            raise ValueError("Task description cannot be empty.")
        if self.time_to_complete <= 0:
            raise ValueError("Task duration must be greater than zero minutes.")
        if self.priority.lower() not in {"high", "medium", "low"}:
            raise ValueError(f"Unsupported task priority: {self.priority}")
        if not self.frequency.strip():
            raise ValueError("Task frequency cannot be empty.")

    @classmethod
    def create_task(
        cls,
        description: str,
        time_to_complete: int,
        priority: str,
        frequency: str = "daily",
    ) -> Task:
        """Create a task with the supplied details."""
        return cls(description, time_to_complete, priority, frequency)

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def mark_incomplete(self) -> None:
        """Mark this task as not completed."""
        self.completed = False


@dataclass(eq=False)
class Schedule:
    available_minutes: int
    tasks: list[Task] = field(default_factory=list)
    unscheduled_tasks: list[Task] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Ensure the available scheduling time is not negative."""
        if self.available_minutes < 0:
            raise ValueError("Available time cannot be negative.")

    def create_schedule(self, owner: Owner) -> list[Task]:
        """Select incomplete owner tasks by priority within the time limit."""
        tasks = [task for task in owner.get_all_tasks() if not task.completed]
        priority_order = {"high": 0, "medium": 1, "low": 2}
        selected_tasks: list[Task] = []
        unscheduled_tasks: list[Task] = []
        remaining_minutes = self.available_minutes

        for task in sorted(
            tasks,
            key=lambda item: (
                priority_order[item.priority.lower()],
                item.time_to_complete,
            ),
        ):
            if task.time_to_complete <= remaining_minutes:
                selected_tasks.append(task)
                remaining_minutes -= task.time_to_complete
            else:
                unscheduled_tasks.append(task)

        self.tasks = selected_tasks
        self.unscheduled_tasks = unscheduled_tasks
        return self.tasks
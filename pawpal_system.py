"""Core class skeletons for the PawPal+ pet care planner."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, time, timedelta


PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


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

    def filter_tasks(
        self,
        completed: bool | None = None,
        pet_name: str | None = None,
    ) -> list[Task]:
        """Filter this owner's tasks by completion status and/or pet name."""
        normalized_pet_name = (
            pet_name.casefold().strip() if pet_name is not None else None
        )
        if normalized_pet_name == "":
            raise ValueError("Pet name cannot be empty.")

        return [
            task
            for task in self.get_all_tasks()
            if (completed is None or task.completed is completed)
            and (
                normalized_pet_name is None
                or (
                    task.pet is not None
                    and task.pet.pet_name.casefold() == normalized_pet_name
                )
            )
        ]

    def create_schedule(self) -> Schedule:
        """Build and store a schedule for today and the following day."""
        schedule = Schedule()
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
    daily: bool = False
    completed: bool = False
    pet: Pet | None = field(default=None, repr=False)
    due_date: date = field(default_factory=date.today)
    scheduled_time: time | None = None

    def __post_init__(self) -> None:
        """Validate the task description, duration, and priority."""
        if not self.description.strip():
            raise ValueError("Task description cannot be empty.")
        if self.time_to_complete <= 0:
            raise ValueError("Task duration must be greater than zero minutes.")
        if self.priority.lower() not in {"high", "medium", "low"}:
            raise ValueError(f"Unsupported task priority: {self.priority}")

    @classmethod
    def create_task(
        cls,
        description: str,
        time_to_complete: int,
        priority: str,
        daily: bool = False,
        scheduled_time: time | None = None,
    ) -> Task:
        """Create a task with the supplied details."""
        return cls(
            description,
            time_to_complete,
            priority,
            daily=daily,
            scheduled_time=scheduled_time,
        )

    def mark_complete(self) -> Task | None:
        """Complete this task and create tomorrow's instance when it is daily."""
        if self.completed:
            return None

        self.completed = True
        if not self.daily:
            return None

        next_task = Task(
            description=self.description,
            time_to_complete=self.time_to_complete,
            priority=self.priority,
            daily=True,
            due_date=date.today() + timedelta(days=1),
            scheduled_time=self.scheduled_time,
        )
        if self.pet is not None:
            self.pet.add_task(next_task)
        return next_task

    def mark_incomplete(self) -> None:
        """Mark this task as not completed."""
        self.completed = False


@dataclass(eq=False)
class Schedule:
    tasks_by_date: dict[date, list[Task]] = field(default_factory=dict)

    def create_schedule(
        self,
        owner: Owner,
        today: date | None = None,
    ) -> dict[date, list[Task]]:
        """List incomplete tasks due today and tomorrow, ordered by priority."""
        schedule_start = today or date.today()
        tomorrow = schedule_start + timedelta(days=1)
        tasks_by_date = {
            schedule_start: [],
            tomorrow: [],
        }

        for task in owner.get_all_tasks():
            if task.completed:
                continue
            due_day = schedule_start if task.due_date <= schedule_start else task.due_date
            if due_day in tasks_by_date:
                tasks_by_date[due_day].append(task)

        for tasks in tasks_by_date.values():
            tasks.sort(key=lambda task: PRIORITY_ORDER[task.priority.lower()])

        self.tasks_by_date = tasks_by_date
        return self.tasks_by_date

    def get_conflict_warnings(self) -> list[str]:
        """Return warnings for multiple tasks with the same date and start time."""
        warnings = []
        for scheduled_date, tasks in self.tasks_by_date.items():
            tasks_by_time: dict[time, list[Task]] = {}
            for task in tasks:
                if task.scheduled_time is not None:
                    tasks_by_time.setdefault(task.scheduled_time, []).append(task)

            for scheduled_time, conflicting_tasks in tasks_by_time.items():
                if len(conflicting_tasks) < 2:
                    continue

                task_names = [
                    f"{task.description} for "
                    f"{task.pet.pet_name if task.pet is not None else 'an unassigned pet'}"
                    for task in conflicting_tasks
                ]
                warnings.append(
                    f"Warning: Scheduling conflict on {scheduled_date.isoformat()} "
                    f"at {scheduled_time.strftime('%I:%M %p').lstrip('0')}: "
                    f"{'; '.join(task_names)}."
                )

        return warnings
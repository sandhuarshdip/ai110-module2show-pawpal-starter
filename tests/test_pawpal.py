from datetime import date, time, timedelta

import pytest

from pawpal_system import Owner, Pet, Schedule, Task


def test_schedule_lists_today_tasks_in_priority_order_without_times() -> None:
    today = date.today()
    owner = Owner("Jordan", "Morning care")
    pet = Pet("Mochi", "Shiba Inu")
    low_priority = Task("Grooming", 20, "low")
    high_priority = Task("Medication", 5, "high")
    medium_priority = Task("Play", 15, "medium")
    for task in (low_priority, high_priority, medium_priority):
        pet.add_task(task)
    owner.add_pet(pet)

    schedule = Schedule()
    schedule.create_schedule(owner, today=today)

    assert schedule.tasks_by_date[today] == [
        high_priority,
        medium_priority,
        low_priority,
    ]
    assert schedule.tasks_by_date[today + timedelta(days=1)] == []


def test_schedule_warns_for_tasks_at_same_time_for_different_pets() -> None:
    owner = Owner("Jordan", "Morning care")
    dog = Pet("Mochi", "Shiba Inu")
    cat = Pet("Nori", "Tabby")
    dog_task = Task("Morning walk", 30, "high", scheduled_time=time(8, 0))
    cat_task = Task("Breakfast", 10, "high", scheduled_time=time(8, 0))
    dog.add_task(dog_task)
    cat.add_task(cat_task)
    owner.add_pet(dog)
    owner.add_pet(cat)

    warnings = owner.create_schedule().get_conflict_warnings()

    assert warnings == [
        f"Warning: Scheduling conflict on {date.today().isoformat()} at 8:00 AM: "
        "Morning walk for Mochi; Breakfast for Nori."
    ]


def test_schedule_warns_for_tasks_at_same_time_for_same_pet() -> None:
    owner = Owner("Jordan", "Morning care")
    pet = Pet("Mochi", "Shiba Inu")
    first_task = Task("Morning walk", 30, "high", scheduled_time=time(8, 0))
    second_task = Task("Medication", 5, "high", scheduled_time=time(8, 0))
    pet.add_task(first_task)
    pet.add_task(second_task)
    owner.add_pet(pet)

    warnings = owner.create_schedule().get_conflict_warnings()

    assert len(warnings) == 1
    assert "Morning walk for Mochi; Medication for Mochi" in warnings[0]


def test_mark_complete_changes_task_status() -> None:
    task = Task("Feed the pet", 10, "high")

    task.mark_complete()

    assert task.completed is True


def test_completed_task_is_not_included_in_schedule() -> None:
    owner = Owner("Jordan", "Morning care")
    pet = Pet("Mochi", "Shiba Inu")
    task = Task("Feed the pet", 10, "high")
    pet.add_task(task)
    owner.add_pet(pet)

    task.mark_complete()
    schedule = owner.create_schedule()

    assert schedule.tasks_by_date[date.today()] == []
    assert owner.filter_tasks(completed=True) == [task]


def test_rebuilt_schedule_removes_task_completed_after_initial_schedule() -> None:
    owner = Owner("Jordan", "Morning care")
    pet = Pet("Mochi", "Shiba Inu")
    task = Task("Feed the pet", 10, "high")
    pet.add_task(task)
    owner.add_pet(pet)

    first_schedule = owner.create_schedule()
    task.mark_complete()
    refreshed_schedule = owner.create_schedule()

    assert first_schedule.tasks_by_date[date.today()] == [task]
    assert refreshed_schedule.tasks_by_date[date.today()] == []


def test_adding_task_increases_pet_task_count() -> None:
    pet = Pet("Mochi", "Shiba Inu")
    task = Task("Morning walk", 30, "high")
    initial_task_count = len(pet.tasks)

    pet.add_task(task)

    assert len(pet.tasks) == initial_task_count + 1


def test_filter_tasks_by_completion_status_and_pet_name() -> None:
    owner = Owner("Jordan", "Morning care")
    dog = Pet("Mochi", "Shiba Inu")
    cat = Pet("Nori", "Tabby")
    incomplete_dog_task = Task("Walk", 30, "high")
    completed_dog_task = Task("Grooming", 20, "low")
    completed_dog_task.mark_complete()
    incomplete_cat_task = Task("Feed", 10, "medium")
    dog.add_task(incomplete_dog_task)
    dog.add_task(completed_dog_task)
    cat.add_task(incomplete_cat_task)
    owner.add_pet(dog)
    owner.add_pet(cat)

    assert owner.filter_tasks(completed=False) == [
        incomplete_dog_task,
        incomplete_cat_task,
    ]
    assert owner.filter_tasks(completed=True) == [completed_dog_task]
    assert owner.filter_tasks(pet_name="mOcHi") == [
        incomplete_dog_task,
        completed_dog_task,
    ]
    assert owner.filter_tasks(completed=False, pet_name="Mochi") == [
        incomplete_dog_task
    ]
    assert owner.filter_tasks() == [
        incomplete_dog_task,
        completed_dog_task,
        incomplete_cat_task,
    ]


def test_filter_tasks_rejects_an_empty_pet_name() -> None:
    owner = Owner("Jordan", "Morning care")

    with pytest.raises(ValueError, match="Pet name cannot be empty"):
        owner.filter_tasks(pet_name="  ")


def test_completing_daily_task_creates_a_new_instance_for_tomorrow() -> None:
    pet = Pet("Mochi", "Shiba Inu")
    task = Task(
        "Medication",
        5,
        "high",
        daily=True,
        scheduled_time=time(8, 0),
    )
    pet.add_task(task)

    next_task = task.mark_complete()

    assert next_task is not None
    assert next_task is not task
    assert next_task.due_date == date.today() + timedelta(days=1)
    assert next_task.description == task.description
    assert next_task.daily is True
    assert next_task.scheduled_time == time(8, 0)
    assert next_task.completed is False
    assert next_task.pet is pet
    assert pet.tasks == [task, next_task]


def test_completing_daily_task_twice_does_not_create_duplicate_instances() -> None:
    pet = Pet("Mochi", "Shiba Inu")
    task = Task("Medication", 5, "high", daily=True)
    pet.add_task(task)

    next_task = task.mark_complete()
    repeated_result = task.mark_complete()

    assert next_task is not None
    assert repeated_result is None
    assert pet.tasks == [task, next_task]


def test_completing_daily_task_lists_new_instance_for_tomorrow() -> None:
    owner = Owner("Jordan", "Morning care")
    pet = Pet("Mochi", "Shiba Inu")
    task = Task("Medication", 10, "high", daily=True)
    pet.add_task(task)
    owner.add_pet(pet)
    next_task = task.mark_complete()
    assert next_task is not None

    schedule = owner.create_schedule()

    assert schedule.tasks_by_date[date.today()] == []
    assert schedule.tasks_by_date[date.today() + timedelta(days=1)] == [next_task]


def test_schedule_returns_tasks_in_chronological_date_order() -> None:
    today = date.today()
    owner = Owner("Jordan", "Morning care")
    pet = Pet("Mochi", "Shiba Inu")
    overdue_task = Task(
        "Overdue grooming", 20, "medium", due_date=today - timedelta(days=1)
    )
    today_task = Task("Today's walk", 30, "medium", due_date=today)
    tomorrow_task = Task(
        "Tomorrow's medication", 5, "medium", due_date=today + timedelta(days=1)
    )
    future_task = Task(
        "Future checkup", 15, "medium", due_date=today + timedelta(days=2)
    )
    for task in (overdue_task, today_task, tomorrow_task, future_task):
        pet.add_task(task)
    owner.add_pet(pet)

    schedule = Schedule()
    schedule.create_schedule(owner, today=today)

    assert list(schedule.tasks_by_date) == [today, today + timedelta(days=1)]
    assert schedule.tasks_by_date[today] == [overdue_task, today_task]
    assert schedule.tasks_by_date[today + timedelta(days=1)] == [tomorrow_task]


def test_schedule_preserves_insertion_order_for_equal_priority_tasks() -> None:
    today = date.today()
    owner = Owner("Jordan", "Morning care")
    pet = Pet("Mochi", "Shiba Inu")
    first_task = Task("Morning walk", 30, "high", due_date=today)
    second_task = Task("Medication", 5, "high", due_date=today)
    pet.add_task(first_task)
    pet.add_task(second_task)
    owner.add_pet(pet)

    schedule = Schedule()
    schedule.create_schedule(owner, today=today)

    assert schedule.tasks_by_date[today] == [first_task, second_task]


def test_schedule_flags_duplicate_tasks_with_the_same_scheduled_time() -> None:
    owner = Owner("Jordan", "Morning care")
    pet = Pet("Mochi", "Shiba Inu")
    first_task = Task("Medication", 5, "high", scheduled_time=time(8, 0))
    duplicate_task = Task("Medication", 5, "high", scheduled_time=time(8, 0))
    pet.add_task(first_task)
    pet.add_task(duplicate_task)
    owner.add_pet(pet)

    warnings = owner.create_schedule().get_conflict_warnings()

    assert len(warnings) == 1
    assert "Medication for Mochi; Medication for Mochi" in warnings[0]


def test_schedule_does_not_return_completed_tasks() -> None:
    today = date.today()
    owner = Owner("Jordan", "Morning care")
    pet = Pet("Mochi", "Shiba Inu")
    incomplete_task = Task("Morning walk", 30, "medium", due_date=today)
    completed_task = Task("Medication", 5, "high", due_date=today)
    completed_task.mark_complete()
    pet.add_task(incomplete_task)
    pet.add_task(completed_task)
    owner.add_pet(pet)

    schedule = Schedule()
    schedule.create_schedule(owner, today=today)

    assert schedule.tasks_by_date[today] == [incomplete_task]

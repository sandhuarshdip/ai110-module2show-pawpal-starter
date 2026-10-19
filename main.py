"""Run a small PawPal+ daily schedule example from the terminal."""

from datetime import date, time, timedelta

from pawpal_system import Owner, Pet, Task


def main() -> None:
    owner = Owner(owner_name="Jordan", preference="Morning care")

    dog = Pet(pet_name="Mochi", pet_breed="Shiba Inu")
    cat = Pet(pet_name="Nori", pet_breed="Tabby")
    owner.add_pet(dog)
    owner.add_pet(cat)

    grooming = Task("Grooming", 20, "low")
    grooming.mark_complete()
    dog.add_task(grooming)
    cat.add_task(Task("Playtime", 15, "medium"))
    cat.add_task(Task("Breakfast", 10, "high", scheduled_time=time(8, 0)))
    dog.add_task(Task("Morning walk", 30, "high", scheduled_time=time(8, 0)))
    cat.add_task(Task("Medication", 5, "high", daily=True))

    print("Incomplete tasks:")
    for task in owner.filter_tasks(completed=False):
        pet_name = task.pet.pet_name if task.pet is not None else "Unknown pet"
        print(f"- {task.description} for {pet_name}")

    print("\nTasks for Mochi:")
    for task in owner.filter_tasks(pet_name="Mochi"):
        status = "complete" if task.completed else "incomplete"
        print(f"- {task.description} ({status})")

    schedule = owner.create_schedule()

    print("\nSchedule warnings:")
    warnings = schedule.get_conflict_warnings()
    if warnings:
        for warning in warnings:
            print(f"- {warning}")
    else:
        print("- No scheduling conflicts.")

    for schedule_date, label in (
        (date.today(), "Today"),
        (date.today() + timedelta(days=1), "Tomorrow"),
    ):
        print(f"{label}'s tasks for {owner.owner_name}:")
        tasks = schedule.tasks_by_date[schedule_date]
        if not tasks:
            print("- No incomplete tasks.")
        for task in tasks:
            pet_name = task.pet.pet_name if task.pet is not None else "Unknown pet"
            print(
                f"- {task.description} for {pet_name}: "
                f"{task.time_to_complete} min ({task.priority} priority)"
                + (
                    f" at {task.scheduled_time.strftime('%I:%M %p').lstrip('0')}"
                    if task.scheduled_time is not None
                    else ""
                )
            )


if __name__ == "__main__":
    main()
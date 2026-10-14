"""Run a small PawPal+ daily schedule example from the terminal."""

from pawpal_system import Owner, Pet, Task


def main() -> None:
    owner = Owner(owner_name="Jordan", preference="Morning care")

    dog = Pet(pet_name="Mochi", pet_breed="Shiba Inu")
    cat = Pet(pet_name="Nori", pet_breed="Tabby")
    owner.add_pet(dog)
    owner.add_pet(cat)

    dog.add_task(Task("Morning walk", 30, "high", "daily"))
    dog.add_task(Task("Grooming", 20, "low", "weekly"))
    cat.add_task(Task("Breakfast", 10, "high", "daily"))
    cat.add_task(Task("Playtime", 15, "medium", "daily"))

    available_minutes = sum(
        task.time_to_complete
        for task in owner.get_all_tasks()
        if not task.completed
    )
    schedule = owner.create_schedule(available_minutes)

    print(f"Today's Schedule for {owner.owner_name}")
    if schedule.tasks:
        for task in schedule.tasks:
            pet_name = task.pet.pet_name if task.pet is not None else "Unknown pet"
            print(
                f"- {task.description} for {pet_name}: "
                f"{task.time_to_complete} min ({task.priority} priority)"
            )
    else:
        print("- No tasks fit into the available time.")

    if schedule.unscheduled_tasks:
        print("\nNot scheduled (time limit reached):")
        for task in schedule.unscheduled_tasks:
            pet_name = task.pet.pet_name if task.pet is not None else "Unknown pet"
            print(
                f"- {task.description} for {pet_name}: "
                f"{task.time_to_complete} min ({task.priority} priority)"
            )


if __name__ == "__main__":
    main()
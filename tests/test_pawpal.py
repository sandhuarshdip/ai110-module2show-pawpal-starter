from pawpal_system import Pet, Task


def test_mark_complete_changes_task_status() -> None:
    task = Task("Feed the pet", 10, "high")

    task.mark_complete()

    assert task.completed is True


def test_adding_task_increases_pet_task_count() -> None:
    pet = Pet("Mochi", "Shiba Inu")
    task = Task("Morning walk", 30, "high")
    initial_task_count = len(pet.tasks)

    pet.add_task(task)

    assert len(pet.tasks) == initial_task_count + 1
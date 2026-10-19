from datetime import date, time, timedelta

import streamlit as st

from pawpal_system import Owner, Pet, Schedule, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption(date.today().strftime("%A, %B %d, %Y"))

st.markdown(
    """
Welcome to the PawPal+ pet care planner. Add pets and care tasks, then generate a schedule
that lists due tasks in priority order for today and tomorrow without assigning times.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

The app connects this interface to the pet care and scheduling logic.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner and pets")
owner_name = st.text_input("Owner name", value="Jordan")
if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_name=owner_name, preference="No preference")

owner = st.session_state.owner
owner.owner_name = owner_name

pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    pet = Pet(pet_name=pet_name, pet_breed=species)
    owner.add_pet(pet)
    st.session_state.pop("schedule", None)

if owner.pets:
    st.write("Your pets:")
    st.write(", ".join(pet.pet_name for pet in owner.pets))
else:
    st.info("Add a pet before creating care tasks.")

st.markdown("### Tasks")
st.caption("Assign each care task to one of your pets.")

if owner.pets:
    selected_pet_index = st.selectbox(
        "Pet for this task",
        range(len(owner.pets)),
        format_func=lambda index: owner.pets[index].pet_name,
    )
    selected_pet = owner.pets[selected_pet_index]
    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input(
            "Duration (minutes)", min_value=1, max_value=240, value=20
        )
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    daily_task = st.checkbox("Daily task")
    set_scheduled_time = st.checkbox("Set a scheduled time")
    scheduled_time = (
        st.time_input("Scheduled time", value=time(8, 0))
        if set_scheduled_time
        else None
    )

    if st.button("Add task"):
        if task_title.strip():
            normalized_task_title = task_title.strip().casefold()
            pending_confirmation = st.session_state.get(
                "pending_duplicate_confirmation"
            )
            is_duplicate = any(
                task.description.strip().casefold() == normalized_task_title
                for task in selected_pet.tasks
            )

            if is_duplicate and pending_confirmation != (
                selected_pet,
                normalized_task_title,
            ):
                st.session_state.pending_duplicate_confirmation = (
                    selected_pet,
                    normalized_task_title,
                )
                st.error(
                    "Duplicate task detected! If not a mistake click Add Task again."
                )
            else:
                selected_pet.add_task(
                    Task(
                        description=task_title,
                        time_to_complete=int(duration),
                        priority=priority,
                        daily=daily_task,
                        scheduled_time=scheduled_time,
                    )
                )
                st.session_state.pop("pending_duplicate_confirmation", None)
                st.session_state.pop("schedule", None)
        else:
            st.error("Enter a task title before adding it.")

tasks = owner.get_all_tasks()
if tasks:
    st.subheader("Task completion")
    incomplete_tasks = owner.filter_tasks(completed=False)
    tasks_due_today = [
        task for task in incomplete_tasks if task.due_date <= date.today()
    ]
    if tasks_due_today:
        selected_task_index = st.selectbox(
            "Task to mark complete",
            range(len(tasks_due_today)),
            format_func=lambda index: (
                f"{tasks_due_today[index].description} — "
                f"{tasks_due_today[index].pet.pet_name if tasks_due_today[index].pet is not None else 'Unassigned'}"
            ),
        )
        task_to_complete = tasks_due_today[selected_task_index]
        if st.button("Mark task complete"):
            task_to_complete.mark_complete()
            st.session_state.schedule = owner.create_schedule()
            st.success(f"Marked “{task_to_complete.description}” complete.")
    elif incomplete_tasks:
        st.info("No tasks are due today. Future daily tasks remain on your list.")
    else:
        st.success("All care tasks are complete.")

    st.write("Current tasks:")
    st.table(
        [
            {
                "Pet": task.pet.pet_name if task.pet is not None else "Unassigned",
                "Task": task.description,
                "Status": "Complete" if task.completed else "Incomplete",
                "Due date": task.due_date.isoformat(),
                "Scheduled time": (
                    task.scheduled_time.strftime("%I:%M %p").lstrip("0")
                    if task.scheduled_time is not None
                    else "Not set"
                ),
                "Duration (minutes)": task.time_to_complete,
                "Priority": task.priority,
                "Daily": "Yes" if task.daily else "No",
            }
            for task in tasks
        ]
    )
else:
    st.info("No tasks yet. Add a pet, then create a task above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Tasks are listed in priority order. Set task times to check for conflicts.")

tasks_to_schedule = [
    task
    for task in owner.get_all_tasks()
    if not task.completed and task.due_date <= date.today() + timedelta(days=1)
]
if st.button("Generate schedule", disabled=not tasks_to_schedule):
    st.session_state.schedule = owner.create_schedule()

schedule: Schedule | None = st.session_state.get("schedule")
if schedule is not None:
    for warning in schedule.get_conflict_warnings():
        st.warning(warning)

    for schedule_date, label in (
        (date.today(), "Today"),
        (date.today() + timedelta(days=1), "Tomorrow"),
    ):
        st.write(f"{label}'s tasks for {owner.owner_name}:")
        scheduled_tasks = [
            task
            for task in schedule.tasks_by_date.get(schedule_date, [])
            if not task.completed
            and (
                task.due_date <= schedule_date
                if schedule_date == date.today()
                else task.due_date == schedule_date
            )
        ]
        if scheduled_tasks:
            st.table(
                [
                    {
                        "Order": index,
                        "Pet": (
                            task.pet.pet_name
                            if task.pet is not None
                            else "Unassigned"
                        ),
                        "Task": task.description,
                        "Duration (minutes)": task.time_to_complete,
                        "Scheduled time": (
                            task.scheduled_time.strftime("%I:%M %p").lstrip("0")
                            if task.scheduled_time is not None
                            else "Not set"
                        ),
                        "Priority": task.priority,
                    }
                    for index, task in enumerate(scheduled_tasks, start=1)
                ]
            )
        else:
            st.info(f"No incomplete tasks due {label.lower()}.")

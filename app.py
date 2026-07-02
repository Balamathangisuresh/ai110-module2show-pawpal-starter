import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
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

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
available_minutes = st.number_input("Available minutes today", min_value=1, max_value=1440, value=120)
if "owner" not in st.session_state:
    st.session_state.owner = Owner(
        name=owner_name,
        available_minutes=int(available_minutes),
    )

st.markdown("### Add a Pet")
col1, col2, col3, col4 = st.columns(4)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with col3:
    breed = st.text_input("Breed", value="Shiba Inu")
with col4:
    age = st.number_input("Age (years)", min_value=0, max_value=30, value=2)

if st.button("Add pet"):
    st.session_state.owner.add_pet(Pet(name=pet_name, species=species, breed=breed, age=int(age)))

if st.session_state.owner.pets:
    st.write("Pets:")
    for pet in st.session_state.owner.pets:
        st.write(f"- {pet.summary()}")
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.markdown("### Add a Task")
if not st.session_state.owner.pets:
    st.info("Add a pet first before adding tasks.")
else:
    pet_names = [pet.name for pet in st.session_state.owner.pets]
    selected_pet_name = st.selectbox("Pet", pet_names)

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
        start_time = st.text_input("Start time (HH:MM)", value="08:00")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        frequency = st.selectbox("Frequency", ["daily", "weekly", "one-time"])
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    if st.button("Add task"):
        selected_pet = next(pet for pet in st.session_state.owner.pets if pet.name == selected_pet_name)
        selected_pet.add_task(
            Task(
                title=task_title,
                duration_minutes=int(duration),
                priority=priority,
                frequency=frequency,
                start_time=start_time,
            )
        )

    any_tasks = any(pet.tasks for pet in st.session_state.owner.pets)
    if any_tasks:
        st.write("Current tasks:")
        for pet in st.session_state.owner.pets:
            for task in pet.tasks:
                st.write(f"- ({pet.name}) {task}")
    else:
        st.info("No tasks yet. Add one above.")

st.divider()

st.subheader(f"Daily Plan for {st.session_state.owner.name}")

if not st.session_state.owner.pets:
    st.info("Add a pet and some tasks first to build today's plan.")
else:
    if st.button("Generate schedule"):
        scheduler = Scheduler(st.session_state.owner)
        scheduler.build_schedule()
        st.session_state.scheduler = scheduler
        st.session_state.conflict_warnings = scheduler.conflict_warnings()

    scheduler = st.session_state.get("scheduler")
    if scheduler is None:
        st.info("Click 'Generate schedule' to build today's plan.")
    else:
        for conflict_warning in st.session_state.get("conflict_warnings", []):
            st.warning(conflict_warning)

        pet_for_task = {
            id(task): pet.name for pet in st.session_state.owner.pets for task in pet.tasks
        }
        priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}

        filter_col1, filter_col2 = st.columns(2)
        with filter_col1:
            pet_filter = st.selectbox(
                "Filter by pet",
                ["All pets"] + [pet.name for pet in st.session_state.owner.pets],
            )
        with filter_col2:
            status_filter = st.radio(
                "Filter by status", ["All", "Pending", "Completed"], horizontal=True
            )

        visible_tasks = [
            task
            for task in scheduler.planned_tasks
            if (pet_filter == "All pets" or pet_for_task[id(task)] == pet_filter)
            and (
                status_filter == "All"
                or task.completed == (status_filter == "Completed")
            )
        ]

        if not visible_tasks:
            st.warning("No tasks match this filter.")
        else:
            header_cols = st.columns([2, 3, 2, 2, 2, 2])
            for col, label in zip(
                header_cols, ["Pet", "Task", "Time", "Duration", "Priority", "Done"]
            ):
                col.markdown(f"**{label}**")

            for task in visible_tasks:
                row = st.columns([2, 3, 2, 2, 2, 2])
                row[0].write(pet_for_task[id(task)])
                row[1].write(task.title)
                row[2].write(task.start_time)
                row[3].write(f"{task.duration_minutes} min")
                row[4].write(f"{priority_emoji.get(task.priority, '')} {task.priority}")
                is_done = row[5].checkbox(
                    "Done",
                    value=task.completed,
                    key=f"done_{id(task)}",
                    label_visibility="collapsed",
                )
                if is_done != task.completed:
                    if is_done:
                        new_task = scheduler.mark_task_complete(task)
                        if new_task is not None:
                            st.toast(f"Next occurrence added: {new_task.title} on {new_task.due_date}")
                    else:
                        task.mark_incomplete()
                    st.rerun()

        if scheduler.skipped_tasks:
            st.warning(
                "Skipped (not enough time): "
                + ", ".join(t.title for t in scheduler.skipped_tasks)
            )

        st.success(f"Total planned time: {scheduler.total_duration()} min")

import pytest
from datetime import date
from pawpal_system import Owner, Pet, Scheduler, Task


def make_task(title="Task", duration_minutes=10, priority="medium", frequency="daily",
              start_time="09:00", completed=False, due_date=None):
    """Build a Task with sensible defaults so tests only spell out what matters."""
    return Task(
        title=title,
        duration_minutes=duration_minutes,
        priority=priority,
        frequency=frequency,
        start_time=start_time,
        completed=completed,
        due_date=due_date if due_date is not None else date(2026, 1, 1),
    )


def make_scheduler(available_minutes, pets_tasks):
    """Build a Scheduler whose owner has one Pet per key in pets_tasks, holding that value's tasks."""
    owner = Owner(name="Owner", available_minutes=available_minutes)
    for pet_name, tasks in pets_tasks.items():
        pet = Pet(name=pet_name, species="dog", breed="mix", age=1)
        for task in tasks:
            pet.add_task(task)
        owner.add_pet(pet)
    return Scheduler(owner)

def test_task_completion():
    """Verify that calling mark_complete() changes the task's completed status to True."""
    # Arrange
    task = Task(
        title="Evening Feeding", 
        duration_minutes=20, 
        priority="Medium", 
        frequency="Daily", 
        start_time="18:30"
    )
    assert task.completed is False  # Initial state check based on UML
    
    # Act
    task.mark_complete()
    
    # Assert
    assert task.completed is True


def test_task_addition_increases_count():
    """Verify that adding a task to a Pet increases that pet's tasks list count."""
    # Arrange
    pet = Pet(name="Buddy", species="Dog", breed="Golden Retriever", age=3)
    task = Task(
        title="Morning Walk", 
        duration_minutes=30, 
        priority="High", 
        frequency="Daily", 
        start_time="08:00"
    )
    
    # Check that it starts with an empty list
    assert len(pet.tasks) == 0
    
    # Act
    pet.add_task(task)
    
    # Assert
    assert len(pet.tasks) == 1
    assert pet.tasks[0] == task


# --- Sorting Correctness ---

def test_sort_by_priority_orders_high_to_low():
    """Verify tasks come back ordered high -> medium -> low priority."""
    high = make_task(title="High", priority="high", start_time="10:00")
    medium = make_task(title="Medium", priority="medium", start_time="09:00")
    low = make_task(title="Low", priority="low", start_time="08:00")
    scheduler = make_scheduler(1000, {"Pet": [low, high, medium]})

    ordered = scheduler._sort_by_priority()

    assert [t.title for t in ordered] == ["High", "Medium", "Low"]


def test_sort_by_priority_ties_broken_by_start_time():
    """Verify same-priority tasks fall back to chronological start-time order."""
    later = make_task(title="Later", priority="high", start_time="15:00")
    earlier = make_task(title="Earlier", priority="high", start_time="07:00")
    scheduler = make_scheduler(1000, {"Pet": [later, earlier]})

    ordered = scheduler._sort_by_priority()

    assert [t.title for t in ordered] == ["Earlier", "Later"]


def test_sort_by_priority_empty_task_list():
    """Verify an owner with no tasks sorts to an empty list without error."""
    scheduler = make_scheduler(1000, {"Pet": []})

    assert scheduler._sort_by_priority() == []


# ---  Recurrence Logic ---

def test_daily_task_completion_creates_next_day_task():
    """Verify completing a daily task spawns a new task due exactly 1 day later."""
    task = make_task(frequency="daily", due_date=date(2026, 1, 1))
    scheduler = make_scheduler(1000, {"Pet": [task]})

    next_task = scheduler.mark_task_complete(task)

    assert task.completed is True
    assert next_task is not None
    assert next_task.completed is False
    assert next_task.due_date == date(2026, 1, 2)
    assert next_task in scheduler.owner.pets[0].tasks


def test_weekly_task_completion_creates_next_week_task():
    """Verify completing a weekly task spawns a new task due exactly 7 days later."""
    task = make_task(frequency="weekly", due_date=date(2026, 1, 1))
    scheduler = make_scheduler(1000, {"Pet": [task]})

    next_task = scheduler.mark_task_complete(task)

    assert next_task.due_date == date(2026, 1, 8)


def test_non_recurring_task_completion_creates_no_new_task():
    """Verify a one-off task's completion returns None and adds nothing new."""
    task = make_task(frequency="once")
    scheduler = make_scheduler(1000, {"Pet": [task]})

    next_task = scheduler.mark_task_complete(task)

    assert next_task is None
    assert task.completed is True
    assert len(scheduler.owner.pets[0].tasks) == 1


def test_recurrence_frequency_is_case_insensitive():
    """Verify a capitalized frequency like 'Daily' still recurs correctly."""
    task = make_task(frequency="Daily", due_date=date(2026, 1, 1))
    scheduler = make_scheduler(1000, {"Pet": [task]})

    next_task = scheduler.mark_task_complete(task)

    assert next_task is not None
    assert next_task.due_date == date(2026, 1, 2)


# --- Conflict Detection ---

def test_check_conflicts_flags_overlapping_same_pet():
    """Verify two overlapping tasks on the same pet are flagged."""
    t1 = make_task(title="Walk", start_time="08:00", duration_minutes=30)
    t2 = make_task(title="Feed", start_time="08:15", duration_minutes=15)
    scheduler = make_scheduler(1000, {"Pet": [t1, t2]})

    assert scheduler.check_conflicts() == [(t1, t2)]


def test_check_conflicts_flags_overlapping_different_pets():
    """Verify overlapping tasks are flagged even when they belong to different pets."""
    t1 = make_task(title="Walk", start_time="08:00", duration_minutes=30)
    t2 = make_task(title="Litter", start_time="08:15", duration_minutes=15)
    scheduler = make_scheduler(1000, {"Dog": [t1], "Cat": [t2]})

    assert scheduler.check_conflicts() == [(t1, t2)]


def test_check_conflicts_exact_same_start_time_flagged():
    """Verify two tasks starting at the identical time are flagged as a conflict."""
    t1 = make_task(title="Walk", start_time="08:00", duration_minutes=20)
    t2 = make_task(title="Feed", start_time="08:00", duration_minutes=10)
    scheduler = make_scheduler(1000, {"Pet": [t1, t2]})

    assert scheduler.check_conflicts() == [(t1, t2)]


def test_check_conflicts_back_to_back_tasks_not_flagged():
    """Verify tasks that only touch at the boundary (one ends when the next starts) don't conflict."""
    t1 = make_task(title="Walk", start_time="08:00", duration_minutes=30)
    t2 = make_task(title="Feed", start_time="08:30", duration_minutes=15)
    scheduler = make_scheduler(1000, {"Pet": [t1, t2]})

    assert scheduler.check_conflicts() == []


def test_check_conflicts_no_tasks_returns_empty():
    """Verify an owner with no tasks has no conflicts."""
    scheduler = make_scheduler(1000, {"Pet": []})

    assert scheduler.check_conflicts() == []


def test_conflict_warnings_message_format():
    """Verify conflict_warnings produces a readable message naming both tasks."""
    t1 = make_task(title="Walk", start_time="08:00", duration_minutes=30)
    t2 = make_task(title="Feed", start_time="08:15", duration_minutes=15)
    scheduler = make_scheduler(1000, {"Pet": [t1, t2]})

    warnings = scheduler.conflict_warnings()

    assert len(warnings) == 1
    assert "Walk" in warnings[0] and "Feed" in warnings[0]


# --- Time-Budget Packing / Skip Logic ---

def test_build_schedule_skips_tasks_that_dont_fit():
    """Verify a task that doesn't fit the remaining budget lands in skipped_tasks."""
    fits = make_task(title="Fits", duration_minutes=30, priority="high")
    skipped = make_task(title="Skipped", duration_minutes=40, priority="low")
    scheduler = make_scheduler(30, {"Pet": [fits, skipped]})

    scheduler.build_schedule()

    assert fits in scheduler.planned_tasks
    assert skipped in scheduler.skipped_tasks


def test_build_schedule_task_exactly_fits_available_minutes():
    """Verify a task whose duration exactly equals the remaining budget is planned, not skipped."""
    task = make_task(duration_minutes=30)
    scheduler = make_scheduler(30, {"Pet": [task]})

    scheduler.build_schedule()

    assert task in scheduler.planned_tasks
    assert scheduler.skipped_tasks == []


def test_build_schedule_restores_available_minutes_after_running():
    """Verify available_minutes is unchanged after build_schedule, so re-running gives the same result."""
    task = make_task(duration_minutes=30)
    scheduler = make_scheduler(50, {"Pet": [task]})

    scheduler.build_schedule()
    scheduler.build_schedule()

    assert scheduler.owner.available_minutes == 50
    assert task in scheduler.planned_tasks


def test_build_schedule_completed_task_does_not_consume_budget():
    """Verify an already-completed task is kept in the plan without competing for time."""
    completed_task = make_task(duration_minutes=100, completed=True)
    pending_task = make_task(duration_minutes=20, priority="high")
    scheduler = make_scheduler(20, {"Pet": [completed_task, pending_task]})

    scheduler.build_schedule()

    assert completed_task in scheduler.planned_tasks
    assert pending_task in scheduler.planned_tasks
    assert scheduler.skipped_tasks == []


def test_build_schedule_no_tasks_produces_empty_plan():
    """Verify a pet with no tasks results in an empty plan with zero total duration."""
    scheduler = make_scheduler(60, {"Pet": []})

    scheduler.build_schedule()

    assert scheduler.planned_tasks == []
    assert scheduler.skipped_tasks == []
    assert scheduler.total_duration() == 0


# --- Priority String Handling ---

def test_priority_score_lowercase_values():
    """Verify lowercase priority strings map to the expected numeric scores."""
    assert make_task(priority="high").priority_score() == 3
    assert make_task(priority="medium").priority_score() == 2
    assert make_task(priority="low").priority_score() == 1


def test_priority_score_unknown_or_capitalized_defaults_to_zero():
    """Document current behavior: capitalized or unrecognized priorities silently score as unknown (0)."""
    assert make_task(priority="High").priority_score() == 0
    assert make_task(priority="urgent").priority_score() == 0
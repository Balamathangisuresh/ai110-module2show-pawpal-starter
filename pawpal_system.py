from dataclasses import dataclass, field
from datetime import date, timedelta

_RECURRENCE_STEP = {
    "daily": timedelta(days=1),
    "weekly": timedelta(weeks=1),
}


def _time_to_minutes(time_str: str) -> int:
    """Convert a 'HH:MM' string to total minutes since midnight."""
    h, m = map(int, time_str.split(":"))
    return h * 60 + m


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str
    frequency: str
    start_time: str
    completed: bool = False
    due_date: date = field(default_factory=date.today)

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def mark_incomplete(self) -> None:
        """Mark this task as not completed."""
        self.completed = False

    def next_occurrence(self) -> "Task | None":
        """Return a fresh Task for the next due date if this task recurs, else None."""
        step = _RECURRENCE_STEP.get(self.frequency.lower())
        if step is None:
            return None
        return Task(
            title=self.title,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            frequency=self.frequency,
            start_time=self.start_time,
            due_date=self.due_date + step,
        )

    def priority_score(self) -> int:
        """Return a numeric score for priority (high=3, medium=2, low=1, unknown=0)."""
        return {"low": 1, "medium": 2, "high": 3}.get(self.priority, 0)

    def __repr__(self) -> str:
        """Return a readable string showing task details and completion status."""
        status = "[done]" if self.completed else "[pending]"
        return f"{self.title} ({self.start_time}, {self.duration_minutes} min, {self.priority}) {status}"


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def summary(self) -> str:
        """Return a short description of the pet."""
        return f"{self.name} ({self.breed}, {self.age} yrs)"

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, title: str) -> None:
        """Remove all tasks matching the given title from this pet's task list."""
        self.tasks = [t for t in self.tasks if t.title != title]


@dataclass
class Owner:
    name: str
    available_minutes: int
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def has_time_for(self, task: Task) -> bool:
        """Return True if the task duration fits within remaining available minutes."""
        return task.duration_minutes <= self.available_minutes


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.planned_tasks: list[Task] = []
        self.skipped_tasks: list[Task] = []

    def mark_task_complete(self, task: Task) -> Task | None:
        """Mark a task complete, spawning its next occurrence on the same pet if it recurs.

        Returns the newly created Task, or None if the task doesn't recur.
        """
        task.mark_complete()
        next_task = task.next_occurrence()
        if next_task is not None:
            for pet in self.owner.pets:
                if any(t is task for t in pet.tasks):
                    pet.add_task(next_task)
                    break
        return next_task

    def _sort_by_priority(self) -> list[Task]:
        """Sort all of the owner's tasks by priority, descending, breaking ties by start time.

        Algorithm: collects every task across all pets into one flat list, then does a single
        sort keyed on (-priority_score, start_time_in_minutes). Sorting on a negated score puts
        "high" before "medium" before "low"; the start-time tiebreaker keeps same-priority tasks
        in chronological order. Runs in O(n log n) for n total tasks.

        Returns:
            list[Task]: every task owned by the owner's pets, priority-first.
        """
        all_tasks = [task for pet in self.owner.pets for task in pet.tasks]
        return sorted(all_tasks, key=lambda t: (-t.priority_score(), _time_to_minutes(t.start_time)))

    def build_schedule(self) -> None:
        """Greedily pack today's tasks into the owner's available time budget, by priority.

        Algorithm: walks tasks in priority order (see _sort_by_priority) and, for each one,
        greedily accepts it into planned_tasks if it still fits in the remaining minutes,
        otherwise sends it to skipped_tasks. This is a greedy 0/1 knapsack approximation, not an
        optimal packing: it maximizes for "highest priority always wins" rather than "use as many
        minutes as possible," so a single expensive high-priority task can bump several cheaper
        lower-priority tasks that would otherwise have fit. Runs in O(n log n), dominated by the sort.

        Already-completed tasks are kept in the plan for reference but don't compete for time,
        since that time was already spent in a prior pass. Mutates self.planned_tasks and
        self.skipped_tasks; leaves self.owner.available_minutes unchanged on exit.
        """
        self.planned_tasks = []
        self.skipped_tasks = []
        original_minutes = self.owner.available_minutes
        for task in self._sort_by_priority():
            if task.completed:
                self.planned_tasks.append(task)
            elif self.owner.has_time_for(task):
                self.planned_tasks.append(task)
                self.owner.available_minutes -= task.duration_minutes
            else:
                self.skipped_tasks.append(task)
        self.owner.available_minutes = original_minutes
        self.planned_tasks.sort(key=lambda t: _time_to_minutes(t.start_time))
        self.skipped_tasks.sort(key=lambda t: _time_to_minutes(t.start_time))

    def check_conflicts(self) -> list[tuple]:
        """Find every pair of tasks whose time windows overlap, same pet or different pets.

        Algorithm: brute-force pairwise comparison over all tasks. For each unique pair (t1, t2),
        converts both start times to minutes-since-midnight, computes each task's end time as
        start + duration, and flags a conflict when the two intervals overlap
        (s1 < e2 and s2 < e1). This is O(n^2) for n total tasks.

        Returns:
            list[tuple[Task, Task]]: each overlapping pair, in the order they were compared.
        """
        all_tasks = [task for pet in self.owner.pets for task in pet.tasks]
        conflicts = []
        for i, t1 in enumerate(all_tasks):
            for t2 in all_tasks[i + 1:]:
                s1 = _time_to_minutes(t1.start_time)
                e1 = s1 + t1.duration_minutes
                s2 = _time_to_minutes(t2.start_time)
                e2 = s2 + t2.duration_minutes
                if s1 < e2 and s2 < e1:
                    conflicts.append((t1, t2))
        return conflicts

    def conflict_warnings(self) -> list[str]:
        """Return a plain-text warning per overlapping task pair, or an empty list if there are none.

        Wraps check_conflicts() so callers (CLI, UI) get a ready-to-display message instead of
        having to compute/format overlaps themselves.
        """
        return [
            f"Warning: '{t1.title}' ({t1.start_time}, {t1.duration_minutes} min) "
            f"overlaps '{t2.title}' ({t2.start_time}, {t2.duration_minutes} min)"
            for t1, t2 in self.check_conflicts()
        ]

    def filter_tasks(self, status: bool = None, pet_name: str = None) -> list[Task]:
        """Return tasks filtered by completion status and/or pet name."""
        result = []
        for pet in self.owner.pets:
            if pet_name is not None and pet.name != pet_name:
                continue
            for task in pet.tasks:
                if status is not None and task.completed != status:
                    continue
                result.append(task)
        return result

    def total_duration(self) -> int:
        """Return the total minutes still drawn from today's time budget (excludes already-completed tasks)."""
        return sum(t.duration_minutes for t in self.planned_tasks if not t.completed)

    def display(self) -> str:
        """Return a formatted string of the daily plan grouped by pet."""
        lines = [f"Daily plan for {self.owner.name}:"]
        for pet in self.owner.pets:
            pet_task_ids = {id(t) for t in pet.tasks}
            pet_planned = [t for t in self.planned_tasks if id(t) in pet_task_ids]
            if pet_planned:
                lines.append(f"\n  {pet.summary()}:")
                for task in pet_planned:
                    lines.append(f"    - {task}")
        if self.skipped_tasks:
            lines.append("\n  Skipped (not enough time):")
            for task in self.skipped_tasks:
                lines.append(f"    - {task}")
        lines.append(f"\n  Total time: {self.total_duration()} min")
        return "\n".join(lines)

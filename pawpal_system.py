from dataclasses import dataclass, field


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

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

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
    preferred_start_time: str
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

    def _sort_tasks(self) -> list[Task]:
        """Collect all tasks from all pets and sort them chronologically by start time."""
        all_tasks = [task for pet in self.owner.pets for task in pet.tasks]
        return sorted(all_tasks, key=lambda t: _time_to_minutes(t.start_time))

    def build_schedule(self) -> None:
        """Populate planned_tasks and skipped_tasks based on available time."""
        self.planned_tasks = []
        self.skipped_tasks = []
        for task in self._sort_tasks():
            if self.owner.has_time_for(task):
                self.planned_tasks.append(task)
                self.owner.available_minutes -= task.duration_minutes
            else:
                self.skipped_tasks.append(task)

    def check_conflicts(self) -> list[tuple]:
        """Return pairs of tasks whose time windows overlap across all pets."""
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
        """Return the total duration in minutes of all planned tasks."""
        return sum(t.duration_minutes for t in self.planned_tasks)

    def display(self) -> str:
        """Return a formatted string of the daily plan grouped by pet."""
        lines = [f"Daily plan for {self.owner.name}:"]
        planned_ids = {id(t) for t in self.planned_tasks}
        for pet in self.owner.pets:
            pet_planned = [t for t in pet.tasks if id(t) in planned_ids]
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

# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```
    Daily plan for Bala:

    Mochi (cat, 3 yrs):
        - Feed Mochi (10 min, high) [pending]
        - Clean litter box (15 min, medium) [pending]
        - Playtime (20 min, low) [pending]

    Biscuit (dog, 5 yrs):
        - Morning walk (30 min, high) [pending]
        - Give meds (5 min, high) [pending]
        - Feed Biscuit (10 min, high) [pending]

    Skipped (not enough time):
        - Grooming (45 min, low) [pending]

    Total time: 90 min

## 🧪 Testing PawPal+

command to run tests: python -m pytest

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Description:
    Sorting Correctness: tasks sort high to medium to low priority, same-priority tasks tie-break by start time, an empty task list sorts to [] without error.

    Recurrence Logic — completing a "daily" task spawns a new one due +1 day, "weekly" spawns one due +7 days, a non-recurring frequency ("once") returns None and adds nothing, frequency matching is case-insensitive ("Daily" still works).

    Conflict Detection: overlapping tasks are flagged whether on the same pet or different pets, identical start times are flagged, back-to-back tasks that only touch at the boundary are not flagged, no tasks means no conflicts, conflict_warnings() produces a readable message naming both tasks.

    Time-Budget Packing/Skip Logic: tasks that don't fit the remaining budget go to skipped_tasks, a task whose duration exactly equals the remaining budget still fits, available_minutes is restored after build_schedule(), an already-completed task stays planned without consuming budget, no tasks produces an empty plan with zero total duration.

    Priority String Case Sensitivity: lowercase "high"/"medium"/"low" score 3/2/1, capitalized ("High") or unrecognized ("urgent") values score 0.



Sample test output:

```
# Paste your pytest output here
    ========================================= test session starts =========================================
    platform win32 -- Python 3.14.5, pytest-9.1.1, pluggy-1.6.0
    rootdir: D:\Classes\Summer_2_2026\ai110-module2show-pawpal-starter
    plugins: anyio-4.13.0
    collected 22 items                                                                                     

    tests\test_pawpal.py ......................                                                      [100%]

    ========================================= 22 passed in 0.10s ==========================================
```
Confidence Level: 5 stars because it passed all of the tests.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler._sort_by_priority()`, `Scheduler.build_schedule()` | Sorts by priority (high → low), ties are broken by start time, greedily fits tasks into `available_minutes` |
| Filtering | `Scheduler.filter_tasks(status, pet_name)` | Filters tasks by completion status, pet name, or both |
| Conflict handling | `Scheduler.check_conflicts()`, `Scheduler.conflict_warnings()` | Flags overlapping time windows (same or different pet), returns warning strings |
| Recurring tasks | `Task.next_occurrence()`, `Scheduler.mark_task_complete()` | Uses `timedelta` to compute the next due date (`+1 day` daily, `+7 days` weekly), task is auto-added on completion. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->

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
Confidence Level: 4 stars because it passed all of the tests I wrote which covers a good amount (both happy cases and edge cases), however my tests doesn't test all of the methods and all of the scenarios.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler._sort_by_priority()`, `Scheduler.build_schedule()` | Sorts by priority (high → low), ties are broken by start time, greedily fits tasks into `available_minutes` |
| Filtering | `Scheduler.filter_tasks(status, pet_name)` | Filters tasks by completion status, pet name, or both |
| Conflict handling | `Scheduler.check_conflicts()`, `Scheduler.conflict_warnings()` | Flags overlapping time windows (same or different pet), returns warning strings |
| Recurring tasks | `Task.next_occurrence()`, `Scheduler.mark_task_complete()` | Uses `timedelta` to compute the next due date (`+1 day` daily, `+7 days` weekly), task is auto-added on completion. |

## 📸 Demo Walkthrough

### Streamlit UI features

- Enter the owner's name and available minutes for the day
- Add a pet (name, species, breed, age)
- Add a task to a chosen pet (title, start time, duration, frequency, priority)
- Generate today's schedule with one click
- Filter the generated plan by pet and by status (All / Pending / Completed)
- Check a task's "Done" box to mark it complete (unchecking marks it incomplete again)
- See skipped tasks and the total planned time at a glance

### Example workflow

1. Enter an owner name and available minutes (e.g., "Bala", 90 minutes).
2. Add a pet (e.g., "Mochi" (cat, Siamese, 3 yrs)) with the **Add a Pet** button.
3. Add that pet's tasks with the **Add a Task** form  (e.g., "Feed Mochi" at 08:00 (10 min, high, daily), "Playtime" at 10:00 (20 min, low, daily). Repeat for a second pet, e.g. "Biscuit" with a "Morning walk" at 08:00 (30 min, high, daily)).
4. Click **Generate schedule**. Any overlapping tasks (like two tasks both starting at 10:00) surface immediately as warning banners.
5. Use the pet/status filters above the plan table to narrow what's shown.
6. Check a recurring task's "Done" box, it's marked complete and confirms its next occurrence (tomorrow for daily, +7 days for weekly) was automatically added.
7. Anything that didn't fit today's available minutes appears in a "Skipped (not enough time)" banner, and the running **Total planned time** is shown at the bottom.

### Key Scheduler behaviors shown

- **Sorting** — the plan always lists tasks high → medium → low priority, with same-priority tasks ordered by start time.
- **Conflict warnings** — two tasks with overlapping time windows (same pet or different pets) are flagged before/alongside the plan.
- **Time-budget packing** — tasks that don't fit the owner's `available_minutes` are pushed to a skipped list instead of silently dropped.
- **Recurrence** — completing a daily/weekly task automatically spawns its next occurrence on the correct future date.
- **Filtering** — the same task pool can be viewed by pet, by completion status, or both.

### Sample CLI output (`python main.py`)

`main.py` seeds two pets with mixed priorities, start times, and an intentional same-time conflict, then walks through conflict checking, scheduling, filtering, and completing a recurring task:

```
=== Conflict Check ===
  Warning: 'Playtime' (10:00, 20 min) overlaps 'Brush fur' (10:00, 10 min)
  Warning: 'Feed Mochi' (08:00, 10 min) overlaps 'Morning walk' (08:00, 30 min)

=== Schedule ===
Daily plan for Bala:

  Mochi (Siamese, 3 yrs):
    - Feed Mochi (08:00, 10 min, high) [pending]
    - Clean litter box (09:00, 15 min, medium) [pending]
    - Playtime (10:00, 20 min, low) [pending]

  Biscuit (Golden Retriever, 5 yrs):
    - Morning walk (08:00, 30 min, high) [pending]
    - Feed Biscuit (08:30, 10 min, high) [pending]
    - Give meds (09:30, 5 min, high) [pending]

  Skipped (not enough time):
    - Brush fur (10:00, 10 min, low) [pending]
    - Grooming (11:00, 45 min, low) [pending]

  Total time: 90 min

=== Pending Tasks ===
  Playtime (10:00, 20 min, low) [pending]
  Feed Mochi (08:00, 10 min, high) [pending]
  Clean litter box (09:00, 15 min, medium) [pending]
  Brush fur (10:00, 10 min, low) [pending]
  Grooming (11:00, 45 min, low) [pending]
  Give meds (09:30, 5 min, high) [pending]
  Morning walk (08:00, 30 min, high) [pending]
  Feed Biscuit (08:30, 10 min, high) [pending]

=== Mochi's Tasks ===
  Playtime (10:00, 20 min, low) [pending]
  Feed Mochi (08:00, 10 min, high) [pending]
  Clean litter box (09:00, 15 min, medium) [pending]
  Brush fur (10:00, 10 min, low) [pending]

=== Completed Tasks ===
  Feed Mochi (08:00, 10 min, high) [done]

  Next occurrence spawned: Feed Mochi due 2026-07-03

=== Schedule After Completion ===
Daily plan for Bala:

  Mochi (Siamese, 3 yrs):
    - Feed Mochi (08:00, 10 min, high) [done]
    - Feed Mochi (08:00, 10 min, high) [pending]
    - Clean litter box (09:00, 15 min, medium) [pending]
    - Playtime (10:00, 20 min, low) [pending]

  Biscuit (Golden Retriever, 5 yrs):
    - Morning walk (08:00, 30 min, high) [pending]
    - Feed Biscuit (08:30, 10 min, high) [pending]
    - Give meds (09:30, 5 min, high) [pending]

  Skipped (not enough time):
    - Brush fur (10:00, 10 min, low) [pending]
    - Grooming (11:00, 45 min, low) [pending]

  Total time: 90 min

  Total planned time: 90 / 90 min available
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->

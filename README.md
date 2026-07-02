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

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

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

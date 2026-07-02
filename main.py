from pawpal_system import Task, Pet, Owner, Scheduler

# --- Setup pets ---
mochi = Pet(name="Mochi", species="cat", breed="Siamese", age=3)
biscuit = Pet(name="Biscuit", species="dog", breed="Golden Retriever", age=5)

# --- Setup owner and add pets ---
owner = Owner(name="Bala", available_minutes=90)
owner.add_pet(mochi)
owner.add_pet(biscuit)

# --- Add tasks out of order (mixed priorities, mixed start times, pets interleaved) ---
# so build_schedule() and filter_tasks() are proven to sort/filter correctly
# regardless of insertion order, not just when data already happens to be tidy.
mochi.add_task(Task("Playtime",         20, "low",    "daily",  "10:00"))
biscuit.add_task(Task("Grooming",       45, "low",    "weekly", "11:00"))
mochi.add_task(Task("Feed Mochi",       10, "high",   "daily",  "08:00"))
biscuit.add_task(Task("Give meds",       5, "high",   "daily",  "09:30"))
mochi.add_task(Task("Clean litter box", 15, "medium", "daily",  "09:00"))
biscuit.add_task(Task("Morning walk",   30, "high",   "daily",  "08:00"))
biscuit.add_task(Task("Feed Biscuit",   10, "high",   "daily",  "08:30"))
# Same-pet conflict: Mochi can't do two things at once at 10:00.
mochi.add_task(Task("Brush fur",        10, "low",    "daily",  "10:00"))

scheduler = Scheduler(owner)

# --- Check for conflicts before scheduling (cross-pet AND same-pet overlaps) ---
print("=== Conflict Check ===")
warnings = scheduler.conflict_warnings()
if warnings:
    for warning in warnings:
        print(f"  {warning}")
else:
    print("  No conflicts found.")

# --- Build and display schedule ---
print("\n=== Schedule ===")
scheduler.build_schedule()
print(scheduler.display())

# --- Filter: pending tasks only ---
print("\n=== Pending Tasks ===")
for task in scheduler.filter_tasks(status=False):
    print(f"  {task}")

# --- Filter: tasks for a specific pet ---
print("\n=== Mochi's Tasks ===")
for task in scheduler.filter_tasks(pet_name="Mochi"):
    print(f"  {task}")

# --- Mark a task complete (spawns its next occurrence) and filter done tasks ---
feed_mochi = next(t for t in mochi.tasks if t.title == "Feed Mochi")
next_occurrence = scheduler.mark_task_complete(feed_mochi)
print("\n=== Completed Tasks ===")
for task in scheduler.filter_tasks(status=True):
    print(f"  {task}")
if next_occurrence:
    print(f"\n  Next occurrence spawned: {next_occurrence.title} due {next_occurrence.due_date}")

# --- Rebuild: completed tasks stay visible but no longer eat the time budget ---
print("\n=== Schedule After Completion ===")
scheduler.build_schedule()
print(scheduler.display())
print(f"\n  Total planned time: {scheduler.total_duration()} / {owner.available_minutes} min available")

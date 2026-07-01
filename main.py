from pawpal_system import Task, Pet, Owner, Scheduler

# --- Setup pets ---
mochi = Pet(name="Mochi", species="cat", breed="Siamese", age=3)
biscuit = Pet(name="Biscuit", species="dog", breed="Golden Retriever", age=5)

# --- Setup owner and add pets ---
owner = Owner(name="Bala", available_minutes=90, preferred_start_time="08:00")
owner.add_pet(mochi)
owner.add_pet(biscuit)

# --- Add tasks directly to pets ---
mochi.add_task(Task("Feed Mochi",      10, "high",   "daily",  "08:00"))
mochi.add_task(Task("Clean litter box",15, "medium", "daily",  "09:00"))
mochi.add_task(Task("Playtime",        20, "low",    "daily",  "10:00"))

biscuit.add_task(Task("Morning walk",  30, "high",   "daily",  "08:00"))
biscuit.add_task(Task("Give meds",      5, "high",   "daily",  "09:30"))
biscuit.add_task(Task("Feed Biscuit",  10, "high",   "daily",  "08:30"))
biscuit.add_task(Task("Grooming",      45, "low",    "weekly", "11:00"))

scheduler = Scheduler(owner)

# --- Check for conflicts before scheduling ---
print("=== Conflict Check ===")
conflicts = scheduler.check_conflicts()
if conflicts:
    for t1, t2 in conflicts:
        print(f"  CONFLICT: '{t1.title}' and '{t2.title}' overlap at {t1.start_time}")
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

# --- Mark a task complete and filter done tasks ---
mochi.tasks[0].mark_complete()
print("\n=== Completed Tasks ===")
for task in scheduler.filter_tasks(status=True):
    print(f"  {task}")

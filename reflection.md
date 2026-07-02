# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

    PetTask - a single activity/task for a pet. It holds the task name, how long it takes, its priority level, and how often it repeats. Can convert its priority label into a numeric score (used for sorting) and display itself as a string.

    Pet - the actual animal. it holds basic identity info (name, species, age) and is can produce a summary of itself as a string.

    Owner - stores information about the person using the app like their name, how much time they have today, and when they want to start. Its method, has_time_for(task), checks whether a given task fits within the owner's remaining time.

    Scheduler - the engine of the system. It holds a reference to both the Pet and the Owner (so it knows who is being cared for and what constraints apply), and three task lists: tasks (all candidate tasks), planned_tasks (tasks that made the cut), and skipped_tasks (tasks that didn't fit). Its responsibilities are to manage the task pool using the methods add_task() and remove_task(), building the schedule using the build_schedule() method which sorts tasks by priority and checks each one against owner.has_time_for() and populates planned_tasks and skipped_tasks, and gives the output using display() metod.


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

    Yes, when brainstorming the uml, Claude recommended 5 different classes which split the now Scheduler class into two seperate classes. This seemed unnecessary and exceeded the number of classes so I asked Claude to move some attributes which it moved to Scheduler class.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

    My scheduler considers time using the Owner's available minutes and priority to fit the highest priority tasks first.

    I decided on using time and priority as the most improtant constraints because they felt non-negotiable as an owner cannot exceed the amount of time they have, and missing a high-priority task like taking meds for a lower priority task like playtime has a huge impact on the pet's health.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

    Scheduler uses a greedy algorithm by sorting by priority first, then start time to fill up an owner's available minutes. One trade off for this algorithm is always do the high-priotity tasks and not fit as many tasks as you can into the available minutes.

    This is reasonable for this scenario because it reflects real consequences for a pet's health. An owner would rather choose to feed and take the pets on regular walks and see playtime get skipped rather than skipping high priority tasks just to get more tasks done. So trading time-efficiency for a guarantee that important tasks always come first matches how a pet owner would actually want their day prioritized.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

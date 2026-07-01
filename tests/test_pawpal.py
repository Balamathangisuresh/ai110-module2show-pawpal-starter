import pytest
from pawpal_system import Pet, Task

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
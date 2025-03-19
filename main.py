import heapq  # We use heapq because it provides an efficient way to manage a priority queue (Min-Heap).
from datetime import datetime  # Used to handle deadlines properly.

class JobApplication:
    """Represents a job application with priority based on deadline & importance."""

    VALID_STATUSES = {"Pending", "Processed", "Interviewing", "Rejected"}  # Set of valid statuses.

    def __init__(self, company, position, deadline, importance):
        """
        Initializes a new job application.
        - company: Name of the company.
        - position: Job title.
        - deadline: Application deadline (YYYY-MM-DD format).
        - importance: Importance level (higher number = more important).
        """
        self.company = company
        self.position = position
        try:
            self.deadline = datetime.strptime(deadline, "%Y-%m-%d")  # Converts string to a date object for comparison.
        except ValueError:
            raise ValueError("Deadline must be in YYYY-MM-DD format.")
        if importance <= 0:
            raise ValueError("Importance must be a positive integer.")
        self.importance = importance  # Higher value = more important.
        self.status = "Pending"  # Default status is "Pending".

    def __lt__(self, other):
        """
        Custom sorting logic for the heap.
        - If two applications have the same importance, the one with the sooner deadline comes first.
        - Otherwise, the one with higher importance comes first.
        """
        if self.importance == other.importance:
            return self.deadline < other.deadline  # Earlier deadline gets higher priority.
        return self.importance > other.importance  # Higher importance gets higher priority.


class JobTracker:
    """Manages job applications using a Min-Heap for priority-based scheduling."""

    def __init__(self):
        """Initializes an empty job tracker with a heap and a hash table."""
        self.job_heap = []  # Heap (priority queue) storing applications.
        self.jobs = {}  # Hash table (dictionary) for quick lookup of applications.

    def add_application(self, company, position, deadline, importance):
        """
        Adds a new job application to the tracker.
        - The heap ensures that the most urgent applications are processed first.
        - The hash table allows fast lookup and management.
        """
        try:
            job = JobApplication(company, position, deadline, importance)  # Create a new job object.
            heapq.heappush(self.job_heap, job)  # Push the job into the heap, maintaining priority order.
            self.jobs[(company, position)] = job  # Store in the hash table for easy access.
            print(f"Added: {company} - {position} (Deadline: {deadline}, Importance: {importance})")
        except ValueError as e:
            print(f"Error: {e}")

    def process_next_application(self):
        """
        Removes and processes the highest-priority job application.
        - The job with the highest importance and earliest deadline will be processed first.
        - Once processed, it is removed from both the heap and the hash table.
        """
        if not self.job_heap:
            print("No pending applications.")
            return None

        job = heapq.heappop(self.job_heap)  # Get the most important job from the heap.
        job.status = "Processed"  # Mark as processed.
        del self.jobs[(job.company, job.position)]  # Remove from the hash table.
        print(f"Processing: {job.company} - {job.position} (Deadline: {job.deadline.date()}, Importance: {job.importance})")
        return job

    def view_pending_applications(self):
        """
        Displays all pending applications sorted by priority.
        - The heap itself does not store elements in sorted order, so we create a sorted list for display.
        """
        if not self.job_heap:
            print("No pending applications.")
            return

        print("\nPending Applications (sorted by priority):")
        for job in sorted(self.job_heap):  # Sort the heap without modifying it.
            print(f"{job.company} - {job.position} | Deadline: {job.deadline.date()} | Importance: {job.importance} | Status: {job.status}")

    def update_status(self, company, position, new_status):
        """
        Updates the status of an existing job application.
        - This does not change the application's priority in the heap.
        """
        if (company, position) not in self.jobs:
            print(f"Application for {company} - {position} not found.")
            return
        if new_status not in JobApplication.VALID_STATUSES:
            print(f"Error: Invalid status. Valid statuses are {JobApplication.VALID_STATUSES}.")
            return

        self.jobs[(company, position)].status = new_status  # Update status in the hash table.
        print(f"Updated: {company} - {position} to '{new_status}'")

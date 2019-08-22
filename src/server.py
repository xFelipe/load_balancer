from src.task import Task
from src.constants import TTASK_LIMITS, UMAX_LIMITS


class Server:
    def __init__(self, ttask, umax):
        """Check limits and start vars"""
        assert TTASK_LIMITS[0] <= ttask <= TTASK_LIMITS[1],\
            'ttask value must be between {} and {}. Value found: {}'.format(TTASK_LIMITS[0], TTASK_LIMITS[1], ttask)
        assert UMAX_LIMITS[0] <= umax <= UMAX_LIMITS[1],\
            'umax value must be between {} and {}. Value found: {}'.format(TTASK_LIMITS[0], TTASK_LIMITS[1], umax)
        self.ttask = ttask
        self.umax = umax
        self.task_list = []
    
    def add_task(self):
        """Create a task on this server"""
        if len(self.task_list) < self.umax:
            self.task_list.append(Task(self.ttask))
        else:
            raise Exception('Maximum number of tasks({}) exceeded.'.format(self.umax))
    
    def is_working(self):
        """Informs if there are any tasks running on the server."""
        return len(self.task_list) > 0
    
    def clock(self):
        """Runs clock on each task and removes finished tasks."""
        for task in self.task_list:
            task.clock()
        
        self.task_list = [ task for task in self.task_list if task.is_alive() ]

    def available_slots(self):
        """Returns the amount of slots available for new tasks."""
        return self.umax - len(self.task_list)

    def stats(self):
        """Shows the status of each task in this server."""
        return [task.missing_ttask for task in self.task_list]
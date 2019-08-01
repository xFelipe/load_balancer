from task import Task


TTASK_LIMITS = (1, 10)
UMAX_LIMITS = (1, 10)


class Server:
    def __init__(self, ttask, umax):
        assert TTASK_LIMITS[0] <= ttask <= TTASK_LIMITS[1], 'ttask value must be between 1 and 10. Value found: {}'.format(ttask)
        assert UMAX_LIMITS[0] <= umax <= UMAX_LIMITS[1], 'umax value must be between 1 and 10. Value found: {}'.format(umax)
        self.ttask = ttask
        self.umax = umax
        self.task_list = []
    
    def add_task(self):
        if len(self.task_list) < self.umax:
            self.task_list.append(Task(self.ttask))
        else:
            raise Exception('Maximum number of tasks({}) exceeded.'.format(self.umax))
    
    def is_working(self):
        return len(self.task_list) > 0
    
    def clock(self):
        for task in self.task_list:
            assert task.modified == False
        
        for task in self.task_list:
            print(' ', task.missing_ttask)
            task.clock()
        
        for task in self.task_list:
            assert task.modified == True
        
        while True in [task.modified for task in self.task_list]:
            for task in self.task_list:
                if not task.is_alive():
                    self.task_list.remove(task)

    def available_slots(self):
        return self.umax - len(self.task_list)

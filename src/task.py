class Task:
    def __init__(self, ttask):
        """Define missing task time"""
        self.missing_ttask = int(ttask)
    
    def clock(self, clock_time=1):
        """Reduce missing task time"""
        self.missing_ttask -= clock_time
        
        if self.missing_ttask < 0:
            self.missing_ttask = 0
    
    def is_alive(self):
        """Informs if this task is running"""
        return self.missing_ttask > 0

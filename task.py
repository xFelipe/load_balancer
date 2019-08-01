class Task:
    def __init__(self, ttask):
        self.missing_ttask = int(ttask)
        self.modified = False
    
    def clock(self, clock_time=1):
        assert self.missing_ttask > 0, "Finished tasks can't run."
        self.missing_ttask -= clock_time
        self.modified = True
        
        if self.missing_ttask < 0:
            self.missing_ttask = 0
            
        return self.missing_ttask
    
    def is_alive(self):
        self.modified = False
        return self.missing_ttask > 0

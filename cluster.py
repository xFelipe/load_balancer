from server import Server
from math import ceil


class Cluster:
    def __init__(self, ttask, umax):
        self.servers_list = []
        self.ttask = ttask
        self.umax = umax

    def add_server(self, numbers_of_new_servers=1):
        for i in range(numbers_of_new_servers):
            self.servers_list.append(Server(self.ttask, self.umax))

    def add_task(self, number_of_tasks):
        current_slots = sum(map(lambda server: server.available_slots(), self.servers_list))
        missing_slots = number_of_tasks - current_slots
        servers_missing = ceil(missing_slots / self.umax)
        if servers_missing > 0:
            for i in range(servers_missing):
                self.servers_list.append(Server(self.ttask, self.umax))

        for server in self.servers_list:
            while server.available_slots() and number_of_tasks:
                server.add_task()
                number_of_tasks -= 1

    ## IMPLEMENTAR CLOCK
from server import Server
from math import ceil

TICK_VALUE = 1.


def allocate_users(unallocated_users, server_list, ttask, umax):
    current_slots = sum(map(lambda server: server.available_slots(), server_list))
    missing_slots = unallocated_users - current_slots
    servers_missing = ceil(missing_slots / umax)
    if servers_missing > 0:
        for i in range(servers_missing):
            server_list.append(Server(ttask, umax))

    for server in server_list:
        while server.available_slots() and unallocated_users:
            server.add_task()
            unallocated_users -= 1


def text_numbers_to_tuple(text):
    chars = text.split()
    numbers = map(lambda char: int(char), chars)
    return tuple(numbers)


if __name__ == '__main__':
    file = open('input')
    _input = text_numbers_to_tuple(file.read())
    ttask, umax, users_per_tick = _input[0], _input[1], _input[2:]
    
    cost = 0.
    server_list = []
    
    for users in users_per_tick:
        print('--', users, '--')
        if users > 0:
            allocate_users(users, server_list, ttask, umax)
        for server in server_list:
            
            cost += TICK_VALUE
            server.clock()
            print(len(server.task_list))
            if not server.is_working():
                server_list.remove(server)
        print('\n')
    print('----------------------\n')
    
    while server_list:
        for server in server_list:
            cost += TICK_VALUE
            print(len(server.task_list), ' ')
            server.clock()
            if not server.is_working():
                server_list.remove(server)
        print('\n')
    print(cost)
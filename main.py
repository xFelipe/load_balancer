from server import Server
from math import ceil

TICK_VALUE = 1.


#def allocate_users(unallocated_users, server_list, ttask, umax):

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
    result = []
    
    for users in users_per_tick:
        if users > 0:
            allocate_users(users, server_list, ttask, umax)
        for server in server_list:
            cost += TICK_VALUE
            server.clock()
            if not server.is_working():
                server_list.remove(server)
    
    while server_list:
        for server in server_list:
            cost += TICK_VALUE
            server.clock()
            if not server.is_working():
                server_list.remove(server)
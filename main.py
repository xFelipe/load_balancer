import sys
from src.cluster import Cluster
from src.constants import TICK_VALUE


def text_numbers_to_tuple(text):
    """Transforms text numbers in int numbers in a tuple"""
    chars = text.split()
    numbers = map(lambda char: int(char), chars)
    return tuple(numbers)


def custom_joiner(list, final):
    """Transforms list in text to write file."""
    log_list = [[str(len(j)) for j in i] for i in list]
    list_of_texts = [','.join(log) for log in log_list]
    list_of_texts.append(str(final))
    text = '\n'.join(list_of_texts)
    return text


def cluster_runner(cluster, users_per_tick):
    """Run servers and collect data"""
    cost = 0
    logs = []
    for users in users_per_tick:
        cluster.add_task(users)
        cost += len(cluster.stats()) * TICK_VALUE
        logs.append(cluster.stats())
        cluster.clock()

    while cluster.servers_list:
        cost += len(cluster.stats()) * TICK_VALUE
        logs.append(cluster.stats())
        cluster.clock()
    return {
        'cost': cost,
        'logs': logs
    }


if __name__ == '__main__':
    # Reads Command Line arguments or raise Exception
    try:
        src, des = sys.argv[1], sys.argv[2]
    except Exception:
        exception_text = 'Invalid arguments. Please, run: ' \
                         '"python {} input_file_path output_file_path"'.format(sys.argv[0])
        raise Exception(exception_text)

    # Start vars in keeping with received args
    with open(src) as file:
        _input = text_numbers_to_tuple(file.read())
    ttask, umax, users_per_tick = _input[0], _input[1], _input[2:]

    cluster = Cluster(ttask, umax)

    # Run
    result = cluster_runner(cluster, users_per_tick)
    result_text = custom_joiner(result['logs'], result['cost'])
    with open(des, 'w') as x:
        x.write(result_text)

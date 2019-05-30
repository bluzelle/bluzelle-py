import socket, errno
import logging
from pprint import pformat
import random


def is_free(port):
    free = False

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind(("127.0.0.1", port))
        free = True
    except socket.error as e:
        if e.errno == errno.EADDRINUSE:
            logging.debug(f'Port {port} is in use')
        else:
            logging.debug(f'Port {port} cannot be used {pformat(e, indent=4)}')
    s.close()
    return free


def get_next_free():
    port = -1
    while (port < 0):
        rand_port = random.randrange(49153, 65534) # safe range
        if (is_free(rand_port)):
            port = rand_port

    return port
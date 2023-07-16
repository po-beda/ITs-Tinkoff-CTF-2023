#  96.564, -155.97, -161.71, 17.1329, 143.143, -161.943, 48.805
#  ['skpf', '24c8', '1n0t', 'jhrg', 'wr55', '1mcm', 'nbub']

import socket
import json
import sys
import time

encoded_str = 'skpf24c81n0tjhrgwr551mcmnbub'
HOST = '158.176.4.7'
PORT = 9443
FILENAME = 'storage.txt'

splitted = [encoded_str[x * 4:x * 4 + 4] for x in range(int(len(encoded_str) / 4))]
print(splitted)

with open(FILENAME, 'w+') as file:
    try:
        HASH_STORAGE = json.load(file)
    except json.decoder.JSONDecodeError:
        print('valid JSON-storage not found, created new', file=sys.stderr)
        HASH_STORAGE = {}


def float_range(start: int, stop: int, step: float):
    while start <= stop:
        yield float(start)
        start += step


def _read_sock(sock: socket.socket) -> str:
    res = ''
    while True:
        resp = sock.recv(1024)
        res += resp.decode()
        if not resp or len(resp) < 1024:  # len of hello message from socket 936 bytes
            break
    return res


def connect() -> socket.socket:
    """
    Create connection to server
    Returns:
        valid socket
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    print(_read_sock(sock))
    sock.sendall('H\n'.encode())    # b = bytearray()
    time.sleep(0.5)
    print(_read_sock(sock))

    return sock


def get_hash(sock: socket.socket, content: str) -> str:
    """
    write current coordinates and get geohash from server
    Args:
        sock: socket object
        content: coordinates
    Returns:
        geohash value
    """
    sock.sendall((content + '\n').encode())
    res = _read_sock(sock)
    return res


prev_val = HASH_STORAGE.get('prev', -180)
nums_gen = float_range(prev_val, 180, 0.001)


if __name__ == '__main__':
    active_storrage = HASH_STORAGE
    sock = connect()

    for hashed_str in splitted:
        while True:
            try:
                val = next(nums_gen)
                if active_storrage.get(val):
                    continue

                response = get_hash(sock, str(val))
                active_storrage[val] = response
            except Exception as err:
                print(err)
                sock = connect()
    with open(FILENAME, 'w+') as file:
        json.dump(active_storrage, file)

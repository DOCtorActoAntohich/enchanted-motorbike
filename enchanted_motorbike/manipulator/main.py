import socket

from pydantic import parse_raw_as

from enchanted_motorbike.models.sensor_data import SensorData
from enchanted_motorbike.settings import settings


def listen(server_socket):
    while True:
        server_socket.listen(1)
        conn, addr = server_socket.accept()
        with conn:
            data = conn.recv(1024)
            sensor_data = parse_raw_as(SensorData, data)


def run_manipulator() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("0.0.0.0", settings.manipulator.port))
        try:
            listen(sock)
        except KeyboardInterrupt:
            pass

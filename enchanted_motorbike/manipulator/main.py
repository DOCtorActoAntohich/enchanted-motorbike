import logging
import socket

from pydantic import parse_raw_as

from enchanted_motorbike.models import ManipulatorStateDecision
from enchanted_motorbike.settings import settings

MaxClients = 1
MaxDataSizeBytes = 1024


class ManipulatorServer:
    @classmethod
    def run(cls) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(("", settings.manipulator.port))
            cls.__listen_forever(server_socket)

    @classmethod
    def __listen_forever(cls, server_socket: socket.socket) -> None:
        while True:
            server_socket.listen(MaxClients)
            client_socket, _ = server_socket.accept()
            cls.__handle_client(client_socket)

    @classmethod
    def __handle_client(cls, client_socket: socket.socket) -> None:
        with client_socket:
            raw_data = client_socket.recv(MaxDataSizeBytes)
            decision = parse_raw_as(ManipulatorStateDecision, raw_data)
            logging.critical(decision)

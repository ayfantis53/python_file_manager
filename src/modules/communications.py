"""Send messages through ports from client to server."""

# Standard lib imports
import socket
from threading import Lock


class Communications:
    """Handles recieving and sending messages using ports.

    Attributes:
        mutex (Lock)       synchronization primitive object designed to handle mutual exclusion.
        is_primary (bool): Tells us if we should be sending messaged or not.
    """

    def __init__(self, mutex: Lock) -> None:
        """Class that initializes variables for file manager to run.

        Args:
            mutex (Lock) synchronization primitive object designed to handle mutual exclusion.
        """
        self.mutex = mutex
        self.is_primary = True

    def rec_proto(self, vars) -> None:
        """Connect to Socket and Receive Protobuf Message."""

        # Initialize new network socket object using IPv4 address family & TCP transport protocol.
        # Attach a client socket to a specific local IP address and port.
        # Put socket into a passive state, signal the operating system kernel to queue incoming connection requests.
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TODO: Delete
        client.bind((vars.HOST, 8089))  # TODO: Delete
        client.listen()  # TODO: Delete

        # Control flow statement used to create an infinite loop.
        while True:
            # Thread protection.
            self.mutex.acquire()

            # -- Attempt to wait for incoming connection --.
            try:
                # Wait for incoming connection, when connected, return new socket object.
                communication_socket, address = client.accept()
                vars.logger.info("Listening on port: " + str(address))

                # Receive primary message from Application and deserialize.
                message_isPrimary = communication_socket.recv(1024).decode("utf-8")

                # Are we primary? If not we dont run copy.
                # Is primary.
                if message_isPrimary == "isprimary":
                    self.is_primary = True
                # Is NOT primary.
                else:
                    self.is_primary = False
            # -- Handles remote server or peer forcefully close on an active network connection unexpectedly --.
            except ConnectionResetError:
                print("Client closed the connection unexpectedly.")
            # -- Handles system-related, i.e. Input/Output, missing file, or network/permission error --.
            except OSError as err:
                print(f"Socket error occurred: {err}")
            # -- Guaranteed to run under all circumstances --.
            finally:
                # Release mutually exclusive lock (mutex) so other waiting threads can access shared resources.
                self.mutex.release()

            vars.logger.info("Connection with " + str(address) + " ended")
            communication_socket.close()

    def send_proto(self, b_status: list[bool], vars: dict) -> None:
        """Connect to Socket and Send Protobuf Message.

        Args:
            b_status (list[bool]): List of the health of all files.
            vars (dict):           Data from config file.
        """
        vars.logger.info("Connected to port " + str(vars.PORT))

        # Initialize Health message.
        state = vars.GREEN
        log_state = "GREEN"

        # Health message.
        for status in range(len(b_status)):
            # Status is Unhealthy.
            if b_status[status] == vars.red:
                state = vars.red
                log_state = "RED"
                break
            # Status is Degraded.
            elif b_status[status] == vars.yellow and state != vars.red:
                state = vars.yellow
                log_state = "YELLOW"

        # Transmit data over a network.
        vars.client.send(log_state.encode("utf-8"))

        vars.logger.info(
            "Sent health message of -------------------------------- " + log_state
        )

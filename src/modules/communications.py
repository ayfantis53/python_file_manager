"""Send messages through ports from client to server."""

# Standard lib imports
import socket
from threading import Lock


class Communications:
    """Handles recieving and sending messages using ports.

    Attributes:
        is_primary (bool): Tells us if we should be sending messaged or not.
        ran_once (bool):   Tells us if we should print a not running message again.
        mutex (Lock)       synchronization primitive object designed to handle mutual exclusion.
    """

    def __init__(self) -> None:
        """Class that initializes variables for file manager to run."""
        self.is_primary = True
        self.ran_once = False
        # initializes a mutual exclusion lock (mutex),
        # from the threading module to prevent multiple threads from accessing a shared resource at the same time.
        self.mutex = Lock()

    def rec_proto(self, conf_vars) -> None:
        """Connect to Socket and Receive Protobuf Message.

        Args:
            conf_vars (dict): Data from config file.
        """
        # Initialize new network socket object using IPv4 address family & TCP transport protocol.
        # Attach a client socket to a specific local IP address and port.
        # Put socket into a passive state, signal the operating system kernel to queue incoming connection requests.
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TODO: Delete
        client.bind((conf_vars.host, 8089))  # TODO: Delete
        client.listen()  # TODO: Delete

        # Control flow statement used to create an infinite loop.
        while True:
            # Thread protection.
            self.mutex.acquire()

            # -- Attempt to wait for incoming connection --.
            try:
                # Wait for incoming connection, when connected, return new socket object.
                communication_socket, address = client.accept()
                client_ip, client_port = address
                conf_vars.logger.info(
                    "Listening on port: %s on %s port",
                    client_ip,
                    client_port,
                )

                # Receive primary message from Application and deserialize.
                message_isPrimary = communication_socket.recv(1024).decode("utf-8")

                # Are we primary? If not we dont run copy.
                # Is primary.
                if message_isPrimary == "isprimary":
                    self.is_primary = True
                # Is NOT primary.
                else:
                    self.is_primary = False
                    conf_vars.logger.warning("is NO longer primary.")
            # -- Handles remote server or peer forcefully close on an active network connection unexpectedly --.
            except ConnectionResetError:
                conf_vars.logger.error("Client closed the connection unexpectedly.")
            # -- Handles system-related, i.e. Input/Output, missing file, or network/permission error --.
            except OSError as err:
                conf_vars.logger.error("Socket error occurred: %s", err)
            # -- Guaranteed to run under all circumstances --.
            finally:
                # Release mutually exclusive lock (mutex) so other waiting threads can access shared resources.
                self.mutex.release()

            # terminates network connection & releases system resources allocated to that specific socket descriptor.
            conf_vars.logger.info(
                "Connection with %s on port %s closed",
                client_ip,
                client_port,
            )
            communication_socket.close()

    def send_proto(self, b_status: list[bool], conf_vars: dict) -> None:
        """Connect to Socket and Send Protobuf Message.

        Args:
            b_status (list[bool]): List of the health of all files.
            conf_vars (dict):      Data from config file.
        """
        conf_vars.logger.debug("Connected to port %d", conf_vars.port)

        # Initialize Health message.
        state = conf_vars.green
        log_state = "GREEN"

        # Health message.
        for status in range(len(b_status)):
            # Status is Unhealthy.
            if b_status[status] == conf_vars.red:
                state = conf_vars.red
                log_state = "RED"
                break
            # Status is Degraded.
            elif b_status[status] == conf_vars.yellow and state != conf_vars.red:
                state = conf_vars.yellow
                log_state = "YELLOW"

        # Transmit data over a network.
        conf_vars.client.send(log_state.encode("utf-8"))

        conf_vars.logger.info(
            "Sent health message of -------------------------------- %s",
            log_state,
        )

"""Send messages through ports from client to server."""

# Standard Library Imports
import socket
from threading import Lock


class Communications:
    """Handles recieving and sending messages using ports.
    
    Attributes:
        mutex (Lock) synchronization primitive object designed to handle mutual exclusion.
    """

    def __init__(self, mutex: Lock) -> None:
        """Class that initializes variables for file manager to run.
        
        Args:
            mutex (Lock) synchronization primitive object designed to handle mutual exclusion.
        """
        self.mutex = mutex

    def rec_proto(self, vars) -> None:
        """ Connect to Socket and Receive Protobuf Message."""

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # TODO: Delete
        client.bind((vars.HOST, 8089))                                  # TODO: Delete
        client.listen()                                                 # TODO: Delete

        # Are we primary? If not we dont run copy.
        global is_primary

        while True:
            # Thread protection.
            self.mutex.acquire()

            try:
                communication_socket, address = client.accept()
                vars.logger.info("Listening on port: " + str(address))

                # Receive primary message from Application and deserialize
                message_isPrimary = communication_socket.recv(1024).decode('utf-8')

                if message_isPrimary == "isprimary":
                    is_primary = True
                else:
                    is_primary = False
            finally:
                # thread protection.
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

        # Health message
        for status in range(len(b_status)):
            if b_status[status] == vars.RED:
                state = vars.RED
                log_state = "RED"
                break
            elif b_status[status] == vars.YELLOW and state != vars.RED:
                state = vars.YELLOW
                log_state = "YELLOW"

        vars.client.send(log_state.encode('utf-8'))

        vars.logger.info("Sent health message of -------------------------------- " + log_state)
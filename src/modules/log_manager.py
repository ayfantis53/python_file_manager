"""Sets up and manages the logfile of output from app running."""

# Standard Library Imports
import logging
from pathlib import Path


class LogManager:
    """Class that sets up and manages the logfile of output from app running.

    Attributes:
        logfile_destination (Path | str): file path logfile will be written to.
    """

    def __init__(self, logfile_destination: Path | str) -> None:
        """Acts as a blueprint for setting up a new object when LogManager
        is instantiated. Also sets all class variables.

        Args:
            logfile_destination (Path | str): file path logfile will be written to.
        """
        self.logfile_destination = logfile_destination

    def log_setup(self, logfile_destination: Path | str) -> logging.Logger:
        """Sets up projects output log file at location provided.

        Args:
            logfile_destination (Path | str): file path logfile will be written to.

        Returns:
            (object) logging.Logger instance associated with the specified name.
        """
        # Make log file path if it doesnt exist.
        if not Path(logfile_destination).exists():
            Path(logfile_destination).mkdir(parents=True, exist_ok=True)

        # Create logfile path destination.
        logging.basicConfig(
            filename=str(logfile_destination) + "file_manager.log", level=logging.DEBUG
        )

        # initialize logger.
        logger = logging.getLogger()

        return logger

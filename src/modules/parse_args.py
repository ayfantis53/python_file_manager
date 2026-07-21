"""Parse the command line arguments from user."""

# Standard lib imports
import argparse


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    """Parse the different arguments from CLI.

    Args:
        args (list[str]): Command line arguments.

    Returns:
        (argparse.Namespace) a simple object used as a container to store the results of command-line argument parsing.
    """
    # creates an argument parser object from the built-in argparse module.
    # object serves as foundation for building a command-line interface (CLI) for script.
    parser = argparse.ArgumentParser()

    # define the -c/--comms command-line arguments script can accept.
    parser.add_argument(
        "-c",
        "--comms",
        type=str,
        default="PORT",
        choices=["PORT", "PROTO"],
        help="Determines the communication type. Default is PORT",
    )

    # define the -j/--json-file command-line arguments script can accept.
    parser.add_argument(
        "-j",
        "--json-file",
        type=str,
        default="./conf/file_manager.conf",
        help="file name and location for file_manager results",
    )

    # Takes the raw strings provided by the user in the terminal and converts them into a Python object.
    return parser.parse_args(args)

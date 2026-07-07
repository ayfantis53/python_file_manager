"""Copies files from one file to another based on send flag."""

# Standard lib imports
import datetime
import glob
import os
import shutil
import sys
import time
from threading import Thread, Lock

# Local imports
from modules.communications import Communications
from modules.file_manage_init import FileManagerInit
from modules.parse_args import parse_args


# initializes a mutual exclusion lock (mutex),
# from the threading module to prevent multiple threads from accessing a shared resource at the same time.
mutex = Lock()


def file_retention_management(index: int, vars: dict, year: int) -> None:
    """Delete files that are past leniency times.

    Args:
        index (int):       File iteration we're on when looping through directory.
        vars (dict):       Data from config file.
        year (int):        Year of the file creation.
    """
    data_dir = vars.paths[index].get(vars.message_dir)

    # Add "_year" to directory if needed based on config.
    if vars.paths[index].get(vars.year):
        data_dir = str(data_dir) + "_" + str(year)

    # File exists and that it wasnt previously copied in the last run.
    if os.path.exists(data_dir):
        leniency_time = vars.paths[index].get("LENIENCY")

        # turning leniency time in minutes to a datetime format to be compared.
        current_time = datetime.datetime.now()
        retention_time = current_time - datetime.timedelta(minutes=leniency_time)

        # Looking through a directory and putting files into an array.
        msgfiles = os.path.join(data_dir, "*")
        l_msgfiles = glob.glob(msgfiles)

        # Go through the files and get the creation time from each one.
        for m_file in l_msgfiles:
            t_mod = os.path.getmtime(m_file)
            t_mod = datetime.datetime.fromtimestamp(t_mod)

            # Is the file older than the current time - retention time.
            if retention_time > t_mod:
                # -- Attempt to delete a specific file path from the filesystem --.
                try:
                    os.remove(m_file)
                    vars.logger.info(
                        "File [" + str(m_file) + "] deleted because it was outdated"
                    )
                # -- Handles access/manipulating file that does not exist at path --.
                except FileNotFoundError as err:
                    vars.logger.error(f"File Not found {err}.")
                # -- Handles performing an operation on file without access privileges --.
                except PermissionError:
                    print("Do NOT have permission to delete this file.")
                # -- Handles system-related, i.e. Input/Output, missing file, or network/permission error --.
                except OSError as err:
                    print(f"A different OS error occurred: {err}.")
    # File does NOT exist.
    else:
        vars.logger.error(
            'File Manager could not find Directory: "' + str(data_dir) + '"'
        )


def file_copied_management(
    last_time: float,
    index: int,
    vars: dict,
    year: int,
) -> datetime.datetime:
    """Copy files that arent past leniency times.

    Args:
        last_time (float): Time of last copied file.
        index (int):       File iteration we're on when looping through directory.
        vars (dict):       Data from config file.
        year (int):        Year of the file creation.

    Returns:
        ([datetime.datetime, int])
            returns the current local date and time as a datetime object.
            returns exit code.
    """
    dest_dir = vars.paths[index].get(vars.dest_dir)
    data_dir = vars.paths[index].get(vars.message_dir)

    # Add _year to directory if needed based on config.
    if vars.paths[index].get(vars.year):
        data_dir = str(data_dir) + "_" + str(year)
        dest_dir = str(dest_dir) + "_" + str(year)

    # Any files Copied?
    copied = False

    # Looking through the directory and putting files into an array.
    msgfiles = os.path.join(data_dir, "*")
    l_msgfiles = glob.glob(msgfiles)

    # make sure files exists and that it wasnt previously copied in the last run.
    if os.path.exists(data_dir):
        # Destination does NOT exists for output directory so create it.
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
            vars.logger.error(
                "Destination Directory ["
                + str(dest_dir)
                + "] did NOT exist and was created"
            )

        # Go through the files and get the creation time from each one.
        for t_file in l_msgfiles:
            t_mod = os.path.getmtime(t_file)
            t_mod = datetime.datetime.fromtimestamp(t_mod)

            # make sure file wasnt copied previously in the last run.
            if last_time <= t_mod:
                # Do we have permission to copy this file.
                if os.access(t_file, os.R_OK):
                    # Try and copy the file since it passed all checks.
                    try:
                        shutil.copy(t_file, dest_dir)
                        vars.logger.debug(
                            'File: "'
                            + str(t_file)
                            + '" copied to "'
                            + str(dest_dir)
                            + '"'
                        )
                        copied = True
                    # Not copied for some other reason.
                    except Exception:
                        vars.logger.error("Could NOT copy file")
                        return [datetime.datetime.now(), 0]
                else:
                    # Return 0 for failed.
                    vars.logger.debug(
                        "Permission Denied to read File: [" + str(t_file) + "]"
                    )
                    return [last_time, 0]
    # Folder does NOT exist.
    else:
        # Return 0 for failed.
        vars.logger.error('Data Directory "' + str(data_dir) + '" does NOT Exist')
        return [last_time, 0]

    # Files were not copied.
    if not copied:
        # Return 1 for Degraded.
        vars.logger.warning('No New Files to Copy in "' + str(data_dir) + '"')
        return [datetime.datetime.now(), 1]

    # Set the new previous time to compare to in next run return 2 for Nominal.
    return [datetime.datetime.now(), 2]


def thread_daemon(vars: FileManagerInit, comms: Communications) -> None:
    """Main thread that does main logic.

    Args:
        vars (FileManagerInit):  Get File manager setup class object.
        comms (Communications): Handles recieving and sending messages using ports class object.
    """
    # initialize variables.
    periodicity = vars.configs.get(vars.freq_checks)
    last_time = [0 for i in vars.paths]
    b_status = [False for i in vars.paths]
    status_good = True

    for path in range(len(vars.paths)):
        # initialize time to compare files to, for copy management.
        last_time[path] = datetime.datetime.min

        # Going to be our health variable to send to APP 2 SUCCESS, 1 DEGRADED, 0 FAIL.
        b_status[path] = vars.green

    # Control flow statement used to create an infinite loop.
    while True:
        # Get time to put in logs and save to know what files are new to copy.
        current_time = datetime.datetime.now()

        print("Current time : {0}".format(current_time))

        if comms.is_primary:
            # Set it back to initial.
            if comms.ran_once:
                comms.ran_once = False

            # Find out if all directories are red.
            for path in range(len(vars.paths)):
                if b_status[path] == vars.red and not status_good:
                    status_good = False
                else:
                    status_good = True

            # If we have at least one non red directory we still run.
            if status_good:
                for path in range(len(vars.paths)):
                    # Delete outdated files and copy new ones.
                    file_retention_management(path, vars, current_time.year)
                    last_time[path], b_status[path] = file_copied_management(
                        last_time[path],
                        path,
                        vars,
                        current_time.year,
                    )

                # Send message to HSD.
                comms.send_proto(b_status, vars)

                # Time to wait until the next loop iteration.
                time.sleep(periodicity * vars.seconds_per_min)

            else:
                # One or both directories have something wrong with them and check every 10 seconds to see if it should run again.
                vars.logger.error("APP Status is RED Attempting to rerun!!!")
                time.sleep(vars.failure_period_time)
        else:
            # Set it to not run over and over.
            if not comms.ran_once:
                # Not Primary so it will check every 10 seconds to see if it should run again.
                vars.logger.debug(
                    'APP IS NOT PRIMARY, AND NOT RUNNING... Listening for ["isprimary"] message'
                )
                comms.ran_once = True

            time.sleep(vars.failure_period_time)


def main():
    """Main Function runs main and communication thread."""
    # ================
    # Initialize.
    # ================

    # comms_type="PORT"
    # File paths.
    json_file_path = "./conf/file_manager.conf"

    # ================
    # CLI args.
    # ================

    # Get arguments from command line.
    args = parse_args(sys.argv[1:])

    # Set the json file in command line args.
    if args.json_file:
        json_file_path = args.json_file
    # if args.comms:
    #     comms_type = args.comms

    # ================
    # Initialize Modules.
    # ================

    # Modules.
    comms = Communications(mutex)
    file_manage_init = FileManagerInit(json_file_path)

    # ================
    # Manage Threads.
    # ================

    # Create threads to be ran concurrently.
    t1 = Thread(target=comms.rec_proto, args=(file_manage_init,))
    t2 = Thread(
        target=thread_daemon,
        args=(
            file_manage_init,
            comms,
        ),
    )

    # flags as a daemon thread, the background process will terminate as soon as all non-daemon threads finish executing.
    t1.daemon = True
    t2.daemon = True

    # Run thread to listen to APP.
    t1.start()
    t2.start()

    # ================
    # Handle unexpected shutdown.
    # ================

    # -- Application is running CTRL-C is not pressed --.
    try:
        # Control flow statement used to create an infinite loop.
        while True:
            time.sleep(0.1)
    # -- Handles when a user manually interrupts a running script --.
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        sys.exit(1)


if __name__ == "__main__":
    """ Ensure this code only runs if the script is executed.
    Not when it's imported as a module by another file.
    """
    main()

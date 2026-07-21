"""Special configuration file used to share test fixtures, load external plugins,
and define hook functions across multiple test files."""

# Standard Library imports
import datetime
import filecmp
from pathlib import Path

# Third-party imports
import pytest

# Local imports
from src.file_manager import file_copied_management
from src.modules.file_manager_init import FileManagerInit


# ================
# Helper Functions: Configs.
# ================


def test_json_setup_config_vars(
    var_1: int,
    var_2: str,
    var_3: int,
    var_4: str,
    file_manager_init: FileManagerInit,
) -> bool:
    """Make sure config variables have correct values.

    Args:
         var_1 (int):                Port number to be tested.
         var_2 (str):                Host name to be tested.
         var_3 (int):                Frequency checks number to be tested.
         var_4 (str):                Logfile path to be tested.
         file_manager_init (object): Class to setup file_manager.

    Returns:
        (bool)
            True:  Variables are equal and correct.
            False: Variables are NOT equal and incorrect.
    """
    # Initialize variables.
    config_variables = file_manager_init.json_parse(config_var="CONFIG_VARS")

    config_port = config_variables.get("PORT")
    config_host = config_variables.get("HOST")
    config_freq = config_variables.get("FREQUENCY_CHECKS")
    config_logs = config_variables.get("LOGFILE_PATH")

    # All variables are correct.
    if (
        config_port == var_1
        and config_host == var_2
        and config_freq == var_3
        and config_logs == var_4
    ):
        return True
    # Variables are NOT correct.
    else:
        return False


def test_json_setup_path_vars(
    var_1: str,
    var_2: int,
    var_3: str,
    var_4: int,
    file_manager_init: FileManagerInit,
) -> bool:
    """Make sure json path variables have correct values.

    Args:
         var_1 (str):                data directory borep path to be tested.
         var_2 (int):                Leniency borep number value to be tested.
         var_3 (str):                data directory eph path to be tested.
         var_4 (int):                Leniency eph number value to be tested.
         file_manager_init (object): Class to setup file_manager.

    Returns:
        (bool)
            True:  Variables are equal and correct.
            False: Variables are NOT equal and incorrect.
    """
    # Initialize variables.
    config_paths = file_manager_init.json_parse("DATA_PATHS")

    conf_data_first = config_paths[0].get("DATA_DIR")
    conf_leniency_first = config_paths[0].get("LENIENCY")
    conf_data_next = config_paths[1].get("DATA_DIR")
    conf_leniency_next = config_paths[1].get("LENIENCY")

    # All variables are correct.
    if (
        conf_data_first == var_1
        and conf_leniency_first == var_2
        and conf_data_next == var_3
        and conf_leniency_next == var_4
    ):
        return True
    # Variables are NOT correct.
    else:
        return False


# ================
# Helper Functions: Copying.
# ================


def test_file_copied_management(
    data_dir: str,
    dir: str,
    last_time: int,
    index: int,
    year: int,
    file_manager_init: FileManagerInit,
) -> bool:
    """Check if after copy both directories have same number of files in them.

    Args:
        data_dir (str):             Directory where files will be copied fromto be tested against.
        dir (str):                  Directory where files will be copied from to be tested.
        last_time (int):            Time of last file copied over.
        index (int):                Data_path index whether it be data_first or data_second.
        year (int):                 Current year.
        file_manager_init (object): Class to setup file_manager.

    Returns:
        (bool)
            True:  Folders had the same amount of files after copy.
            False: Folders did NOT have the same amount of files after copy.
    """
    # Initialize variables.
    data = file_manager_init.json_parse("DATA_PATHS")
    dest_dir = data[index].get("DEST_DIR")
    eph_data = data[1].get(data_dir)

    # Add _year to directory if needed based on config.
    if data[index].get(file_manager_init.year):
        dest_dir = str(dest_dir) + "_" + str(year)
    eph_data = str(eph_data) + "_" + str(year)

    # Run copy function from file_manager.
    file_copied_management(last_time, index, file_manager_init, year)

    # Compare both directories.
    comparison = filecmp.dircmp(dir, dest_dir)

    # merges elements into single string, placing a comma separator between each element.
    left_only_files = ",".join(comparison.left_only)
    right_only_files = ",".join(comparison.right_only)

    # Same amount of files in data and destination directories.
    if left_only_files == right_only_files:
        return True
    # Different amount of files in data and destination directories.
    else:
        return False


def test_data_create(data_dir: str, max: int) -> None:
    """Create directory with test files to copy.

    Args:
        dir (str): Path to data directory.
        max (int): Number of test files to make in the directory.
    """
    # Create the directory and any missing parent directories.
    Path(data_dir).mkdir(parents=True, exist_ok=True)

    # Create the amount of files as given in arguments.
    for item in range(0, max):
        f = open(data_dir + "/" + "item_" + str(item), "w")
        f.close()


# ================
# Helper Functions: TestRetention.
# ================


def test_file_retention_management(
    dir_index: int,
    file_manager_init: FileManagerInit,
) -> bool:
    """Test we are deleting outdated index 0 or 1 files correctly.

    Args:
        dir_index (int):            Data directory we check for expired files in (0: borep, 1: eph).
        file_manager_init (object): Class to setup file_manager.

    Returns:
        (bool)
            True:  No expired files were found in data dir.
            False: Expired files were found in data dir.
    """
    # Initialize variables.
    config_paths = file_manager_init.json_parse("DATA_PATHS")
    data_dir = config_paths[dir_index].get("DATA_DIR")
    leniency_time = config_paths[dir_index].get("LENIENCY")

    # Initialize time.
    current_time = datetime.datetime.now()
    retention_time = current_time - datetime.timedelta(minutes=leniency_time)

    # Iterate files, get the raw Unix timestamp & convert POSIX/Unix timestamp to human readable.
    for m_file in Path(data_dir).glob("*"):
        t_mod = m_file.stat().st_mtime
        t_mod = datetime.datetime.fromtimestamp(t_mod)

        # Retention time is greater than time modified.
        if retention_time > t_mod:
            return False

    return True


@pytest.fixture(scope="class")
def inject_helpers(request):
    """
    Binds shared helper utilities and data generators
    directly to the invoking unittest.TestCase class context.
    """
    # Bind the functions to the class object.
    request.cls.test_json_setup_config_vars = staticmethod(test_json_setup_config_vars)
    request.cls.test_json_setup_path_vars = staticmethod(test_json_setup_path_vars)
    request.cls.test_file_copied_management = staticmethod(test_file_copied_management)
    request.cls.test_data_create = staticmethod(test_data_create)
    request.cls.test_file_retention_management = staticmethod(
        test_file_retention_management
    )

    # You can also bind class-cached mock databases or client systems.
    request.cls.shared_constant = "APP_TEST_ENV"

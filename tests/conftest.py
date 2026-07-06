"""Special configuration file used to share test fixtures, load external plugins,
and define hook functions across multiple test files."""

# Standard Library imports
import datetime
import filecmp
import glob
import os
from pathlib import Path

# Third-party imports
import pytest

# Local imports
from src.file_manager import file_copied_management


# ================
# Helper Functions: Configs.
# ================


def test_json_setup_config_vars(var_1: int, var_2: str, var_3: int, var_4: str, file_manager_init,) -> bool:
    """Make sure config variables have correct values.

    Args:
         var_1 (int): Port number to be tested.
         var_2 (str): Host name to be tested.
         var_3 (int): Frequency checks number to be tested.
         var_4 (str): Logfile path to be tested.

    Returns:
        (bool)
            True:  Variables are equal and correct.
            False: Variables are NOT equal and incorrect.
    """
    config_variables = file_manager_init.json_parse(config_var="CONFIG_VARS")

    config_port = config_variables.get("PORT")
    config_host = config_variables.get("HOST")
    config_freq = config_variables.get("FREQUENCY_CHECKS")
    config_logs = config_variables.get("LOGFILE_PATH")

    if (
        config_port == var_1
        and config_host == var_2
        and config_freq == var_3
        and config_logs == var_4
    ):
        return True
    else:
        return False


def test_json_setup_path_vars(var_1: str, var_2: int, var_3: str, var_4: int, file_manager_init,) -> bool:
    """Make sure config variables have correct values.

    Args:
         var_1 (str): data directory borep path to be tested.
         var_2 (int): Leniency borep number value to be tested.
         var_3 (str): data directory eph path to be tested.
         var_4 (int): Leniency eph number value to be tested.

    Returns:
        (bool)
            True:  Variables are equal and correct.
            False: Variables are NOT equal and incorrect.
    """
    config_paths = file_manager_init.json_parse("DATA_PATHS")

    config_bore = config_paths[0].get("DATA_DIR")
    config_lenb = config_paths[0].get("LENIENCY")
    config_ephe = config_paths[1].get("DATA_DIR")
    config_lene = config_paths[1].get("LENIENCY")

    if (
        config_bore == var_1
        and config_lenb == var_2
        and config_ephe == var_3
        and config_lene == var_4
    ):
        return True
    else:
        return False


# ================
# Helper Functions: Copying.
# ================


def test_file_copied_management(data_dir, dir, last_time, index, year, file_manager_init,) -> bool:
    """Check if after copy both directories have same number of files in them.

    Args:
        data_dir (str):
        dir (str):
        last_time (int):
        index (int):
        year (int):

    Returns:
        (bool)
            True:  Folders had the same amount of files after copy.
            False: Folders did NOT have the same amount of files after copy.
    """
    data = file_manager_init.json_parse("DATA_PATHS")

    nas = data[index].get("NAS_DIR")
    bore_data = data[0].get(data_dir)
    eph_data = data[1].get(data_dir)

    # Add _year to directory if needed based on config.
    if data[index].get(file_manager_init.year):
        nas = str(nas) + "_" + str(year)
    eph_data = str(eph_data) + "_" + str(year)

    # Run copy function from file_manager.
    file_copied_management(last_time, index, file_manager_init, year)

    # Compare both directories.
    comparison = filecmp.dircmp(dir, nas)

    left_only_files = ",".join(comparison.left_only)
    right_only_files = ",".join(comparison.right_only)

    if left_only_files == right_only_files:
        return True
    else:
        return False


def test_data_create(data_dir: str, max: int) -> None:
    """Create directory with test files to copy.

    Args:
        dir (str): Path to data directory.
        max (int): Number of test files to make in the directory
    """
    # Create the directory and any missing parent directories
    Path(data_dir).mkdir(parents=True, exist_ok=True)

    for item in range(0, max):
        f = open(data_dir + "/" + "item_" + str(item), "w")
        f.close()


# ================
# Helper Functions: TestRetention.
# ================


def test_file_retention_management(dir_index, file_manager_init) -> bool:
    """Test we are deleting outdated index 0 or 1 files correctly.

    Args:
        index (int): Which data directory we are checking for expired files (0: borep, 1: eph).

    Returns:
        (bool)
            True:  No expired files were found in data dir.
            False: Expired files were found in data dir.
    """
    config_paths = file_manager_init.json_parse("DATA_PATHS")

    data_dir = config_paths[dir_index].get("DATA_DIR")
    leniency_time = config_paths[dir_index].get("LENIENCY")

    current_time = datetime.datetime.now()
    retention_time = current_time - datetime.timedelta(minutes=leniency_time)

    msgfiles = os.path.join(data_dir, "*")
    l_msgfiles = glob.glob(msgfiles)

    for m_file in l_msgfiles:
        t_mod = os.path.getmtime(m_file)
        t_mod = datetime.datetime.fromtimestamp(t_mod)

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
    request.cls.test_file_retention_management = staticmethod(test_file_retention_management)
    
    # You can also bind class-cached mock databases or client systems.
    request.cls.shared_constant = "APP_TEST_ENV"
"""Test code."""

# Standard Library Imports
import os
import sys
import glob
import filecmp
import unittest
import datetime

sys.path.append("..")

# Local Imports
from src.file_manager import file_copied_management
from src.file_manager import file_retention_management
from src.modules.file_manage_init import FileManagerInit


# ================
# Global variables.
# ================
global JSON_FILE
JSON_FILE = "./conf/file_manager.conf"

global FILE_MANAGER_INIT
FILE_MANAGER_INIT = FileManagerInit(JSON_FILE)


# ================
# Testing Suites.
# ================


class TestJSON(unittest.TestCase):
    """Using Python's built-in unittest library, using subclass unittest.TestCase
    test methods are defined that start with the prefix test. Test our JSON reliability."""

    def test_json_SUCCESS(self):
        """Test that our config variables are being read correctly."""
        print("TESTED JSON CORRECT VALUES")

        result_1 = test_json_setup_config_vars(9090, "localhost", 0.5, "../test/logs/")
        result_2 = test_json_setup_path_vars(
            "../test/test_data/Data_borep",
            1,
            "../test/test_data/Data_ep",
            1,
        )

        # Were the values in the json correct?
        if result_1 != result_2 and result_1:
            result = False
        else:
            result = True

        self.assertEqual(result, True)

    def test_json_FAIL(self):
        """Test that our config variables recognize incorrect values."""
        print("TESTED JSON NOT-CORRECT VALUES")

        result_1 = test_json_setup_config_vars(8080, "lochost", 5, "./test/logs/")
        result_2 = test_json_setup_path_vars(
            "../test/test_data/Data_repars", 12, "../test/test_data/Daa_epheeris", 1
        )

        # Were the values in the json correct?
        if result_1 != result_2 and result_1:
            result = False
        else:
            result = True

        self.assertEqual(result, True)


class TestCopy(unittest.TestCase):
    """Using Python's built-in unittest library, using subclass unittest.TestCase
    test methods are defined that start with the prefix test. Test we copy files correctly."""

    def test_borep(self):
        """Test all borep files were copied correctly."""
        print("TESTED BOREP COPY FUNCTIONALITY")
        current_time = datetime.datetime.now()

        last_time_bore = datetime.datetime.min
        test_data_create("./test_data/Data_borep", 3)

        result = test_file_copied_management(
            "DATA_DIR",
            "./test_data/Data_borep",
            last_time_bore,
            0,
            current_time.year,
        )

        self.assertEqual(result, True)

    def test_eph(self):
        """Test all ep files were copied correctly."""
        print("TESTED EP COPY FUNCTIONALITY")
        current_time = datetime.datetime.now()

        last_time_eph = datetime.datetime.min
        test_data_create("./test_data/Data_ep_2023", 3)

        result = test_file_copied_management(
            "DATA_DIR",
            "./test_data/Data_ep_2023",
            last_time_eph,
            1,
            current_time.year,
        )

        self.assertEqual(result, True)


class TestRetention(unittest.TestCase):
    """Using Python's built-in unittest library, using subclass unittest.TestCase
    test methods are defined that start with the prefix test. Test we delete files correctly."""

    def test_borep_retention(self):
        """Test we are deleting outdated borep files correctly."""
        print("TESTED BOREP RETENTION FUNCTIONALITY")
        current_time = datetime.datetime.now()

        file_retention_management(0, FILE_MANAGER_INIT, current_time.year)

        result = test_file_retention_management(0)

        self.assertEqual(result, True)

    def test_eph_retention(self):
        """Test we are deleting outdated ep files correctly."""
        print("TESTED EP RETENTION FUNCTIONALITY")
        current_time = datetime.datetime.now()

        file_retention_management(1, FILE_MANAGER_INIT, current_time.year)

        result = test_file_retention_management(1)

        self.assertEqual(result, True)


# ================
# Helper Functions: Configs.
# ================


def test_json_setup_config_vars(var1: int, var2: str, var3: int, var4: str):
    """Make sure config variables have correct values.

    Args:
         var1 (int): Port number to be tested.
         var1 (str): Host name to be tested.
         var1 (int): Frequency checks number to be tested.
         var1 (str): Logfile path to be tested.

    Returns:
        (bool)
            True:  Variables are equal and correct.
            False: Variables are NOT equal and incorrect.
    """
    config_variables = FILE_MANAGER_INIT.json_parse(config_var="CONFIG_VARS")

    config_port = config_variables.get("PORT")
    config_host = config_variables.get("HOST")
    config_freq = config_variables.get("FREQUENCY_CHECKS")
    config_logs = config_variables.get("LOGFILE_PATH")

    if (
        config_port == var1
        and config_host == var2
        and config_freq == var3
        and config_logs == var4
    ):
        return True
    else:
        return False


def test_json_setup_path_vars(var1: str, var2: int, var3: str, var4: int):
    """Make sure config variables have correct values.

    Args:
         var1 (str): data directory borep path to be tested.
         var1 (int): Leniency borep number value to be tested.
         var1 (str): data directory eph path to be tested.
         var1 (int): Leniency eph number value to be tested.

    Returns:
        (bool)
            True:  Variables are equal and correct.
            False: Variables are NOT equal and incorrect.
    """
    config_paths = FILE_MANAGER_INIT.json_parse("DATA_PATHS")

    config_bore = config_paths[0].get("DATA_DIR")
    config_lenb = config_paths[0].get("LENIENCY")
    config_ephe = config_paths[1].get("DATA_DIR")
    config_lene = config_paths[1].get("LENIENCY")

    if (
        config_bore == var1
        and config_lenb == var2
        and config_ephe == var3
        and config_lene == var4
    ):
        return True
    else:
        return False


# ================
# Helper Functions: Copying.
# ================


def test_file_copied_management(json, dir, last_time, index, year):
    """Check if after copy both directories have same number of files in them.

    Args:
        json (str):
        dir (str):
        last_time (int):
        index (int):
        year (int):

    Returns:
        (bool)
            True:  Folders had the same amount of files after copy.
            False: Folders did NOT have the same amount of files after copy.
    """
    data = FILE_MANAGER_INIT.json_parse("DATA_PATHS")

    nas = data[index].get("NAS_DIR")
    bore_data = data[0].get(json)
    eph_data = data[1].get(json)

    # Add _year to directory if needed based on config.
    if data[index].get(FILE_MANAGER_INIT.YEAR):
        nas = str(nas) + "_" + str(year)
    eph_data = str(eph_data) + "_" + str(year)

    # Delete current files in NAS directories.
    for f in os.listdir(nas):
        os.remove(os.path.join(nas, f))
    for f in os.listdir(bore_data):
        os.remove(os.path.join(bore_data, f))
    for f in os.listdir(eph_data):
        os.remove(os.path.join(eph_data, f))

    # Run copy function from file_manager.
    file_copied_management(last_time, index, FILE_MANAGER_INIT, year)

    # Compare both directories.
    comparison = filecmp.dircmp(dir, nas)

    left_only_files = ",".join(comparison.left_only)
    right_only_files = ",".join(comparison.right_only)

    if left_only_files == right_only_files:
        return True
    else:
        return False


def test_data_create(dir: str, max: int) -> None:
    """Create directory with test files to copy.

    Args:
        dir (str): Path to data directory.
        max (int): Number of test files to make in the directory
    """
    for item in range(0, max):
        f = open(dir + "/" + "item_" + str(item), "w")
        f.close()


# ================
# Helper Functions: TestRetention.
# ================


def test_file_retention_management(index):
    """Test we are deleting outdated index 0 or 1 files correctly.

    Args:
        index (int): Which data directory we are checking for expired files (0: borep, 1: eph).

    Returns:
        (bool)
            True:  No expired files were found in data dir.
            False: Expired files were found in data dir.
    """
    config_paths = FILE_MANAGER_INIT.json_parse("DATA_PATHS")

    data_dir = config_paths[index].get("DATA_DIR")
    leniency_time = config_paths[index].get("LENIENCY")

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


if __name__ == "__main__":
    """ Ensure this code only runs if the script is executed.
    Not when it's imported as a module by another file.
    """
    unittest.main()

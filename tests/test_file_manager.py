"""Test code."""

# Standard Library imports
from datetime import datetime
import unittest

# Third-party imports
import pytest

# Local imports
from src.file_manager import file_retention_management
from src.modules.file_manager_init import FileManagerInit


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


@pytest.mark.usefixtures("inject_helpers")
class TestJSON(unittest.TestCase):
    """Using Python's built-in unittest library, using subclass unittest.TestCase
    test methods are defined that start with the prefix test. Test our JSON reliability."""

    def test_json_SUCCESS(self):
        """Test that our config variables are being read correctly."""
        print("TESTED JSON CORRECT VALUES")

        # Make sure config variables have correct values.
        result_1 = self.test_json_setup_config_vars(
            9090,
            "localhost",
            0.5,
            "../test/logs/",
            FILE_MANAGER_INIT,
        )
        # Make sure json path variables have correct values.
        result_2 = self.test_json_setup_path_vars(
            "./test/test_data/Data_first",
            1,
            "./test/test_data/Data_next",
            1,
            FILE_MANAGER_INIT,
        )

        # Were the values in the json correct?
        if result_1 != result_2 and result_1:
            result = False
        else:
            result = True

        # Check if test passed.
        self.assertEqual(result, True)

    def test_json_FAIL(self):
        """Test that our config variables recognize incorrect values."""
        print("TESTED JSON NOT-CORRECT VALUES")

        # Make sure config variables have correct values.
        result_1 = self.test_json_setup_config_vars(
            8080,
            "lochost",
            5,
            "./test/logs/",
            FILE_MANAGER_INIT,
        )
        # Make sure json path variables have correct values.
        result_2 = self.test_json_setup_path_vars(
            "./test/test_data/Data_repars",
            12,
            "./test/test_data/Daa_epheeris",
            1,
            FILE_MANAGER_INIT,
        )

        # Were the values in the json correct?
        if result_1 != result_2 and result_1:
            result = False
        else:
            result = True

        # Check if test passed.
        self.assertEqual(result, True)


@pytest.mark.usefixtures("inject_helpers")
class TestCopy(unittest.TestCase):
    """Using Python's built-in unittest library, using subclass unittest.TestCase
    test methods are defined that start with the prefix test. Test we copy files correctly."""

    def test_first_data(self):
        """Test all borep files were copied correctly."""
        print("TESTED BOREP COPY FUNCTIONALITY")

        # Setup time.
        current_time = datetime.now()
        last_time_first = datetime.min

        # Create directories with test files to copy.
        self.test_data_create("./tests/test_data/Data_first", 3)
        self.test_data_create("./tests/test_data/Dest_first", 0)

        # Check if after copy both directories have same number of files in them.
        result = self.test_file_copied_management(
            "DATA_DIR",
            "./tests/test_data/Data_first",
            last_time_first,
            0,
            current_time.year,
            FILE_MANAGER_INIT,
        )

        # Check if test passed.
        self.assertEqual(result, True)

    def test_next_data(self):
        """Test all ep files were copied correctly."""
        print("TESTED EP COPY FUNCTIONALITY")

        # Setup time.
        current_time = datetime.now()
        last_time_eph = datetime.min

        # Create directories with test files to copy.
        self.test_data_create("./tests/test_data/Data_next_2026", 3)
        self.test_data_create("./tests/test_data/Dest_next_2026", 0)

        # Check if after copy both directories have same number of files in them.
        result = self.test_file_copied_management(
            "DATA_DIR",
            "./tests/test_data/Data_next_2026",
            last_time_eph,
            1,
            current_time.year,
            FILE_MANAGER_INIT,
        )

        # Check if test passed.
        self.assertEqual(result, True)


@pytest.mark.usefixtures("inject_helpers")
class TestRetention(unittest.TestCase):
    """Using Python's built-in unittest library, using subclass unittest.TestCase
    test methods are defined that start with the prefix test. Test we delete files correctly."""

    def test_first_retention(self):
        """Test we are deleting outdated borep files correctly."""
        print("TESTED BOREP RETENTION FUNCTIONALITY")

        # Setup time.
        current_time = datetime.now()

        # Call function from file_manager.py Delete files that are past leniency times.
        file_retention_management(0, FILE_MANAGER_INIT, current_time.year)

        # Test we are deleting outdated index 0 (first) files correctly.
        result = self.test_file_retention_management(0, FILE_MANAGER_INIT)

        # Check if test passed.
        self.assertEqual(result, True)

    def test_next_retention(self):
        """Test we are deleting outdated ep files correctly."""
        print("TESTED EP RETENTION FUNCTIONALITY")

        # Setup time.
        current_time = datetime.now()

        # Call function from file_manager.py Delete files that are past leniency times.
        file_retention_management(1, FILE_MANAGER_INIT, current_time.year)

        # Test we are deleting outdated index 1 (next) files correctly.
        result = self.test_file_retention_management(1, FILE_MANAGER_INIT)

        # Check if test passed.
        self.assertEqual(result, True)


if __name__ == "__main__":
    """ Ensure this code only runs if the script is executed.
    Not when it's imported as a module by another file.
    """
    unittest.main()

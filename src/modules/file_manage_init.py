"""Setup File manager class."""

# Standard Library Imports
import json
from pathlib import Path
import socket

# Local Imports
from modules.log_manager import LogManager


class FileManagerInit:
    """Get file_manager setup.
    
    Attributes:
        red (int):                 Integer representation of bad health.
        yellow (int):              Integer representation of degraded health.
        green (int):               Integer representation of good health.
        data_dir (str | Path):     directories of all data to be copied over and managed.
        conf (str | Path):         path of config file.
        nas_dir (str | Path):      path of NAS directory.
        log_file (str | Path):     path of log file.
        message_dir (str | Path):  path of message directory.
        year (int):                year of files creations.
        seconds_per_min (int):     Number of seconds in a minute (60).
        failure_period_time (int): 
        freq_checks (Number):      
        seconds_per_min (int):     
        configs (dict): 
    """

    def __init__(self, json_file: Path | str) -> None:
        """Class that initializes variables for file manager to run.
    
        Args:
            json_file (Path | str): file path json will be read from. 
        """
        # Health variables
        self.red = 0
        self.yellow = 1
        self.green = 2

        # Sections
        self.data_dir = 'DATA_PATHS'
        self.conf = 'CONFIG_VARS'

        # Config variables
        self.nas_dir = 'NAS_DIR'
        self.log_file = 'LOGFILE_PATH'
        self.message_dir = 'DATA_DIR'
        self.year = 'YEAR'

        # Leniency variables
        self.seconds_per_min = 60
        self.failure_period_time = 10
        self.freq_checks = 'FREQUENCY_CHECKS'
        
        # config data.
        self.configs = self.json_parse(self.CONFIG, json_file)
        self.paths = self.json_parse(self.DATA_DIR, json_file)

        # get logfile configured.
        self.logfile_txt = self.configs.get(self.LOGFILE)
        self.log_manager = LogManager(self.logfile_txt)
        self.logger = self.log_manager.log_setup(self.logfile_txt)

        # connect to socket once initialized.
        self.port = self.configs.get('PORT')
        self.host = self.configs.get('HOST')

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))

    def json_parse(config_var: dict, json_file: Path | str) -> dict:
        """Read all the values from the json config file to use in app.

        Args:
            config_var (dict): Python object of all values from config variables.
            json_file (Path | str): file path json will be read from.

        Returns:
            (dict)  of all values from config variables.
        """
        # Open and read JSON file.
        with open(json_file, 'r') as config_file_path:
            data = config_file_path.read()

            # load data into python dictionary.
            obj = json.loads(data)
            config_variables = obj[config_var]

            # close the file because it already read.
            config_file_path.close()

        return config_variables
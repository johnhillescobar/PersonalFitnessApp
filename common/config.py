#import os

#DB_HOST = os.environ.get('DB_HOST')
#DB_PORT = os.environ.get('DB_PORT')
# DB_NAME = os.environ.get('DB_NAME')
# DB_USER = os.environ.get('DB_USER')
# DB_PASSWORD = os.environ.get('DB_PASSWORD')

from functools import lru_cache
from pyhocon import ConfigFactory

conf = ConfigFactory.parse_file("./conf/application.conf").with_fallback("./conf/dev_data.conf")

class ConfigConstant:
    """
    Get config attributes.

    Inputs:
        None

    Outputs:
        None
    
    """

    def __init__(self):
        self.db_host = conf.get("DB_HOST")
        self.db_port = conf.get("DB_PORT")
        self.db_name = conf.get("DB_NAME")
        self.db_user = conf.get("DB_USER")
        self.db_password = conf.get("DB_PASSWORD")

    @lru_cache()
    def get_config_instance():
        """
        Instantiate ConfigConstant class.

        Inputs:
        None

        Outputs:
            ConfigConstant object
        """

        return ConfigConstant()

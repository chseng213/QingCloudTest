# encoding: utf-8
import json
import os

from main.utils import BASE_DIR, file_writer
from main.utils.errors import BadParameterException, ConfigException


class ArgsValidator(object):
    """
    command line args validator
    """

    @classmethod
    def validator(cls, params):
        try:
            return json.loads(params)
        except json.decoder.JSONDecodeError:
            return BadParameterException(4, 'json args need to be in format JSON STRING')


class ConfigFileValidator(object):
    """
    validate config params
    """

    @classmethod
    def validator(cls, file):
        """
        create config_temp.py file ,read user config and validate
        :param file:
        :return:
        """
        return_obj = 0
        temp_config_path = os.path.join(BASE_DIR, "config_temp.py")
        config_path = "config.py"
        new_config = (file.name != config_path)
        if new_config:
            file_writer(file, temp_config_path)
        missing_params_info = "config file missing required params,they are qy_secret_access_key, qy_access_key_id, zone"
        not_string_info = "The configured params must be a string type"
        try:
            if new_config:
                from config_temp import qy_secret_access_key, qy_access_key_id, zone
            else:
                from config import qy_secret_access_key, qy_access_key_id, zone
            if not (isinstance(qy_access_key_id, str)
                    and isinstance(qy_access_key_id, str)
                    and isinstance(zone, str)):
                return_obj = ConfigException(3, not_string_info)
            # rename config file
            with open(temp_config_path) as f:
                file_writer(f, config_path) if new_config else 0
        except ImportError:
            return_obj = ConfigException(2, missing_params_info)
        except Exception as e:
            return_obj = ConfigException(-1, str(e))
        finally:
            return return_obj


if __name__ == '__main__':
    ArgsValidator.validator("d[]s")

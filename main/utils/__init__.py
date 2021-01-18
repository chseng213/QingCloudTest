import os
import sys

import click

from main.utils.errors import ConfigException

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# help string
config_help_str = """
When you have not edited the configuration file `config.py`,you need to specify the configuration file,like `/etc/qingcloud/config.py` and file  content should configure your own qy_access_key_id , qy_secret_access_key and zone

such as:


qy_access_key_id='YOUR-ACCESS-KEY'
qy_secret_access_key='YOUR-SECRET-ACCESS-KEY'
zone='sh1'  
"""
json_option_help_str = """
Use string  in  json format to send some not required Parameters,Parameters that do not exist in the document will be filtered

such as :

'{
"vxnets.1": "vxnet-0",

"instance_type": "e2.small.r1",

"instance_name": "demo",

"image_id": "centos64x86a",

"login_mode": "passwd",

"login_passwd": "QingCloud20130712"
}'
"""
instances_n_help_str = """
instance id is required ,can send multiple,

such as :

-i instances-id -i instances-id ...
"""
image_id_n_help_str = """
image_id ,can send multiple,

such as :

-id image-id -id image-idd ...
"""
instance_type_n_help_str = """
instance_type ,can send multiple,

such as :

-t small.1 -t large.2 ...
"""
direct_cease_help_str = """
Whether to destroy the host directly, if you specify "1", it will not enter the recycle bin and destroy it directly, the default is "0"
"""
login_help_str = "needed when your chosen login mode is %s"


# Python version recognition
def get_version():
    """
    get python interpreter  version
    :return: 2 or 3
    """

    return 3 if sys.version > '3' else 2


PYTHON_VERSION = get_version()


def file_writer(source_file, target_file):
    """
    read source file content to write target file
    :param source_file:file object
    :param target_file:file path
    :return:
    """
    try:
        with click.open_file(target_file, "w", encoding="utf-8") as f:
            f.write(source_file.read())
    except Exception as e:
        raise ConfigException("file io error %s" % str(e))

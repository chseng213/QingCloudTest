# encoding: utf-8
"""
ErrorCode  and  meanings
-1  unknown Error
1   config file not found
2   config params not contain   qy_secret_access_keya and  qy_access_key_id and  zone
3   The configured params must be a string type
4   json args error
5   TerminateInstances action should specify one or more instances id'
"""


class ExitMessage(object):
    def __init__(self, error_code, error_info):
        self.error_code = error_code
        self.error_info = error_info

    def __str__(self):
        return 'The program exits abnormally. ErrorCode:%s\tErrorMessage:%s' % (self.error_code, self.error_info)

    def __repr__(self):
        return 'The program exits abnormally. ErrorCode:%s\tErrorMessage:%s' % (self.error_code, self.error_info)


class RequestsException(ExitMessage):
    """
    request exception to receive error code and msg
    """
    pass


class ConfigException(ExitMessage):
    pass


class JsonArgsException(ExitMessage):
    pass


class BadParameterException(ExitMessage):
    pass

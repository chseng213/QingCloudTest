# encoding: utf-8


class RequestsException(Exception):
    """
    request exception to receive error code and msg
    """

    def __init__(self, error_code, error_info):
        """

        :param error_code: last time requests code  or api return code
        :param error_info: error information   or  api  return message
        """
        super().__init__(self)
        self.error_code = error_code
        self.error_info = error_info

    def __str__(self):
        return 'ErrorCode:%s\tErrorMessage:%s' % (self.error_code, self.error_info)


class ConfigException(Exception):
    def __init__(self, error_info, error_code=-1):
        """

        :param error_code:
        :param error_info: error information
        """
        super().__init__(self)
        self.error_code = error_code
        self.error_info = error_info

    def __str__(self):
        return 'ErrorCode:%s\tErrorMessage:%s' % (self.error_code, self.error_info)


class JsonArgsException(Exception):
    def __init__(self, error_info, error_code=-2):
        """

        :param error_code:
        :param error_info: error information
        """
        super().__init__(self)
        self.error_code = error_code
        self.error_info = error_info

    def __str__(self):
        return 'ErrorCode:%s\tErrorMessage:%s' % (self.error_code, self.error_info)

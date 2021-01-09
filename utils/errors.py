# encoding: utf-8

class RequestsException(Exception):
    """
    自定义异常类接受code以及msg
    """

    def __init__(self, error_code, error_info):
        """

        :param error_code: 请求异常code  或者api返回的错误code
        :param error_info: 请求异常消息   或者api返回的错误msg
        """
        super().__init__(self)
        self.error_code = error_code
        self.error_info = error_info

    def __str__(self):
        return 'ErrorCode:%s\tErrorMessage:%s' % (self.error_code, self.error_info)

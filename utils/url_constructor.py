# encoding: utf-8
import base64
import hmac
from urllib.parse import quote_plus
from hashlib import sha256


class URLConstructor(object):
    """
    接口地址生成器,用于加签,以及uri拼接
    """

    def __init__(self, secret_access_key):
        self.secret_access_key = secret_access_key

    def get_str_to_sign(self, request_str):
        """
        todo uri对应action动态获取
        :param request_str:
        :return:
        """
        str_to_sign = "GET\n/iaas/\n" + request_str
        return quote_plus(str_to_sign, encoding='utf-8')

    def get_signature(self, str_to_sign):
        """
        参数加签
        :param str_to_sign:
        :return:
        """
        h = hmac.new(self.secret_access_key, digestmod=sha256)
        h.update(str_to_sign)
        sign = base64.b64encode(h.digest()).strip()
        signature = quote_plus(sign, encoding='utf-8')
        return signature


if __name__ == '__main__':
    pass

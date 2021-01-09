# encoding: utf-8

import requests

from utils.errors import RequestsException


class Request(object):
    """
    自定义请求,请求失败可重试3次
    """
    MAX_TRY = 3

    def __init__(self, session=None, timeout=5):
        """

        :param session: requests session 对象  default:新建session对象
        :param timeout: 请求超时时间 default:5S
        """
        if session is None:
            session = requests.session()
        self.session = session
        self.timeout = timeout

    def get(self, url):
        """

        :param url: 通过构造器生成的url
        :return:   json data or raise RequestsException
        """
        requests_num = 0
        connect_num = 0
        code = 0
        res = {}
        for _ in range(self.MAX_TRY):
            try:
                res = self.session.get(url, timeout=self.timeout).json()
                code = res.status_code
                break
            except requests.exceptions.ConnectionError:
                connect_num += 1
            except requests.exceptions.RequestException:
                requests_num += 1
        # 3次请求失败   raise Exception
        assert code == 200, RequestsException(code,
                                              "ConnectionError:%s\tRequestError:%s" % (code,
                                                                                       connect_num,
                                                                                       requests_num))
        # 当返回码为错误码时 raise Exception
        assert res.get("ret_code") == 0, RequestsException(res.get("ret_code"), res.get("message"))
        return res

# encoding: utf-8

import requests


class Request(object):
    """
    Simple package requests
    """
    MAX_RETRY = 3

    def __init__(self, session=None, timeout=5):
        """

        :param session: requests session object  default:new session obj
        :param timeout: requests timeout  default:5S
        """
        if session is None:
            session = requests.session()
        self.session = session
        self.timeout = timeout

    def get(self, url):
        """
        http get method and raise exception where result does not meet expectations
        :param url: api url
        :return:   json data or raise RequestsException
        """
        requests_num = 0
        connect_num = 0
        code = 0
        response = {}
        for _ in range(self.MAX_RETRY):
            try:
                response = self.session.get(url, timeout=self.timeout)
                code = response.status_code
                break
            except requests.exceptions.ConnectionError:
                connect_num += 1
            except requests.exceptions.RequestException:
                requests_num += 1
        # max  three times to request,   raise Exception
        assert code == 200, "ConnectionError:%s\tRequestError:%s" % (connect_num, requests_num)
        #  raise Exception  where  ret_code is not equal 0
        assert response.json().get("ret_code") == 0, response.json().get("message")
        return response

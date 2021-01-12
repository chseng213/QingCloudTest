# encoding: utf-8
import time
import unittest

import requests

from config import qy_access_key_id, qy_secret_access_key, zone
from main.utils.url_constructor import URLConstructor

url_constructor = URLConstructor(qy_secret_access_key, qy_access_key_id, zone)


class URLConstructorTestCase(unittest.TestCase):
    MAX_RETRY = 3

    def test_get_url(self):
        action = "RunInstances"
        params = {
            "vxnets.1": "vxnet-0",
            "instance_type": "e2.small.r1",
            "signature_method": "HmacSHA256",
            "instance_name": "demo",
            "image_id": "centos64x86a",
            "login_mode": "passwd",
            "login_passwd": "QingCloud20130712",
        }
        url = url_constructor.build_url(action, params)
        try_count = 0
        response = {}
        while try_count < self.MAX_RETRY:
            try:
                response = requests.get(url).json()
                break
            except Exception:
                try_count += 1
                time.sleep(2)
        self.assertEqual(response['ret_code'], 0)


if __name__ == '__main__':
    unittest.main()

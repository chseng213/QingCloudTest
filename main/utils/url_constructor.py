# encoding: utf-8
import base64
import datetime
import hmac

from hashlib import sha256

from main.utils import PYTHON_VERSION

if PYTHON_VERSION == 3:
    from urllib.parse import quote_plus
else:
    from urllib import quote_plus


class URLConstructor(object):
    """
    api url constructor, define signature function,and uri format
    """
    BASE_URL = "https://api.qingcloud.com/iaas/?"

    def __init__(self, secret_access_key, access_key_id, zone):
        self.secret_access_key = secret_access_key
        self.access_key_id = access_key_id
        self.zone = zone

    def common_params(self, action):
        """
         return  api  common params
        :param action: contain three instance actions
        :return:
        """
        return {
            "action": action,
            "zone": self.zone,
            "access_key_id": self.access_key_id,
            "version": 1,
            "time_stamp": self.get_time_stamp(),
            "signature_version": 1,
            "signature_method": "HmacSHA256",
        }

    @classmethod
    def structure_request_str(cls, params):
        """
         sorted params and  structure http query args use & and =
        :param params: params dict
        :return: request string
        """
        sorted_params = sorted(params.items(), key=lambda x: x[0])
        request_str = "&".join(["%s=%s" % (quote_plus(key),
                                           quote_plus(str(value)))
                                for key, value in sorted_params
                                ])
        return request_str

    @classmethod
    def get_str_to_sign(cls, request_str, uri="iaas"):
        """
        get string to sign
        :param request_str: sorted params and use "&","=" splicing
        :param uri:
        :return: string  to sign
        """
        return "GET\n/%s/\n%s" % (uri, request_str)

    def get_signature_3(self, str_to_sign):
        """
        request params signature
        :param str_to_sign:
        :return:
        """
        h = hmac.new(self.secret_access_key.encode('utf-8'), digestmod=sha256)
        h.update(str_to_sign.encode('utf-8'))
        sign = base64.b64encode(h.digest()).strip()
        signature = quote_plus(sign.decode('utf-8'), encoding="utf-8")
        return signature

    def get_signature_v2(self, str_to_sign):
        h = hmac.new(self.secret_access_key, digestmod=sha256)
        h.update(str_to_sign)
        sign = base64.b64encode(h.digest()).strip()
        signature = quote_plus(sign)
        return signature

    def get_signature(self, str_to_sign):
        """
        request params signature
        :param str_to_sign:
        :return:
        """
        if PYTHON_VERSION == 3:
            return self.get_signature_3(str_to_sign)
        else:
            return self.get_signature_v2(str_to_sign)

    @classmethod
    def get_time_stamp(cls):
        """
        return  utc time string  ( string format : YYYY-MM-DDThh:mm:ssZ)
        :return:
        """
        utc_now = datetime.datetime.utcnow()
        time_stamp_str = utc_now.strftime("%Y-%m-%dT%TZ")
        return time_stamp_str

    def build_url(self, action, params):
        """
        structure request url
        :param action:
        :param params: required params
        :return:
        """
        request_args = self.common_params(action)
        # extend  required params
        request_args.update(params)
        request_str = self.structure_request_str(request_args)
        str_to_sign = self.get_str_to_sign(request_str)
        signature = self.get_signature(str_to_sign)
        return self.BASE_URL + request_str + "&signature=%s" % signature


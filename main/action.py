# encoding: utf-8

import click

from main.utils import exit_with_request_error
from main.utils.errors import BadParameterException, ExitMessage
from main.utils.request import Request
from main.utils.url_constructor import URLConstructor
from main.utils.validator import ArgsValidator

try:
    from config import qy_secret_access_key, qy_access_key_id, zone
except:
    click.echo("CONFIG FILE NEED SPECIFY")
    qy_secret_access_key, qy_access_key_id, zone = "", "", ""


class Action(object):
    QY_SECRET_ACCESS_KEY = qy_secret_access_key
    QY_ACCESS_KEY_ID = qy_access_key_id
    ZONE = zone
    action = ""
    valid_json_args = []

    @staticmethod
    def multi_value_params(params, key_worlds):
        """

        :param params:
        :param key_worlds:
        :return:
        """
        values = params.get(key_worlds)
        if values:
            params.update({key_worlds + ".%s" % i: value for i, value in enumerate(values, 1) if value})
            params.pop(key_worlds)

    def get_params(self, params):
        params.update(action=self.action)
        # value is `0` will be removed
        # return {key: value for key, value in params.items() if value}
        return params

    def validate_json_args(self, params):
        json_args = params.get("json_args", {})
        # validate json args
        if json_args:
            option_args = ArgsValidator.validator(json_args)
            option_args = {key: value for key, value in option_args.items() if
                           key in self.valid_json_args and value}
            params.pop("json_args")
            params.update(option_args)
        return params

    def params_after_verification(self, params):
        pass

    def build_url(self, params):
        url_constructor = URLConstructor(self.QY_SECRET_ACCESS_KEY, self.QY_ACCESS_KEY_ID, self.ZONE)
        url = url_constructor.build_url(self.action, params)
        return url

    def run(self, params):
        request = Request()
        try:
            validated_result = self.params_after_verification(params)
            if isinstance(validated_result, ExitMessage):
                exit_with_request_error(validated_result)
            params = self.get_params(validated_result)
            url = self.build_url(params)
            response = request.get(url)
            click.echo(response.text)
            return response
        except Exception as e:
            exit_with_request_error(ExitMessage(-1, str(e)))


class RunInstanceAction(Action):
    action = "RunInstances"

    def params_after_verification(self, params):
        # validate json args
        # params = self.validate_json_args(params)

        # Choose login method and corresponding parameters
        login_mode = params.get("login_mode")
        if login_mode == "keypair":
            if not params.get("login_keypair"):
                return BadParameterException(6, "keypair login mode should specify login_keypair")

        elif login_mode == "passwd":
            if not params.get("login_passwd"):
                return BadParameterException(6, "passwd login mode should specify login_passwd")
        else:
            return BadParameterException(6, "login_mode only `keypair` or `passwd`")

        # Choose instance type or cpu and memory
        instance_type = params.get("login_mode")
        if not instance_type:
            if not (params.get("cpu") and params.get("memory")):
                return BadParameterException(6, "if  not specify `instance_type`,`cpu` and `memory` are needed ")

        # vxnets
        self.multi_value_params(params, "vxnets")
        # vxnets = params.get("vxnet")
        # if vxnets:
        #     params.update({"vxnets.%s" % i: value for i, value in enumerate(vxnets, 1) if value})
        #     params.pop("vxnet")

        return params


class DescribeInstanceAction(Action):
    action = "DescribeInstances"

    def params_after_verification(self, params):
        # validate json args
        # params = self.validate_json_args(params)

        # instances.n
        self.multi_value_params(params, "instances")
        # instances = params.get("instances")
        # if instances:
        #     params.update({"instances.%s" % i: value for i, value in enumerate(instances, 1) if value})
        #     params.pop("instances")

        # image_id.n
        self.multi_value_params(params, "image_id")
        # image_id_list = params.get("image_id")
        # if image_id_list:
        #     params.update({"image_id.%s" % i: value for i, value in enumerate(image_id_list, 1) if value})
        #     params.pop("image_id")

        # instance_type.n
        self.multi_value_params(params, "instance_type")
        # instance_type_list = params.get("instance_type")
        # if instance_type_list:
        #     params.update({"instance_type.%s" % i: value for i, value in enumerate(instance_type_list, 1) if value})
        #     params.pop("instance_type")

        # status.n
        self.multi_value_params(params, "status")
        # status_list = params.get("status")
        # if status_list:
        #     params.update({"status.%s" % i: value for i, value in enumerate(status_list, 1) if value})
        #     params.pop("status")

        # tags.n
        self.multi_value_params(params, "tags")
        # tags = params.get("tags")
        # if tags:
        #     params.update({"tags.%s" % i: value for i, value in enumerate(tags, 1) if value})
        #     params.pop("tags")

        return params


class TerminateInstanceAction(Action):
    action = "TerminateInstances"

    def params_after_verification(self, params):
        instances = params.get("instances")
        if instances:
            params.update({"instances.%s" % i: value for i, value in enumerate(instances, 1) if value})
            params.pop("instances")
        else:
            return BadParameterException(5, 'TerminateInstances action should specify one or more instances id')
        return params

# encoding: utf-8
import sys

import click

from main.utils.errors import RequestsException
from main.utils.request import Request
from main.utils.url_constructor import URLConstructor

from main.utils.validator import ArgsValidator

try:
    from config import qy_secret_access_key, qy_access_key_id, zone
except Exception:
    click.echo("CONFIG FILE NEED SPECIFY")
    qy_secret_access_key, qy_access_key_id, zone = "", "", ""


class Action(object):
    QY_SECRET_ACCESS_KEY = qy_secret_access_key
    QY_ACCESS_KEY_ID = qy_access_key_id
    ZONE = zone
    action = ""
    valid_json_args = []

    def exit_with_request_error(self, error):
        # use click echo can  compatible with different python versions
        click.echo(error.error_info)
        sys.exit(1)

    def exit_with_params_error(self, error):
        click.echo(error.message)
        sys.exit(1)

    def exit_with_unkown_error(self, error):
        click.echo(str(error))
        sys.exit(1)

    def get_params(self, params):
        params.update(action=self.action)
        return {key: value for key, value in params.items() if value}

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
            params = self.get_params(self.params_after_verification(params))
            url = self.build_url(params)
            response = request.get(url)
            click.echo(response.text)
            return response
        except RequestsException as e:
            self.exit_with_request_error(e)
        except click.BadParameter as e:
            self.exit_with_params_error(e)
        except AssertionError as e:
            self.exit_with_unkown_error(e)
        except Exception as e:
            self.exit_with_unkown_error(e)


class RunInstanceAction(Action):
    action = "RunInstances"

    valid_json_args = [
        "os_disk_size",
        "hostname",
        "need_newsid",
        "instance_class",
        "cpu_model",
        "gpu",
        "gpu_class",
        "need_userdata",
        "userdata_type",
        "userdata_value",
        "userdata_path",
        "userdata_file",
        "target_user",
        "dedicated_host_group_id",
        "dedicated_host_id",
        "instance_group",
        "hypervisor",
        "os_disk_encryption",
        "cipher_alg",
        "months",
        "auto_renew",
    ]

    def params_after_verification(self, params):
        # validate json args
        params = self.validate_json_args(params)

        # Choose login method and corresponding parameters
        login_mode = params.get("login_mode")
        if login_mode == "keypair":
            assert params.get("login_keypair"), "keypair login mode should specify login_keypair"
        elif login_mode == "passwd":
            assert params.get("login_passwd"), "passwd login mode should specify login_passwd"
        else:
            raise click.BadParameter("login_mode only `keypair` or `passwd`")

        # Choose instance type or cpu and memory
        instance_type = params.get("login_mode")
        if not instance_type:
            assert params.get("cpu") and params.get(
                "memory"), "if  not specify `instance_type`,`cpu` and `memory` are needed "

        # vxnets
        vxnets = params.get("vxnet")
        if vxnets:
            params.update({"vxnets.%s" % i: value for i, value in enumerate(vxnets, 1) if value})
            params.pop("vxnet")
        return params


class DescribeInstanceAction(Action):
    action = "DescribeInstances"
    valid_json_args = [
        "instance_class",
        "vcpus_current",
        "memory_current",
        "os_disk_size",
        "exclude_reserved",
        "search_word",
        "dedicated_host_group_id",
        "dedicated_host_id",
        "owner",
        "verbose",
        "offset",
        "limit",
    ]

    def params_after_verification(self, params):
        # validate json args
        params = self.validate_json_args(params)

        # instances.n
        instances = params.get("instances")
        if instances:
            params.update({"instances.%s" % i: value for i, value in enumerate(instances, 1) if value})
            params.pop("instances")

        # image_id.n
        image_id_list = params.get("image_id")
        if image_id_list:
            params.update({"image_id.%s" % i: value for i, value in enumerate(image_id_list, 1) if value})
            params.pop("image_id")

        # instance_type.n
        instance_type_list = params.get("instance_type")
        if instance_type_list:
            params.update({"instance_type.%s" % i: value for i, value in enumerate(instance_type_list, 1) if value})
            params.pop("instance_type")
        return params


class TerminateInstanceAction(Action):
    action = "TerminateInstances"

    def params_after_verification(self, params):
        instances = params.get("instances")
        if instances:
            params.update({"instances.%s" % i: value for i, value in enumerate(instances, 1) if value})
            params.pop("instances")
        else:
            raise click.BadParameter('TerminateInstances action should specify one or more instances id')
        return params

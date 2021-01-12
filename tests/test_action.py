# encoding: utf-8
import unittest

from main.action import RunInstanceAction, DescribeInstanceAction, TerminateInstanceAction


class RunInstanceActionTestCase(unittest.TestCase):
    run_instance = RunInstanceAction()

    def test_get_params(self):
        input_params = {
            "image_id": 'centos63x64',
            "instance_type": 'e2.small.r1',
            "instance_name": 'demo',
            "vxnets.1": '',
            "login_mode": "passwd",
            "login_passwd": "QingCloud20130712",
            "json_args": '{"os_disk_size":30}'
        }
        expected_params = {
            "action": 'RunInstances',
            "image_id": 'centos63x64',
            "instance_type": 'e2.small.r1',
            "instance_name": 'demo',
            "login_mode": "passwd",
            "login_passwd": "QingCloud20130712",
            "os_disk_size": 30
        }
        valid_params = self.run_instance.params_after_verification(input_params)
        output_params = self.run_instance.get_params(valid_params)
        self.assertEqual(set(output_params.items()), set(expected_params.items()))

    def test_run(self):
        params = {
            "image_id": 'centos56x64',
            "instance_type": 'e2.small.r1',
            "instance_name": 'demo',
            "vxnet": ("vxnet-0",),
            "login_mode": "passwd",
            "login_passwd": "QingCloud20130712",
            "json_args": '{"os_disk_size":20}'
        }
        result = self.run_instance.run(params)
        self.assertEqual(result.json().get("ret_code"), 0)


class DescribeInstanceActionTestCase(unittest.TestCase):
    describe_instance = DescribeInstanceAction()

    def test_get_params(self):
        input_params = {
            "instances": ('i-jsgr7li1',),
            "image_id": ('centos63x64',),
            "instance_type": ('e2.small.r1',),
            "json_args": '{"os_disk_size":30,"instance_class":201}'
        }
        expected_params = {
            "action": 'DescribeInstances',
            "instances.1": 'i-aa990tjt',
            "image_id.1": 'centos63x64',
            "instance_type.1": 'e2.small.r1',
            "os_disk_size": '30',
            "instance_class": '201',

        }
        valid_params = self.describe_instance.params_after_verification(input_params)
        output_params = self.describe_instance.get_params(valid_params)
        self.assertEqual(set(output_params.items()), set(expected_params.items()))

    def test_run(self):
        params = {
            "instances": ('i-jsgr7li1',),
            "image_id": ('centos63x64',),
            "instance_type": ('e2.small.r1',),
            "json_args": '{"os_disk_size":30,"instance_class":201}'
        }
        result = self.describe_instance.run(params)
        self.assertEqual(result.json().get("ret_code"), 0)


class TerminateInstanceActionTestCase(unittest.TestCase):
    terminate_instance = TerminateInstanceAction()

    def test_run(self):
        params = {
            "instances": ('i-jsgr7li1',),
        }
        result = self.terminate_instance.run(params)
        self.assertEqual(result.json().get("ret_code"), 0)


if __name__ == '__main__':
    unittest.main()

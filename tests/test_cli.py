# encoding: utf-8
import unittest

from click.testing import CliRunner

from main.cli import cli


class CLITestCase(unittest.TestCase):
    runner = CliRunner()

    def test_run_instances(self):
        result = self.runner.invoke(cli,
                                    ['run-instances', "centos56x64", "passwd", "-p", "Wasd54574@", "-T", "e2.small.r1",
                                     "-J", '{"os_disk_size":20}'])
        assert result.exit_code == 0
        assert '"ret_code":0' in result.output

    def test_describe_instances(self):
        result = self.runner.invoke(cli,
                                    ['describe-instances', "-m", "centos56x64", "-t", "e2.small.r1"])
        assert result.exit_code == 0
        assert '"ret_code":0' in result.output

    def test_terminate_instances(self):
        result = self.runner.invoke(cli,
                                    ['terminate-instances', "-i", "i-vxs8g1e9", "-i", ""])
        assert result.exit_code == 0
        assert '"ret_code":0' in result.output


if __name__ == '__main__':
    unittest.main()

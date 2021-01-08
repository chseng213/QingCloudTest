# encoding: utf-8
import click
import requests
from click.testing import CliRunner


@click.command()
def cli():
    """ get your ip address"""
    ip_json = requests.get("http://ip-api.com/json/").json()
    click.echo("your ip is %s" % ip_json.get("query"))


def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli)
    assert result.exit_code == 0
    ip_json = requests.get("http://ip-api.com/json/").json()
    assert result.output == 'your ip is %s\n' % ip_json.get("query")


if __name__ == '__main__':
    test_cli()

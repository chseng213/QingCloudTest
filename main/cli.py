# encoding: utf-8
import os

import click

from main.action import RunInstanceAction, DescribeInstanceAction, TerminateInstanceAction
from main.utils import BASE_DIR, ConfigException, config_help_str, json_option_help_str, instances_n_help_str, \
    image_id_n_help_str, instance_type_n_help_str, direct_cease_help_str, login_help_str
from main.utils.validator import ConfigFileValidator


@click.group()
@click.option('-f', "--file",
              type=click.File("r"),
              default=os.path.join(BASE_DIR, "config.py"),
              help=config_help_str,
              )
def cli(file):
    try:
        ConfigFileValidator.validator(file)
    except ConfigException as e:
        click.echo(e)


@cli.command(name="run-instances")
@click.argument("image_id", required=True, type=str)
@click.argument("login_mode", required=True, type=str)
@click.option("-k", "login_keypair", type=str, help=login_help_str % "keypair")
@click.option("-p", "login_passwd", type=str, help=login_help_str % "passwd")
@click.option("-T", "instance_type", type=str, help='qing cloud instance type')
@click.option("-C", "cpu", type=int, default=None, help='instance cpu, like 1,2...')
@click.option("-M", "memory", type=int, default=None, help='instance memory,like 1024,2048...')
@click.option("-N", "instance_name", type=str, default=None, help='instance name')
@click.option("-c", "count", type=int, default=1, help='create instance count, default 1')
@click.option("-vxnet", "vxnets", type=str, multiple=True, help='vxnets can send multiple')
@click.option("-J", "--json_args", type=str, help=json_option_help_str)
def run_instances(image_id, login_mode, login_keypair, login_passwd, instance_type,
                  cpu, memory, instance_name, count, vxnets, json_args):
    """action RunInstances :required params `image_id` `instance_type` `login_mode` ,
       other unnecessary params use json format string
    """
    params = locals()
    run_cli = RunInstanceAction()
    run_cli.run(params)


@cli.command(name="describe-instances")
@click.option("-i", "--instances", type=str, multiple=True,
              help=instances_n_help_str)
@click.option("-m", "--image_id", type=str, multiple=True,
              help=image_id_n_help_str)
@click.option("-t", "--instance_type", type=str, multiple=True,
              help=instance_type_n_help_str)
@click.option("-J", "--json_args", type=str, help=json_option_help_str)
def describe_instances(instances, image_id, instance_type, json_args):
    """action DescribeInstances"""
    params = locals()
    describe_cli = DescribeInstanceAction()
    describe_cli.run(params)


@cli.command(name="terminate-instances")
@click.option("-i", "--instances", type=str, multiple=True,
              help=instances_n_help_str)
@click.option("-d", "--direct_cease", type=int, default=0,
              help=direct_cease_help_str)
def terminate_instances(instances, direct_cease):
    """action TerminateInstances"""
    params = locals()
    terminate_cli = TerminateInstanceAction()
    terminate_cli.run(params)


if __name__ == '__main__':
    cli()

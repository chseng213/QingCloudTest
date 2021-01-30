# encoding: utf-8
import os

import click
from click.testing import CliRunner

from main.action import RunInstanceAction, DescribeInstanceAction, TerminateInstanceAction
from main.utils import BASE_DIR, config_help_str, json_option_help_str, instances_n_help_str, \
    image_id_n_help_str, instance_type_n_help_str, direct_cease_help_str, login_help_str, instance_class_help_str, \
    exit_with_request_error
from main.utils.errors import ExitMessage
from main.utils.validator import ConfigFileValidator


@click.group(invoke_without_command=True)
@click.option('-f', "--file",
              type=click.File("r"),
              default=os.path.join(BASE_DIR, "config.py"),
              help=config_help_str,
              )
@click.pass_context
def cli(ctx, file):
    if ctx.invoked_subcommand is None:
        result = CliRunner().invoke(cli, ["--help"])
        click.echo(result.output)

    validated_result = ConfigFileValidator.validator(file)
    if isinstance(validated_result, ExitMessage):
        exit_with_request_error(validated_result)


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
@click.option("-vxnets", "vxnets", type=str, multiple=True, help='vxnets can send multiple')
@click.option("-security_group", type=str, help="")
@click.option("-hostname", type=str, help="")
@click.option("-cpu_model", type=str, help="")
@click.option("-cpu_topology", type=str, help="")
@click.option("-userdata_type", type=str, help="")
@click.option("-userdata_value", type=str, help="")
@click.option("-userdata_path", type=str, help="")
@click.option("-userdata_file", type=str, help="")
@click.option("-target_user", type=str, help="")
@click.option("-hypervisor", type=str, help="")
@click.option("-cipher_alg", type=str, help="")
@click.option("-os_disk_encryption", type=bool, help="")
@click.option("-instance_group", type=str, help="")
@click.option("-dedicated_host_id", type=str, help="")
@click.option("-dedicated_host_group_id", type=str, help="")
@click.option("-need_newsid", type=int, help="")
@click.option("-instance_class", type=int, help="")
@click.option("-gpu", type=int, help="")
@click.option("-gpu_class", type=int, help="")
@click.option("-months", type=int, help="")
@click.option("-auto_renew", type=int, help="")
@click.option("-nic_mqueue", type=int, help="")
@click.option("-need_userdata", type=int, help="")
@click.option("-volumes", "volumes", type=str, multiple=True, help='')
def run_instances(image_id, login_mode, login_keypair, login_passwd, instance_type,
                  cpu, memory, instance_name, count, vxnets, security_group,
                  hostname, cpu_model, cpu_topology, userdata_type, userdata_value, userdata_path,
                  userdata_file, target_user, hypervisor, cipher_alg, os_disk_encryption, instance_group,
                  dedicated_host_id, dedicated_host_group_id, need_newsid, instance_class,
                  gpu, gpu_class, months, auto_renew, nic_mqueue, need_userdata, volumes
                  ):
    """action RunInstances

    :required params `image_id` `instance_type` `login_mode` ,
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
@click.option("--instance_class", type=int, help=instance_class_help_str)
@click.option("-C", "--vcpus_current", type=int, help="instance cpu, like 1,2...")
@click.option("-M", "--memory_current", type=int, help="instance memory,like 1024,2048...")
@click.option("-os_disk_size", type=int, help="instance disk size")
@click.option("-exclude_reserved", type=int,
              help="Whether to filter reserved instance, if it is 1, no reserved instance information is returned")
@click.option("-status", type=str, multiple=True,
              help="instance status like:pending, running, stopped, suspended, terminated, ceased")
@click.option("-tags", type=str, multiple=True, help="Filter by tag ID, only return resources bound to a tag")
@click.option("-search_word", type=str, help="Search keywords, support instance ID, instance name")
@click.option("-dedicated_host_group_id", type=str, help="Filter by dedicated instance unit")
@click.option("-dedicated_host_id", type=str, help="Filter by a instance in the dedicated instance group")
@click.option("-owner", type=str, help="Filter by user account, only return resources of the specified account")
@click.option("-verbose", type=int,
              help="Whether to return lengthy information, if it is 1, then return the detailed data of other resources related to the instance.")
@click.option("-offset", type=int, default=0,help="Data offset, default is 0")
@click.option("-limit", type=int,default=20, help="Return data length, default is 20, maximum is 100")
def describe_instances(instances, image_id, instance_type, instance_class,
                       vcpus_current, memory_current, os_disk_size, exclude_reserved,
                       status, tags, search_word, dedicated_host_group_id, dedicated_host_id,
                       owner, verbose, offset, limit
                       ):
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

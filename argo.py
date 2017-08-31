#!/usr/bin/env python
#       d8888 8888888b.   .d8888b.   .d88888b.  
#      d88888 888   Y88b d88P  Y88b d88P" "Y88b 
#     d88P888 888    888 888    888 888     888 :q
#    d88P 888 888   d88P 888        888     888
#   d88P  888 8888888P"  888  88888 888     888
#  d88P   888 888 T88b   888    888 888     888
# d8888888888 888  T88b  Y88b  d88P Y88b. .d88P
# d88P     888 888   T88b  "Y8888P88  "Y88888P"
#
#                         Trade Solutions GmbH


# !/usr/bin/env python
import argparse
import sys
import os
import webbrowser
import re
import commands
from os import path
from ConfigParser import SafeConfigParser

args = None
env = None
kibanaEndpoints = {
    'argo-api-production': "https://logit.io/a/fa6fb844-b91c-4ee5-b4d4-4f64d59196e2/s/0c5ec344-970f-4e0f-9352-06e02588b069/kibana/access",
    'argo-api-staging': "https://logit.io/a/fa6fb844-b91c-4ee5-b4d4-4f64d59196e2/s/3d5501fc-bcc3-441c-8c93-daee2cea366c/kibana/access",
}


def get_env_vars():
    global env
    raw = commands.getstatusoutput("eb printenv %s | grep -e '^ *[A-Z][A-Z].*'" % args.e)[1]
    p = re.compile('([A-Z_]+)\s*=\s*(.+)\n?')
    lines = raw.split('\n')
    tuples = [(m.group(1), m.group(2)) for l in lines for m in [p.search(l)] if m]
    env = {}
    for var in tuples:
        env[var[0]] = var[1]


def rails_console():
    print('Connecting to Beanstalk Environment: %s...' % args.e)
    os.system("eb ssh %s -c 'sudo su -c \"cd /var/app/current && rails c\" --login'" % args.e)


def db_dump():
    print('Fetching Environment Variables...')
    get_env_vars()
    out_file = args.o or (args.e + '.dump')
    print('Dumping RDS Database %s to %s...' % (args.e, out_file))
    os.system("pg_dump --dbname=postgresql://%s:%s@%s:5432/%s --format t -f %s" % (
        env['ARGO_API_DATABASE_USER'],
        env['ARGO_API_DATABASE_PASSWORD'],
        env['ARGO_API_DATABASE_ENDPOINT'],
        env['ARGO_API_DATABASE_NAME'],
        out_file))
    print('Done %s' % out_file)



def db_restore():
    in_file = args.i or (args.e + '.dump')
    print("Restoring %s to local database argo_api_development..." % in_file)
    os.system("dropdb argo_api_development && createdb argo_api_development && pg_restore -d argo_api_development %s" % in_file)
    print('Done!')

def db_sync():
    db_dump()
    # file is argo-api-env.dump


def kibana_open():
    webbrowser.open(kibanaEndpoints[args.e])


def call_func(f):
    m = sys.modules[__name__]
    func = getattr(m, f)
    func()


def rails_logs():
    print('Connecting to Beanstalk Environment: %s...' % args.e)
    os.system("eb ssh %s -c 'sudo su -c \"tail -f /var/app/support/logs/passenger.log \" --login'" % args.e)


def sidekiq_logs():
    print('Connecting to Beanstalk Environment: %s...' % args.e)
    os.system("eb ssh %s -c 'sudo su -c \"tail -f /var/app/current/log/sidekiq.log \" --login'" % args.e)


def validate_requirements():
    validate_ssh_key()
    # TODO:
    # 1. Validate presense of ~/.ssh/aws-eb-argo-api
    # 2. Validate presence of ~/.aws and profile [argo]
    # 3. Validate presense of pg_restore, pg_dump
    # 4. Validate presence of eb cli


def print_success(msg):
    print('[\033[1;32mOK\033[0m] %s' % msg)
def print_error(msg):
    print('[\033[31mERR\033[0m] %s' % msg)

def req_validate():
    print('Validating Requirements...')
    validate_requirements()
    validate_aws_config()
    validate_eb_cli()
    validate_postgresql()

def validate_ssh_key():
    context = "SSH Certificate"
    if path.isfile(path.expanduser('~/.ssh/aws-eb-argo-api')):
        print_success(context)
    else:
        print_error(context)


def validate_aws_config():
    context = "AWS Credentials"
    config_path = path.expanduser('~/.aws/credentials')
    if path.isfile(config_path):
        parser = SafeConfigParser()
        try:
            parser.read(config_path)
            if parser.get("argo", "aws_access_key_id") and parser.get("argo", "aws_secret_access_key"):
                print_success(context)
        except Exception:
            print_error(context)
    else:
        print_error(context)

def validate_eb_cli():
    context = "EB CLI Tool"
    if any(os.access(os.path.join(path, 'eb'), os.X_OK) for path in os.environ["PATH"].split(os.pathsep)):
        print_success(context)
    else:
        print_error(context)

def validate_postgresql():
    context = "PostgreSQL"
    if any(os.access(os.path.join(path, 'pg_dump'), os.X_OK) for path in os.environ["PATH"].split(os.pathsep)):
        print_success(context)
    else:
        print_error(context)

# def validate_postgresql():
#
# def validate_eb_cli():
#


def main():
    global args
    parser = argparse.ArgumentParser(
        prog='argo',
        epilog="Keep Confedential",
        formatter_class=argparse.RawTextHelpFormatter,
        description="""
        \033[34m
       d8888 8888888b.   .d8888b.   .d88888b.
      d88888 888   Y88b d88P  Y88b d88P" "Y88b
     d88P888 888    888 888    888 888     888
    d88P 888 888   d88P 888        888     888
   d88P  888 8888888P"  888  88888 888     888
  d88P   888 888 T88b   888    888 888     888
 d8888888888 888  T88b  Y88b  d88P Y88b. .d88P
d88P     888 888   T88b  "Y8888P88  "Y88888P"

                         Trade Solutions GmbH
                                 Made in ARGO
        \033[0m
    """
    )
    subparsers = parser.add_subparsers(dest='command')

    # db:dump
    db_dump = subparsers.add_parser('db:dump',
                                    description="Dump RDS database to a local file. note: doesn't work with production environment",
                                    help="Dump RDS database to a local file. note: doesn't work with production environment")
    db_dump.add_argument('-o', metavar='file',
                         help="Output dump file to save dump to. If not specified, dump will be saved in argo-api-[env].dump")

    # db:restore
    db_restore = subparsers.add_parser('db:restore',
                                       description="Restore postgresql dump to local db (argo_api_development)",
                                       help="Restore postgresql dump to local db (argo_api_development)")

    db_restore.add_argument('-i', metavar='file',
                            help="Source dump file to restore. If not specified, dump will be loaded from argo-api-[env].dump")

    # rails:console
    subparsers.add_parser('rails:console', description="Starts a rails console session to Beanstalk instance",
                          help="Starts a rails console session to Beanstalk instance")

    # rails:logs
    subparsers.add_parser('rails:logs',
                          description="Starts a tail session to rails app logs in the given environment",
                          help="Starts a tail session to rails app logs in the given environment")

    # sidekiq:logs
    subparsers.add_parser('sidekiq:logs',
                          description="Starts a tail session to sidekiq logs in the given environment",
                          help="Starts a tail session to sidekiq logs in the given environment")

    # kibana:open
    subparsers.add_parser('kibana:open',
                          description="Opens Kibana logs dashboard for the selected env. (argo-api-staging, argo-api-production)",
                          help="Opens Kibana logs dashboard for the selected env. (argo-api-staging, argo-api-production)")

    subparsers.add_parser('req:validate',
                          help="Validates that all requirements needed by the CLI tool are satisfied on your local machine ")
    # subparsers.add_parser('get:env:vars')
    parser.add_argument('-e', metavar="environment", default="argo-api-staging",
                        help="Beanstalk environment to run the commands on. (argo-api-production, argo-api-staging, ..etc)")
    args = parser.parse_args()

    # execute command
    command = args.command.replace(':', '_')
    call_func(command)


if __name__ == '__main__':
    main()

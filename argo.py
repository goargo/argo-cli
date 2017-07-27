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

args = None


def rails_console():
    print('Rails Console Called')
    os.system("eb ssh argo-api-staging -c 'sudo su -c \"cd /var/app/current && rails c\" --login'")


def db_dump():
    print('db:dump Called')
    print(args.o)
    os.system("eb ssh argo-api-staging -c 'sudo su -c \""
              " pg_dump --dbname=postgresql://$ARGO_API_DATABASE_USER:$ARGO_API_DATABASE_PASSWORD@$ARGO_API_DATABASE_ENDPOINT:5432/$ARGO_API_DATABASE_NAME"
              " --format t -f staging_dump"
              "\" --login'")


def call_func(f):
    m = sys.modules[__name__]
    func = getattr(m, f)
    func()


def rails_logs():
    os.system("eb ssh argo-api-staging -c 'sudo su -c \"tail -f /var/app/support/logs/passenger.log \" --login'")


def main():
    global args
    parser = argparse.ArgumentParser(prog='argo', description="command line tool for use in ARGO dev team",
                                     epilog="Keep Confedential")
    subparsers = parser.add_subparsers(dest='command')
    # rails:console
    subparsers.add_parser('rails:console', help="Starts a rails console session to Beanstalk instance")
    # db:dump
    db_dump = subparsers.add_parser('db:dump', help="Dump RDS database to a file")
    db_dump.add_argument('-o', metavar="file", help="Save dump output to file")
    # db:restore
    db_restore = subparsers.add_parser('db:restore', help="Restore postgresql dump to RDS")
    db_restore.add_argument('-i', metavar='file', help="Source dump file to restore")
    # rails:logs
    rails_logs = subparsers.add_parser('rails:logs', help="Starts a tail session to rails app logs")

    parser.add_argument('-e', metavar="environment", default="argo-api-staging",
                        help="Beanstalk environment to run the commands on")

    args = parser.parse_args()
    print(args)
    command = args.command.replace(':', '_');
    call_func(command)


if __name__ == '__main__':
    main()

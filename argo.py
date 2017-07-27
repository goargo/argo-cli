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

args = None
kibanaEndpoints = {
    'argo-api-production': "https://logit.io/a/fa6fb844-b91c-4ee5-b4d4-4f64d59196e2/s/0c5ec344-970f-4e0f-9352-06e02588b069/kibana/access",
    'argo-api-staging': "https://logit.io/a/fa6fb844-b91c-4ee5-b4d4-4f64d59196e2/s/3d5501fc-bcc3-441c-8c93-daee2cea366c/kibana/access",
}

def rails_console():
    print('Rails Console Called')
    os.system("eb ssh %s -c 'sudo su -c \"cd /var/app/current && rails c\" --login'" % args.e)


def db_dump():
    print('db:dump Called')
    os.system("""
        eb ssh %s -c 'sudo su -c \"
           pg_dump --dbname=postgresql://$ARGO_API_DATABASE_USER:$ARGO_API_DATABASE_PASSWORD@$ARGO_API_DATABASE_ENDPOINT:5432/$ARGO_API_DATABASE_NAME
            --format t -f %s.dump
        \" --login'
      """ % (args.e, args.e))


def kibana_open():
    webbrowser.open(kibanaEndpoints[args.e])

def call_func(f):
    m = sys.modules[__name__]
    func = getattr(m, f)
    func()


def rails_logs():
    os.system("eb ssh %s -c 'sudo su -c \"tail -f /var/app/support/logs/passenger.log \" --login'" % args.e)

def sidekiq_logs():
    os.system("eb ssh %s -c 'sudo su -c \"tail -f /var/app/current/log/sidekiq.log \" --login'" % args.e)


def main():
    global args
    parser = argparse.ArgumentParser(prog='argo', description="command line tool for use in ARGO dev team",
                                     epilog="Keep Confedential")
    subparsers = parser.add_subparsers(dest='command')

    # rails:console
    subparsers.add_parser('rails:console', help="Starts a rails console session to Beanstalk instance")

    # db:dump
    db_dump = subparsers.add_parser('db:dump', help="Dump RDS database to a file")

    # db:restore
    # db_restore = subparsers.add_parser('db:restore', help="Restore postgresql dump to RDS")
    # db_restore.add_argument('-i', metavar='file', help="Source dump file to restore")

    # rails:logs
    rails_logs = subparsers.add_parser('rails:logs', help="Starts a tail session to rails app logs in the given environment")


    # kibana:open
    subparsers.add_parser('kibana:open', help="Opens Kibana logs dashboard for the selected env. (argo-api-staging, argo-api-production)")


    # sidekiq:logs
    subparsers.add_parser('sidekiq:logs', help="Starts a tail session to sidekiq logs in the given environment")

    parser.add_argument('-e', metavar="environment", default="argo-api-staging",
                        help="Beanstalk environment to run the commands on")
    args = parser.parse_args()
    print(args)
    command = args.command.replace(':', '_')
    call_func(command)


if __name__ == '__main__':
    main()

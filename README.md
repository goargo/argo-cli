CLI tool to be used by ARGO developers, This tool was written in hopes to save the dev team time by having these
commands as shortcuts to repetitive workflows we have internally.

## Requirements
- Python must be installed
- Elastic beanstalk cli tool has to be installed. Installation instructions http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install.html
- SSH certificate must be in position (~/.ssh/aws-eb-argo-api). Certificate can be found on `argo-secrets` bucket in S3
- ~/.aws/credentials must have `argo` profile with your IAM access key and secret key from AWS. eg
```
[argo]
aws_access_key_id = ***************
aws_secret_access_key = *************
```

## Installation

```
git clone https://github.com/goargo/argo-cli /tmp/argo-cli && chmod +x /tmp/argo-cli/argo.py && sudo cp /tmp/argo-cli/argo.py /usr/local/bin/argo && rm -rf /tmp/argo-cli
```

# Validate Requirements
To make sure you have all the requirements. Run
```
argo req:validate
```

## Commands
```
$ argo -h
usage: argo [-h] [-e environment]
            {db:dump,db:restore,rails:console,rails:logs,sidekiq:logs,kibana:open,req:validate}
            ...

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


positional arguments:
  {db:dump,db:restore,rails:console,rails:logs,sidekiq:logs,kibana:open,req:validate}
    db:dump             Dump RDS database to a local file. note: doesn't work with production environment
    db:restore          Restore postgresql dump to local db (argo_api_development)
    rails:console       Starts a rails console session to Beanstalk instance
    rails:logs          Starts a tail session to rails app logs in the given environment
    sidekiq:logs        Starts a tail session to sidekiq logs in the given environment
    kibana:open         Opens Kibana logs dashboard for the selected env. (argo-api-staging, argo-api-production)
    req:validate        Validates that all requirements needed by the CLI tool are satisfied on your local machine

optional arguments:
  -h, --help            show this help message and exit
  -e environment        Beanstalk environment to run the commands on

Keep Confedential
```
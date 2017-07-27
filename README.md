CLI tool to be used by ARGO developers, This tool was written in hopes to save the dev team time by having these
commands as shortcuts to repetitive workflows we have internally.

# Requirements
- Elastic beanstalk cli tool has to be installed. Installation instructions http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install.html
- SSH certificate must be in position (~/.ssh/aws-eb-argo-api). Certificate can be found on `argo-secrets` bucket in S3
- ~/.aws must have `argo` profile with your IAM access key and secret key from AWS
- Python must be installed

# Installation
```
cd /tmp && git clone https://github.com/goargo/argo-cli && cd argo-cli
chmod +x argo.py
sudo cp argo.py /usr/bin/argo
```

# Commands
```
api master 🐷   argo --help
usage: argo [-h] [-e environment]
            {rails:console,db:dump,db:restore,rails:logs} ...

command line tool for use in ARGO dev team

positional arguments:
  {rails:console,db:dump,db:restore,rails:logs}
    rails:console       Starts a rails console session to Beanstalk instance
    db:dump             Dump RDS database to a file
    db:restore          Restore postgresql dump to RDS
    rails:logs          Starts a tail session to rails app logs

optional arguments:
  -h, --help            show this help message and exit
  -e environment        Beanstalk environment to run the commands on

Keep Confedential
```
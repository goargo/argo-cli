CLI tool to be used by ARGO developers

# Requirements
- Elastic beanstalk cli tool has to be installed
- SSH certificate must be in position (~/.ssh/aws-eb-argo-api)
- ~/.aws must have `argo` profile with your IAM access key and secret key from AWS
- Python must be installed

# Installation
```
sudo curl URL > /usr/bin/argo
sudo chmod +x /usr/bin/argo

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
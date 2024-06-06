# This script creates and deploys resources for the Q Custom Connector workshop.
# It creates an ECR repository using boto3, builds the data source container image, 
# and pushes the resulting image to ECR. It then deploys the CDK stack to launch the
# data source container as a Fargate ECS service.
#
# Options: 
# -a, --acct_id  Target AWS Acct ID 
# -r, --region   Target AWS Region
#
#

import boto3
import shutil
import os
import argparse
import logging
import subprocess
from rich_argparse import RichHelpFormatter
from rich.logging import RichHandler
from botocore.exceptions import ClientError
from botocore.config import Config
import re
import base64

logging.basicConfig(
  format='%(asctime)s [%(name)s]: %(message)s',
  level=logging.INFO,
  datefmt='%Y-%m-%d %H:%M:%S',
  handlers=[RichHandler()]
)
log = logging.getLogger()

REPO_NAME = 'qbus-workshop'

# Data source code to docker image build directory
shutil.copy(
  src='../../generic/server.py',
  dst='../datasource/server.py'
)

parser = argparse.ArgumentParser(
  prog='deploy_script',
  description="Script with pre deploy, CDK deploy, and post deploy actions",
  formatter_class=RichHelpFormatter
)
parser.add_argument('-a', '--acct_id', action='store', help="target AWS acct ID for deployment", required=True)
parser.add_argument('-r', '--region', action='store', help="target AWS region, e.g. us-west-2", required=True)
parser.add_argument('-c', '--command', action='store', nargs='?', default='docker', help="container CLI command; valid options: docker | podman; default: docker")
args = parser.parse_args()

# Validate inputs
if not re.match(r'(us|ap|ca|eu)-(central|(north|south)?(east|west)?)-\d', args.region):
  log.error(f"Invalid region: {args.region}")
  exit(1)
else:
  region = args.region

if not re.match(r'\d{12}', args.acct_id):
  log.error(f"Invalid account ID: {args.acct_id}")
  exit(1)
else: 
  acct_id = args.acct_id

if not args.command in ['docker', 'podman']:
  log.error(f"Invalid container CLI command: {args.command}")
  exit(1)
else:
  command = args.command

# set CDK environment variables
os.environ['CDK_DEFAULT_ACCOUNT'] = acct_id
os.environ['CDK_DEFAULT_REGION'] = region

def run_cmd(cmd):
  log.info(f"Running command: {cmd}")
  try:
    # check for windows and use shell=True
    if os.name == 'nt':
      subprocess.check_output(cmd, text=True, shell=True)
    else:
      subprocess.check_output(cmd, text=True)
  except Exception as e:
    log.error(f"Command failed: {cmd}\nError: {e}")
    exit(1)

###############
# Bootstrap CDK
###############
log.info("Running CDK bootstrap")
run_cmd(['cdk', 'bootstrap', f'aws://{acct_id}/{region}'])
log.info("CDK bootstrap successful")

###############
# boto3 Create ECR repository
###############
log.info("Creating ECR repository")
try:
  ecr_client = boto3.client('ecr', 
                            region_name=region, 
                            config=Config(retries={'max_attempts': 10, 'mode': 'standard'}))
  response = ecr_client.create_repository(repositoryName=REPO_NAME)
  repo_uri = response['repository']['repositoryUri']
  log.info(f"ECR repository created: {repo_uri}")
except ClientError as e:
  log.error(f"Failed to create ECR repository: {e}")
  if e.response['Error']['Code'] == 'RepositoryAlreadyExistsException':
    log.info("Repository already exists, SAFE to move on...")
    repo_uri = f'{acct_id}.dkr.ecr.{region}.amazonaws.com/{REPO_NAME}'
  else: 
    exit(1)

###############
# login to ECR
###############
log.info("Logging into ECR")
try:
  ecr_client = boto3.client('ecr',
                            region_name=region,
                            config=Config(retries={'max_attempts': 10, 'mode': 'standard'}))
  auth_token = ecr_client.get_authorization_token()
  username, password = base64.b64decode(auth_token['authorizationData'][0]['authorizationToken']).decode().split(':')
  ecr_url = auth_token['authorizationData'][0]['proxyEndpoint']
  log.info(f"ECR URL: {ecr_url}")
  run_cmd([command, 'login', '-u', username, '-p', password, ecr_url])
  log.info("ECR login successful")
except ClientError as e:
  log.error(f"Failed to login to ECR: {e}")
  exit(1)

###############
# build datasource container
###############
log.info("Building datasource container")
run_cmd([command, 'build', '-t', REPO_NAME+':1.0', '../datasource'])
log.info("Datasource container build successful")

###############
# tag image for push to ECR
###############
log.info("Tagging image for push to ECR")
run_cmd([command, 'tag', REPO_NAME+':1.0', f'{repo_uri}:1.0'])
log.info("Image tag successful")

###############
# push image to ECR
###############
log.info("Pushing image to ECR")
run_cmd([command, 'push', f'{repo_uri}:1.0'])
log.info("Image push successful")

###############
# Deploy CDK
###############
log.info("Running CDK deploy")
run_cmd(['cdk', 'deploy', '--require-approval', 'never'])
log.info("CDK deploy successful")

log.info("SUCCESS!!!")
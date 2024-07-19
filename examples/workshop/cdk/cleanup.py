# This script cleans up Q Custom Connector workshop resources.
#
# Options: 
# -a, --acct_id  AWS_ACCT_ID    Target 12-digit AWS acct ID [REQUIRED]
# -r, --region   AWS_REGION     Target AWS region, e.g., us-west-2 [REQUIRED]
#
# Args:
# Cloudformation stack ID
#

import sys
import boto3
import re
import os
import argparse
import logging
import subprocess
from rich_argparse import RichHelpFormatter
from rich.logging import RichHandler
from botocore.exceptions import ClientError, ValidationError
from botocore.config import Config

logging.basicConfig(
  format='%(asctime)s [%(name)s]: %(message)s',
  level=logging.INFO,
  datefmt='%Y-%m-%d %H:%M:%S',
  handlers=[RichHandler()]
)
log = logging.getLogger()

REPO_NAME = 'qbus-workshop'

parser = argparse.ArgumentParser(
  prog='deploy_script',
  description="Script with pre deploy, CDK deploy, and post deploy actions",
  formatter_class=RichHelpFormatter
)
parser.add_argument('-a', '--acct_id', action='store', help="target AWS acct ID for deployment", required=True)
parser.add_argument('-r', '--region', action='store', nargs='?', default='us-west-2', help="target AWS region, e.g. us-east-1, default: us-west-2")
parser.add_argument('cfn_stack_id', action='store', nargs='?', help='cloudformation stack ID')
args = parser.parse_args()

# Validate inputs
if not re.match(r'(us|ap|ca|eu)-(central|(north|south)?(east|west)?)-\d', args.region):
  log.error(f"Invalid region: {args.region}")
  sys.exit(1)
else:
  region = args.region

if not re.match(r'\d{12}', args.acct_id):
  log.error(f"Invalid account ID: {args.acct_id}")
  sys.exit(1)
else: 
  acct_id = args.acct_id

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
    sys.exit(1)

###############
# validate cfn stack ID, and retrieve ECR image URI
###############
try:
  log.info("Validating CloudFormation ID")
  cfn = boto3.client('cloudformation', 
                     region_name=region,
                     config=Config(retries={'max_attempts': 10, 'mode': 'standard'}))
  response = cfn.describe_stacks(StackName=args.cfn_stack_id)
  log.info("Stack found...")
  outputs = response['Stacks'][0]['Outputs']
  for output in outputs:
    if output['OutputKey'] == 'ImageUri':
      ecr_uri = output['OutputValue']
      log.info(f"Found ECR repo: {ecr_uri}")
except ValidationError as e:
  log.error("Script failed to validate CFN stack ID and retrieving outputs")
  log.error(e)
  sys.exit(1)

###############
# delete ECR repo
###############
try:
  log.info("Deleting ECR repo")
  ecr_client = boto3.client('ecr',
                            region_name=region,
                            config=Config(retries={'max_attempts': 10, 'mode': 'standard'}))
  ecr_client.delete_repository(repositoryName=REPO_NAME, force=True)
  log.info("ECR repo deletion successful")
except ClientError as e:
  log.error(f"Failed to delete ECR repo: {e}")
  if e.response['Error']['Code'] == 'RepositoryNotFoundException':
    log.info("Repository already deleted, SAFE to move on...")
  else:
    sys.exit(1)

###############
# destroy CDK stack
###############
log.info("Running CDK destroy")
run_cmd(['cdk', 'destroy', '--force'])
log.info("CDK destroy successful")

log.info("SUCCESS!!!")


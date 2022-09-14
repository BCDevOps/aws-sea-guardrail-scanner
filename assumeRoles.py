import os
import subprocess
import suppFunct
import convertToHTML
import getSnapshotFunction
from os.path import exists

# To run this function,  you need to export the following values as env variables, or if calling it
# in a GiHub action, you need to add these values as secrets
#  AWS_ACCESS_KEY_ID
#  AWS_SECRET_ACCESS_KEY
#  AWS_SESSION_TOKEN
#  AWS_DEFAULT_REGION

# Running manually copy/paste the credentials provided by the https://dev.oidc.gov.bc.ca/auth/realms/.... site (depends on the LZ)


MASTER_AWS_ACCESS_KEY_ID=os.environ.get('AWS_ACCESS_KEY_ID')
MASTER_AWS_SECRET_ACCESS_KEY=os.environ.get('AWS_SECRET_ACCESS_KEY')
MASTER_AWS_SESSION_TOKEN=os.environ.get('AWS_SESSION_TOKEN')

MasterCredentials=[str(MASTER_AWS_ACCESS_KEY_ID),str(MASTER_AWS_SECRET_ACCESS_KEY),str(MASTER_AWS_SESSION_TOKEN)]


# List of accounts to assume - in the future will be an input file
#LZ1
# 513114711595 - f2u30s-tools
#     BCGOV_WORKLOAD_admin_tmhl5tvs     
# 900136227765 - f2u30s-dev
#     BCGOV_WORKLOAD_admin_tmhl5tvs
# 032091603982 - ubwyx8-dev
#     BCGOV_WORKLOAD_admin_tmhl5tvs
# 709720252926 - ubwyx8-sandbox
#     BCGOV_WORKLOAD_admin_tmhl5tvs

print("##################### MASTERIdentity")
identity= subprocess.getoutput('aws sts get-caller-identity')
print(identity)
print("####################")
# Assuming the role for account  513114711595
os.system('aws sts assume-role --role-arn arn:aws:iam::513114711595:role/AWSCloudFormationStackSetExecutionRole --role-session-name test | jq \'.Credentials | {AccessKeyId,SecretAccessKey,SessionToken}\' > ./apiResults.json')

AWS_ACCESS_KEY_ID=suppFunct.returnValue("apiResults.json","AccessKeyId")
AWS_SECRET_ACCESS_KEY=suppFunct.returnValue("apiResults.json","SecretAccessKey")
AWS_SESSION_TOKEN=suppFunct.returnValue("apiResults.json","SessionToken")

suppFunct.setCredentials([AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,AWS_SESSION_TOKEN])

print("##################### 513114711595 Identity")
identity= subprocess.getoutput('aws sts get-caller-identity')
print(identity)


# Here call getSnapshotFunction.py
# Requires the following variables
# 513114711595 - f2u30s-tools
#     BCGOV_WORKLOAD_admin_tmhl5tvs

getSnapshotFunction.getSnapshot("BCGOV_WORKLOAD_admin_tmhl5tvs","f2u30s-tools","1")  #def getSnapshot(awsRoleUsed, LicensePlate, LZ):

print("####################")

suppFunct.setCredentials(MasterCredentials) # Reset the credentials to Master
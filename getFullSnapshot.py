import os
from this import d
import datetime
import aws_ConfigValues
import aws_PoliciesInRoles
import suppFunct
from os.path import exists


print("############################################################################################################")
print("This script will create a snapshot of the SEA Guardrails. It required the AWS credentials for Master account of the zone")
print("   AWS_ACCESS_KEY_ID")
print("   AWS_SECRET_ACCESS_KEY")
print("   AWS_SESSION_TOKEN")
print("   AWS_DEFAULT_REGION")
print("by exporting them into your terminal session")
print("############################################################################################################")

print("The script will ask only for the number of the Landing Zone you want to scan.")
print("The script will reads the config file accountsToScan.json to determine which account and roles to scan")
print("As output will generate four files for each account + role in the previous file. The files will have the following format")
print("YYYMMDD_<type><Role><Config/Policies>_<LicensePlate>_<LZ#>")
print("############################################################################################################")
print("")



LZ=""
while LZ not in ["0","1","2"]:
    print('Which Landing zone LZ are you using 0/1/2')
    LZ=input()

########## Capture Snapshots for Master account
masterAccount=suppFunct.returnValue("accountsToScan.json","LZ" + LZ + ".Master.accountNumber")
masterLicensePlate=suppFunct.returnValue("accountsToScan.json","LZ" + LZ + ".Master.licensePlate")
masterRole=suppFunct.returnValue("accountsToScan.json","LZ" + LZ + ".Master.role")

awsRoleUsed=masterRole
awsRoleUsedSplit=masterRole.split("_")

LicensePlate=masterLicensePlate

typeDic={"CORE":"core","core":"core", "MASTER":"master","master":"master","WORKLOAD":"workload","workload":"workload"}
type=typeDic[awsRoleUsedSplit[1]]    

roleDic={"admin":"Admin","billing":"Billing","developer":"Developer", "readonly":"Readonly","security":"SecurityAudit"}  
role=roleDic[awsRoleUsedSplit[2]]     

    
currentDate = datetime.date.today().strftime("%Y%m%d")
resultsConfigFile=currentDate + "_" + type + role + "Config" + "_" + LicensePlate + "_" + "LZ" + LZ + ".json"
resultsPoliciesFile=currentDate + "_" + type + role + "Policies" + "_" +  LicensePlate+ "_" + "LZ" + LZ + ".json"

# Notice the folder where we save the results is hardcoded
#aws_ConfigValues.awsConfigValues(awsRoleUsed,LicensePlate,"./results/"+resultsConfigFile,LZ)
#aws_PoliciesInRoles.awsPoliciesInRoles(awsRoleUsed,LicensePlate,"./results/"+resultsPoliciesFile,LZ)

print("The following files have been created in the results folder:")
print("-" + resultsConfigFile )
print("-" + resultsConfigFile.split(".")[0] + ".html")
print("-" + resultsPoliciesFile )
print("-" + resultsPoliciesFile.split(".")[0] + ".html")

# This section captures the snapshots for the other accounts in the LZ. We will assume their roles
# from the master account

numberOfAccounts=suppFunct.getOutputApi("accountsToScan.json","LZ1.Accounts")



for n in range(int(numberOfAccounts)-1):
    #First, get the role for this account and assume the role
    userAccount=suppFunct.returnValue("accountsToScan.json","LZ" + LZ + ".Accounts | to_entries | .[" + str(n) +"] | [.key][0]")
   #usermasterLicensePlate=suppFunct.returnValue("accountsToScan.json","LZ1.Master.licensePlate")
   # usermasterRole=suppFunct.returnValue("accountsToScan.json","LZ1.Master.role")

    
    #suppFunct.setCredentials([AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,AWS_SESSION_TOKEN])



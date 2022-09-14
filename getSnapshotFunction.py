import os
from this import d
import datetime
import aws_ConfigValues
import aws_PoliciesInRoles
import suppFunct
from os.path import exists


print("############################################################################################################")
print("This script will create a snapshot of the SEA Guardrails. This snapshot depends of the account you are using")
print("It requires you previously have enter the values for:")
print("   AWS_ACCESS_KEY_ID")
print("   AWS_SECRET_ACCESS_KEY")
print("   AWS_SESSION_TOKEN")
print("   AWS_DEFAULT_REGION")
print("by exporting them into your terminal session")
print("############################################################################################################")

print("The following questions are used to create the name of the output files in the form")
print("YYYMMDD_<type><Role><Config/Policies>_<LicensePlate>_<LZ#>")
print("############################################################################################################")
print("")



def getSnapshot(awsRoleUsed, LicensePlate, LZ):
    
    awsRoleUsedSplit=awsRoleUsed.split("_")
    
    typeDic={"CORE":"core","core":"core", "MASTER":"master","master":"master","WORKLOAD":"workload","workload":"workload"}
    type=typeDic[awsRoleUsedSplit[1]]    


    roleDic={"admin":"Admin","billing":"Billing","developer":"Developer", "readonly":"Readonly","security":"SecurityAudit"}  
    role=roleDic[awsRoleUsedSplit[2]]     

    
    currentDate = datetime.date.today().strftime("%Y%m%d")
    resultsConfigFile=currentDate + "_" + type + role + "Config" + "_" + LicensePlate + "_" + "LZ" + LZ + ".json"
    resultsPoliciesFile=currentDate + "_" + type + role + "Policies" + "_" +  LicensePlate+ "_" + "LZ" + LZ + ".json"

    # Notice the folder where we save the results is hardcoded
    aws_ConfigValues.awsConfigValues(awsRoleUsed,LicensePlate,"./results/"+resultsConfigFile,LZ)
    aws_PoliciesInRoles.awsPoliciesInRoles(awsRoleUsed,LicensePlate,"./results/"+resultsPoliciesFile,LZ)

    print("The following files have been created in the results folder:")
    print("-" + resultsConfigFile )
    print("-" + resultsConfigFile.split(".")[0] + ".html")
    print("-" + resultsPoliciesFile )
    print("-" + resultsPoliciesFile.split(".")[0] + ".html")
    
    return
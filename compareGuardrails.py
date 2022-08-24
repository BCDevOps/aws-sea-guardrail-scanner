import os
import json
import suppFunct
from os.path import exists




def importJsonFile(jsonFile):
    try:
        with open(jsonFile, 'r') as json_file:
            json_data = json.load(json_file)
            return json_data
    except FileNotFoundError:
        print("my_file not found")
    return    


############################################################################################
########   Asking for the files names
############################################################################################


print("############################################################################################################")
print("This script assumes the files to compare are stored in the ./results folder. Please read the messages if you want to ")
print("compare files with non-standard names or located in folders different than ./results")
print("")
print("The following questions are used to find the files you want to compare and create the name of the output file in the form")
print("comparison_YYYMMDD_yyyymmdd_<type><Role><Config/Policies><LZ#>")
print("where YYYYMMDD is the date for the older snapshot and yyyyddmm is the date for the newer snapshot")
print("############################################################################################################")
print("")

Location=""
olderSnapshotConfig=""
newerSnapshotConfig=""
olderSnapshotPolicies=""
newerSnapshotPolicies=""

print("Are the files located in a folder other than /results and/or the filenames are not standard? Any key other than y is understood as NO")
Location=input()

if Location=="y": # Case we search in a folder other than ./results and/or the files have non-standard names
    print("Location of the older Config snapshot")
    olderSnapshotConfig=input()
    print("Location of the newer Config snapshot")
    newerSnapshotConfig=input()
    
    print("Location of the older Policies snapshot")
    olderSnapshotPolicies=input()
    print("Location of the newer Policies snapshot")
    newerSnapshotPolicies=input()
    
    if not os.path.exists(olderSnapshotConfig) or not os.path.exists(newerSnapshotConfig) or not os.path.exists(olderSnapshotPolicies) or not os.path.exists(newerSnapshotPolicies):
        print("Either the older or the newer Config/Policies snapshots has not been found")
        quit()
    else:
        olderSnapshotConfig=suppFunct.importJsonFile(olderSnapshotConfig)
        newerSnapshotConfig=suppFunct.importJsonFile(newerSnapshotConfig)
        olderSnapshotPolicies=suppFunct.importJsonFile(olderSnapshotPolicies)
        newerSnapshotPolicies=suppFunct.importJsonFile(newerSnapshotPolicies)
        
        
    userRoleSplit=olderSnapshotConfig["TestInformation"]["awsRoleUsed"].split("_")
    LicensePlate=olderSnapshotConfig["TestInformation"]["LicensePlate"]
    LZ=olderSnapshotConfig["TestInformation"]["Landing Zone"][-1]
    olderDate=olderSnapshotConfig["TestInformation"]["DateTime"].split(" ")[0].replace("-","")
    newerDate=newerSnapshotConfig["TestInformation"]["DateTime"].split(" ")[0].replace("-","")
    
    
    
    typeDic={"CORE":"core","core":"core", "MASTER":"master","master":"master","WORKLOAD":"workload","workload":"workload"}
    type=typeDic[userRoleSplit[1]] 
    roleDic={"admin":"Admin","billing":"Billing","developer":"Developer", "readonly":"Readonly","s":"SecurityAudit","security audit":"SecurityAudit"}  
    role=roleDic[userRoleSplit[2]]     
    
    
else: # Case we search in the ./results folder and the files names follow the standard YYYMMDD_<type><Role><Config/Policies><LZ#>
    userRole=" " #Notice the whitespace, so len is >0
    userRoleSplit=[]

    while len(userRole)!=0 and len(userRoleSplit)<4 :
        print("Which AWS user ROLE are you using? - If enter nothing will use  \"BCGOV_MASTER_admin_tmhl5tvs\"")

        userRole=input()
        if len(userRole)==0:
            userRole="BCGOV_MASTER_admin_tmhl5tvs"
            
        userRoleSplit=userRole.split("_")

    LicensePlate=""
    print("Which License Plate-environment is using the previous base account? - If enter nothing will use  \"tmhl5tvs-dev\"")
    LicensePlate=input()
    if len(LicensePlate)==0:
        LicensePlate="tmhl5tvs-dev"
    
    LZ=""
    while LZ not in ["0","1","2"]:
        print('Which Landing zone LZ are you using 0/1/2')
        LZ=input()

    typeDic={"CORE":"core","core":"core", "MASTER":"master","master":"master","WORKLOAD":"workload","workload":"workload"}
    type=typeDic[userRoleSplit[1]]    


    roleDic={"admin":"Admin","billing":"Billing","developer":"Developer", "readonly":"Readonly","s":"SecurityAudit","security audit":"SecurityAudit"}  
    role=roleDic[userRoleSplit[2]]     

    olderDate=""
    while len(olderDate) !=8:
        print('Enter the date of the older snapshot as YYYYMMDD')
        olderDate=input()
        
    newerDate=""
    while len(newerDate) !=8:
        print('Enter the date of the newer snapshot as YYYYMMDD')
        newerDate=input()  
   
    olderSnapshotConfig=olderDate+ "_" + type + role + "Config" + "_" + LicensePlate + "_LZ" + LZ + ".json"
    newerSnapshotConfig=newerDate+ "_" + type + role + "Config" + "_" + LicensePlate + "_LZ" +  LZ + ".json"
 
    olderSnapshotPolicies=olderDate+ "_" + type + role + "Policies" + "_" + LicensePlate + "_LZ" +  LZ + ".json"
    newerSnapshotPolicies=newerDate+ "_" + type + role + "Policies" + "_" + LicensePlate + "_LZ" +  LZ + ".json"   
    
    olderSnapshotConfig=suppFunct.importJsonFile("./results/"+olderSnapshotConfig)
    newerSnapshotConfig=suppFunct.importJsonFile("./results/"+newerSnapshotConfig)
    
    olderSnapshotPolicies=suppFunct.importJsonFile("./results/"+olderSnapshotPolicies)
    newerSnapshotPolicies=suppFunct.importJsonFile("./results/"+newerSnapshotPolicies)


if olderSnapshotConfig["TestInformation"]["awsRoleUsed"]!=newerSnapshotConfig["TestInformation"]["awsRoleUsed"] or olderSnapshotConfig["TestInformation"]["AWS_DEFAULT_REGION"]!=newerSnapshotConfig["TestInformation"]["AWS_DEFAULT_REGION"] or olderSnapshotConfig["TestInformation"]["Landing Zone"]!=newerSnapshotConfig["TestInformation"]["Landing Zone"]or olderSnapshotConfig["TestInformation"]["LicensePlate"]!=newerSnapshotConfig["TestInformation"]["LicensePlate"]:
    print("You are comparing the wrong snapshots, either the account, region or Landing Zone are not the same")
    quit()


title = "LZ" + LZ + " Configuration comparison between " + olderSnapshotConfig["TestInformation"]["DateTime"]  + " and " + newerSnapshotConfig["TestInformation"]["DateTime"] #The title of the report
html = suppFunct.addHeader(title)


# Adding the test information
html=html+ "<table><tr><th></th><th>Older Snapshot</th><th>Newer Snapshot</th></tr>"
html=html+ "<td><B>Date/Time</B></td><td>"    + olderSnapshotConfig["TestInformation"]["DateTime"]           + "</td><td>" + newerSnapshotConfig["TestInformation"]["DateTime"]           + "</td></tr>"
html=html+ "<td><B>Role</B></td><td>"      + olderSnapshotConfig["TestInformation"]["awsRoleUsed"]     + "</td><td>" + newerSnapshotConfig["TestInformation"]["awsRoleUsed"]     + "</td></tr>"
html=html+ "<td><B>Region</B></td><td>"       + olderSnapshotConfig["TestInformation"]["AWS_DEFAULT_REGION"] + "</td><td>" + newerSnapshotConfig["TestInformation"]["AWS_DEFAULT_REGION"] + "</td></tr>"
html=html+ "<td><B>License Plate</B></td><td>" + olderSnapshotConfig["TestInformation"]["LicensePlate"]      + "</td><td>" + newerSnapshotConfig["TestInformation"]["LicensePlate"]       + "</td></tr>"
html=html+ "<td><B>Landing Zone</B></td><td>" + olderSnapshotConfig["TestInformation"]["Landing Zone"]       + "</td><td>" + newerSnapshotConfig["TestInformation"]["Landing Zone"]       + "</td></tr>"

html=html+ "</tr></table>"

html=html+ "<hr class=\"dashed\">\n"

##########################################
# Parsing and comparing the Config files
##########################################

html=html+ "<H2>LZ" + LZ + " configuration values</H2>\n"

changeFlag=0
if olderSnapshotConfig["awsNumberIamUsers"]!=newerSnapshotConfig["awsNumberIamUsers"]:
    html=html+"<P>The number of <B>AWS IAM users</B> in LZ" + LZ + "  has changed from : <B>" + str(olderSnapshotConfig["awsNumberIamUsers"])+ "</B> to <B>" + str(newerSnapshotConfig["awsNumberIamUsers"]) + "</B></P>\n"
    changeFlag=1
    
if olderSnapshotConfig["awsNumberIamUsers"]!=newerSnapshotConfig["awsNumberIamUsers"]:
    html=html+"<P>The number of <B>AWS IAM groups</B> in LZ" + LZ + "  has changed from : <B>" + str(olderSnapshotConfig["awsNumberIamUsers"])+ "</B> to <B>" + str(newerSnapshotConfig["awsNumberIamUsers"]) + "</B></P>\n"
    changeFlag=1

if olderSnapshotConfig["awsNumberIamRoles"]!=newerSnapshotConfig["awsNumberIamRoles"]:
    html=html+"<P>The number of <B>AWS IAM roles</B> in LZ" + LZ + "  has changed from: <B>" + str(olderSnapshotConfig["awsNumberIamRoles"])+ "</B> to <B>" + str(newerSnapshotConfig["awsNumberIamRoles"]) + "</B></P>\n"
    changeFlag=1

if olderSnapshotConfig["awsNumberIamPolicies"]!=newerSnapshotConfig["awsNumberIamPolicies"]:
    html=html+"<P>The number of <B>AWS IAM policies</B> in LZ" + LZ + "  has changed from  : <B>" + str(olderSnapshotConfig["awsNumberIamPolicies"])+ "</B> to <B>" + str(newerSnapshotConfig["awsNumberIamPolicies"]) + "</B></P>\n"
    changeFlag=1




if olderSnapshotConfig["awsNumberAvailablePolicies"]!=newerSnapshotConfig["awsNumberAvailablePolicies"]:
    html=html+"<P>The number of <B>Policies</B> available to the AWS account in LZ" + LZ + "  has changed from  : <B>" + str(olderSnapshotConfig["awsNumberAvailablePolicies"])+ "</B> to <B>" + str(newerSnapshotConfig["awsNumberAvailablePolicies"]) + "</B></P>\n"
    changeFlag=1

if olderSnapshotConfig["awsTotalNumberAccounts"]!=newerSnapshotConfig["awsTotalNumberAccounts"]:
    html=html+"<P>The number of <B>accounts</B> in LZ" + LZ + "  has changed from  : <B>" + str(olderSnapshotConfig["awsTotalNumberAccounts"])+ "</B> to <B>" + str(newerSnapshotConfig["awsTotalNumberAccounts"]) + "</B></P>\n"
    changeFlag=1

if olderSnapshotConfig["numberCloudfrontDistributions"]!=newerSnapshotConfig["numberCloudfrontDistributions"]:
    html=html+"<P>The number of <B>Cloudfront Distributions</B> associated to this account has changed from  : <B>" + str(olderSnapshotConfig["numberCloudfrontDistributions"])+ "</B> to <B>" + str(newerSnapshotConfig["numberCloudfrontDistributions"]) + "</B></P>\n"
    changeFlag=1

if olderSnapshotConfig["numberCloudfrontFunctions"]!=newerSnapshotConfig["numberCloudfrontFunctions"]:
    html=html+"<P>The number of <B>Cloudfront Functions</B> associated to this account has changed from  : <B>" + str(olderSnapshotConfig["numberCloudfrontFunctions"])+ "</B> to <B>" + str(newerSnapshotConfig["numberCloudfrontFunctions"]) + "</B></P>\n"
    changeFlag=1    

if olderSnapshotConfig["numberClusters"]!=newerSnapshotConfig["numberClusters"]:
    html=html+"<P>The number of <B>clusters</B> associated to this account has changed from  : <B>" + str(olderSnapshotConfig["numberClusters"])+ "</B> to <B>" + str(newerSnapshotConfig["numberClusters"]) + "</B></P>\n"
    changeFlag=1  

if olderSnapshotConfig["numberEC2Instances"]!=newerSnapshotConfig["numberEC2Instances"]:
    html=html+"<P>The number of <B>EC2 instances</B> associated to this account has changed from  : <B>" + str(olderSnapshotConfig["numberEC2Instances"])+ "</B> to <B>" + str(newerSnapshotConfig["numberEC2Instances"]) + "</B></P>\n"
    changeFlag=1  

if olderSnapshotConfig["numberLambdaFunctions"]!=newerSnapshotConfig["numberLambdaFunctions"]:
    html=html+"<P>The number of <B>Lambda Functions</B> associated to this account has changed from  : <B>" + str(olderSnapshotConfig["numberLambdaFunctions"])+ "</B> to <B>" + str(newerSnapshotConfig["numberLambdaFunctions"]) + "</B></P>\n"
    changeFlag=1  


if changeFlag==0:
    html=html+"<P>There have been no changes on the configuration values</P>\n"
    


################################## S3 Buckets
html=html+ "<hr class=\"dashed\">\n"
html=html+ "<H2>S3 Buckets</H2>\n"
html=html+ "<H3>S3 Buckets policies change</H3>\n"

changeFlag=0 # Reset the flag
for key,value in olderSnapshotConfig["S3Buckets_AccessPolicy"].items():
    if key in newerSnapshotConfig["S3Buckets_AccessPolicy"]:
        if olderSnapshotConfig["S3Buckets_AccessPolicy"][key]!=newerSnapshotConfig["S3Buckets_AccessPolicy"][key]:
            html=html+"<P>The policy for S3 bucket <B>" + key + "</B> has changed from <I>" + olderSnapshotConfig["S3Buckets_AccessPolicy"][key] + "</I> to <I>" + newerSnapshotConfig["S3Buckets_AccessPolicy"][key] + "</I></P>\n"
            changeFlag=1   
            
if changeFlag==0:
    html=html+"<P>There have been no changes on any S3 Bucket access policy</P>\n"

html=html+ "<H3>New S3 Buckets</H3>\n"
changeFlag=0 # Reset the flag
for key,value in newerSnapshotConfig["S3Buckets_AccessPolicy"].items():
    if key not in olderSnapshotConfig["S3Buckets_AccessPolicy"]:
        html=html+"<P>There is a new S3 bucket <B>" + key + "</B> with policy <B>" +  newerSnapshotConfig["S3Buckets_AccessPolicy"][key] +"</B></P>\n"
        changeFlag=1   

if changeFlag==0:
    html=html+"<P>No new S3 buckets have been added</P>\n"

html=html+ "<H3>Deleted S3 Buckets</H3>\n"
changeFlag=0 # Reset the flag
for key,value in olderSnapshotConfig["S3Buckets_AccessPolicy"].items():
    if key not in newerSnapshotConfig["S3Buckets_AccessPolicy"]:
        html=html+"<P>The S3 bucket <B>" + key + "</B> has been deleted</P>\n"
        changeFlag=1   

if changeFlag==0:
    html=html+"<P>No S3 buckets have been deleted</P>\n"



######################################################################################


################################## Roles

html=html+ "<hr class=\"dashed\">\n"
html=html+ "<H2>Roles</H2>\n"

if olderSnapshotConfig["awsNumberRoles"]!=newerSnapshotConfig["awsNumberRoles"]:
    html=html+"<P>The number of <B>roles</B> associated to the user in LZ" + LZ + "  has changed from  : <B>" + str(olderSnapshotConfig["awsNumberRoles"])+ "</B> to <B>" + str(newerSnapshotConfig["awsNumberRoles"]) + "</B></P>\n"
    changeFlag=1

html=html+ "<H3>Roles changes: same name, but arn changes</H3>\n"

changeFlag=0 # Reset the flag
for key,value in olderSnapshotConfig["List_of_Roles_for_the_Account"].items():
    if key in newerSnapshotConfig["List_of_Roles_for_the_Account"]:
        if olderSnapshotConfig["List_of_Roles_for_the_Account"][key]!=newerSnapshotConfig["List_of_Roles_for_the_Account"][key]:
            html=html+"<P>Role with Name <B>" + key + "</B> had the Arn changed from <I>" + olderSnapshotConfig["List_of_Roles_for_the_Account"][key] + "</I> to <I>" + newerSnapshotConfig["List_of_Roles_for_the_Account"][key] + "</I></P>\n"
            changeFlag=1   
            
if changeFlag==0:
    html=html+"<P>There have been no on the Arn associated to Roles</P>\n"

html=html+ "<H3>New Roles</H3>\n"
changeFlag=0 # Reset the flag
for key,value in newerSnapshotConfig["List_of_Roles_for_the_Account"].items():
    if key not in olderSnapshotConfig["List_of_Roles_for_the_Account"]:
        html=html+"<P>There is a new Role with name <B>" + key + "</B> and Arn <B>" +  newerSnapshotConfig["List_of_Roles_for_the_Account"][key] +"</B></P>\n"
        changeFlag=1   

if changeFlag==0:
    html=html+"<P>No new Roles have been added</P>\n"

html=html+ "<H3>Deleted Roles</H3>\n"
changeFlag=0 # Reset the flag
for key,value in olderSnapshotConfig["List_of_Roles_for_the_Account"].items():
    if key not in newerSnapshotConfig["List_of_Roles_for_the_Account"]:
        html=html+"<P>The Role with name <B>" + key + "</B> has been deleted</P>\n"
        changeFlag=1   

if changeFlag==0:
    html=html+"<P>No Roles have been deleted</P>\n"


######################################################################################

################################## Organization Units
html=html+ "<hr class=\"dashed\">\n"

html=html+ "<H2>Organizational Units</H2>\n"

if olderSnapshotConfig["OrganizationsInformation"]["numberOrganizationUnits"]!=newerSnapshotConfig["OrganizationsInformation"]["numberOrganizationUnits"]:
    html=html+"<P>The number of <B>Organizations</B> associated to this account has changed from  : <B>" + str(olderSnapshotConfig["OrganizationsInformation"]["numberOrganizationUnits"])+ "</B> to <B>" + str(newerSnapshotConfig["OrganizationsInformation"]["numberOrganizationUnits"]) + "</B></P>\n"

html=html+ "<H3>Deleted Organizations</H3>\n"
changeFlag=0 # Reset the flag
for key,value in olderSnapshotConfig["OrganizationsInformation"].items():
    if key not in newerSnapshotConfig["OrganizationsInformation"] and key!="numberOrganizationUnits":
        html=html+"<P>The Organization <B>" + key + "</B> has been deleted</P>\n"
        changeFlag=1   

if changeFlag==0:
    html=html+"<P>No organizations have been deleted</P>\n"

html=html+ "<H3>New Organizations</H3>\n"
changeFlag=0 # Reset the flag
for key,value in newerSnapshotConfig["OrganizationsInformation"].items():
    if key not in olderSnapshotConfig["OrganizationsInformation"] and key!="numberOrganizationUnits":
        html=html+"<P>The Organization <B>" + key + "</B> has been added</P>\n"
        changeFlag=1   

if changeFlag==0:
    html=html+"<P>No new organizations have been added</P>\n"



html=html+ "<hr class=\"dashed\">\n"
#########################################
# Parsing and comparing the Policies files
#########################################


html=html+ "<H2>Policies</H2>\n"
html=html+ "<H3>Managed Policies Attached to IAM Role</H3>\n"

html=html+ "<H4>Managed Policies Attached to IAM Role changes</H4>\n"
changeFlag=0 # Reset the flag
for key,value in olderSnapshotPolicies.items():
    if key in newerSnapshotPolicies and key.split("_",1)[0]=="managedPoliciesAttachedToIAMRole":
        if olderSnapshotPolicies[key]!=newerSnapshotPolicies[key] and olderSnapshotPolicies[key]!="TestInformation":
            html=html+"<P>The Managed Policies Attached to IAM Role <B>" + key.split("_",1)[1] + "</B> has changed from <I>" + str(olderSnapshotPolicies[key]) + "</I> to <I>" + str(newerSnapshotPolicies[key]) + "</I></P>\n"
            changeFlag=1   
            
if changeFlag==0:
    html=html+"<P>There have been no changes on any Managed Policies Attached to IAM Role</P>\n"


html=html+ "<H4>New Managed Policies Attached to IAM Role</H4>\n"
changeFlag=0 # Reset the flag
for key,value in newerSnapshotPolicies.items():
    if key not in olderSnapshotPolicies and key.split("_",1)[0]=="managedPoliciesAttachedToIAMRole" and newerSnapshotPolicies[key]!="TestInformation":
        html=html+"<P>There is a new Managed Policies Attached to IAM Rolet <B>" + key.split("_",1)[1] + "</B> with <I>" + str(newerSnapshotPolicies[key]) + "</I> roles attached to it</P>\n"
        changeFlag=1   
            
if changeFlag==0:
    html=html+"<P>There are no new Managed Policies Attached to IAM Role</P>\n"


html=html+ "<H4>Deleted Managed Policies Attached to IAM Role</H4>\n"
changeFlag=0 # Reset the flag
for key,value in olderSnapshotPolicies.items():
    if key not in newerSnapshotPolicies and key.split("_",1)[0]=="managedPoliciesAttachedToIAMRole" and olderSnapshotPolicies[key]!="TestInformation":
        html=html+"<P>The following Managed Policies Attached to IAM Rolet <B>" + key.split("_",1)[1] + "</B> has  been removed</P>\n"
        changeFlag=1   
            
if changeFlag==0:
    html=html+"<P>There have been no deleted  Managed Policies Attached to IAM Role</P>\n"


html=html+ "<H3>In line Policies Embedded to IAM IAM Role</H3>\n"

html=html+ "<H4>In line Policies Embedded to IAM IAM Role changes</H4>\n"
changeFlag=0 # Reset the flag
for key,value in olderSnapshotPolicies.items():
    if key in newerSnapshotPolicies and key.split("_",1)[0]=="inlinePoliciesEmbeddedToIamRole":
        if olderSnapshotPolicies[key]!=newerSnapshotPolicies[key] and olderSnapshotPolicies[key]!="TestInformation":
            html=html+"<P>The in line Policies Embedded to IAM IAM Role <B>" + key.split("_",1)[1] + "</B> has changed from <I>" + str(olderSnapshotPolicies[key]) + "</I> to <I>" + str(newerSnapshotPolicies[key]) + "</I></P>\n"
            changeFlag=1   
            
if changeFlag==0:
    html=html+"<P>There have been no changes in line Policies Embedded to IAM IAM Role</P>\n"


html=html+ "<H4>New Managed Policies Embedded to IAM IAM Role</H4>\n"
changeFlag=0 # Reset the flag
for key,value in newerSnapshotPolicies.items():
    if key not in olderSnapshotPolicies and key.split("_",1)[0]=="inlinePoliciesEmbeddedToIamRole" and newerSnapshotPolicies[key]!="TestInformation":
        html=html+"<P>There is a new In line Policies Embedded to IAM IAM Role <B>" + key.split("_",1)[1] + "</B> with <I>" + str(newerSnapshotPolicies[key]) + "</I> roles attached to it</P>\n"
        changeFlag=1   
            
if changeFlag==0:
    html=html+"<P>There have been no new in line Policies Embedded to IAM IAM Role</P>\n"


html=html+ "<H4>Deleted Policies Embedded to IAM IAM Role</H4>\n"
changeFlag=0 # Reset the flag
for key,value in olderSnapshotPolicies.items():
    if key not in newerSnapshotPolicies and key.split("_",1)[0]=="inlinePoliciesEmbeddedToIamRole" and olderSnapshotPolicies[key]!="TestInformation":
        html=html+"<P>The following In line Policies Embedded to IAM IAM Role <B>" + key.split("_",1)[1] + "</B> has  been removed</P>\n"
        changeFlag=1   
            
if changeFlag==0:
    html=html+"<P>There have been no deleted in line Policies Embedded to IAM IAM Role</P>\n"


html=html+"</body>\n"
html=html+"</head>\n"
  
with open('./'+ olderDate + '_' + newerDate + '_' + type + role + "_" + LicensePlate + "_LZ" + LZ + '.html', 'w') as f: #The report name is harcoded.
    f.write(html)
    
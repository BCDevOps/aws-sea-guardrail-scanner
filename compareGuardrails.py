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

print("Are the files located in a non-standard location? Any key other than y is understood as NO")
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
    
else: # Case we search in the ./results folder and the files names follow the standard YYYMMDD_<type><Role><Config/Policies><LZ#>
    userAccount=" " #Notice the whitespace, so len is >0
    userAccountSplit=[]

    while len(userAccount)!=0 and len(userAccountSplit)<4 :
        print("Which AWS user account are you using? - If enter nothing will use  \"BCGOV_MASTER_admin_tmhl5tvs\"")

        userAccount=input()
        if len(userAccount)==0:
            userAccount="BCGOV_MASTER_admin_tmhl5tvs"
        userAccountSplit=userAccount.split("_")


    LZ=""
    while LZ not in ["0","1","2"]:
        print('Which Landing zone LZ are you using 0/1/2')
        LZ=input()

    typeDic={"CORE":"core","core":"core", "MASTER":"master","master":"master","WORKLOAD":"workload","workload":"workload"}
    type=typeDic[userAccountSplit[1]]    


    roleDic={"admin":"Admin","billing":"Billing","developer":"Developer", "readonly":"Readonly","s":"SecurityAudit","security audit":"SecurityAudit"}  
    role=roleDic[userAccountSplit[2]]     

    olderDate=""
    while len(olderDate) !=8:
        print('Enter the date of the older snapshot as YYYYMMDD')
        olderDate=input()
        
    newerDate=""
    while len(newerDate) !=8:
        print('Enter the date of the newer snapshot as YYYYMMDD')
        newerDate=input()  
   
    olderSnapshotConfig=olderDate+ "_" + type + role + "ConfigLZ" + LZ + ".json"
    newerSnapshotConfig=newerDate+ "_" + type + role + "ConfigLZ" + LZ + ".json"
 
    olderSnapshotPolicies=olderDate+ "_" + type + role + "PoliciesLZ" + LZ + ".json"
    newerSnapshotPolicies=newerDate+ "_" + type + role + "PoliciesLZ" + LZ + ".json"   
    
    olderSnapshotConfig=suppFunct.importJsonFile("./results/"+olderSnapshotConfig)
    newerSnapshotConfig=suppFunct.importJsonFile("./results/"+newerSnapshotConfig)
    
    #olderSnapshotPolicies=suppFunct.importJsonFile("./results/"+olderSnapshotPolicies)
    #newerSnapshotPolicies=suppFunct.importJsonFile("./results/"+newerSnapshotPolicies)

#print('Enter the name of the Configuration snapshot before the upgrade')
#jsonFileBefore=input()
#jsonFileBefore = jsonFileBefore if len(jsonFileBefore)>0 else "./resultsKeyParametersBefore.json"

#olderSnapshotConfig=suppFunct.importJsonFile(jsonFileBefore)

#print('Enter the name of the Configuration snapshot after the upgrade')
#jsonFileAfter=input()
#jsonFileAfter = jsonFileAfter if len(jsonFileAfter)>0 else "./resultsKeyParametersAfter.json"






############################################################################################
########   Comparing the files
############################################################################################


title = "LZ2 Configuration comparison between " + olderSnapshotConfig["TestInformation"]["DateTime"]  + " and " + newerSnapshotConfig["TestInformation"]["DateTime"] #The title of the report

html = suppFunct.addHeader(title)

html=html+ "<H2>LZ2 configuration values</H2>\n"

changeFlag=0
if olderSnapshotConfig["awsNumberIamUsers"]!=newerSnapshotConfig["awsNumberIamUsers"]:
    html=html+"<P>The number of <B>AWS IAM users</B> in LZ2 has changed from : <B>" + str(olderSnapshotConfig["awsNumberIamUsers"])+ "</B> to <B>" + str(newerSnapshotConfig["awsNumberIamUsers"]) + "</B></P>\n"
    changeFlag=1
    
if olderSnapshotConfig["awsNumberIamUsers"]!=newerSnapshotConfig["awsNumberIamUsers"]:
    html=html+"<P>The number of <B>AWS IAM groups</B> in LZ2 has changed from : <B>" + str(olderSnapshotConfig["awsNumberIamUsers"])+ "</B> to <B>" + str(newerSnapshotConfig["awsNumberIamUsers"]) + "</B></P>\n"
    changeFlag=1

if olderSnapshotConfig["awsNumberIamRoles"]!=newerSnapshotConfig["awsNumberIamRoles"]:
    html=html+"<P>The number of <B>AWS IAM roles</B> in LZ2 has changed from: <B>" + str(olderSnapshotConfig["awsNumberIamRoles"])+ "</B> to <B>" + str(newerSnapshotConfig["awsNumberIamRoles"]) + "</B></P>\n"
    changeFlag=1

if olderSnapshotConfig["awsNumberIamPolicies"]!=newerSnapshotConfig["awsNumberIamPolicies"]:
    html=html+"<P>The number of <B>AWS IAM policies</B> in LZ2 has changed from  : <B>" + str(olderSnapshotConfig["awsNumberIamPolicies"])+ "</B> to <B>" + str(newerSnapshotConfig["awsNumberIamPolicies"]) + "</B></P>\n"
    changeFlag=1


if olderSnapshotConfig["awsNumberRoles"]!=newerSnapshotConfig["awsNumberRoles"]:
    html=html+"<P>The number of <B>roles</B> associated to the user in LZ2 has changed from  : <B>" + str(olderSnapshotConfig["awsNumberRoles"])+ "</B> to <B>" + str(newerSnapshotConfig["awsNumberRoles"]) + "</B></P>\n"
    changeFlag=1

if olderSnapshotConfig["awsNumberAvailablePolicies"]!=newerSnapshotConfig["awsNumberAvailablePolicies"]:
    html=html+"<P>The number of <B>Policies</B> available to the AWS account in LZ2 has changed from  : <B>" + str(olderSnapshotConfig["awsNumberAvailablePolicies"])+ "</B> to <B>" + str(newerSnapshotConfig["awsNumberAvailablePolicies"]) + "</B></P>\n"
    changeFlag=1

if olderSnapshotConfig["awsTotalNumberAccounts"]!=newerSnapshotConfig["awsTotalNumberAccounts"]:
    html=html+"<P>The number of <B>accounts</B> in LZ2 has changed from  : <B>" + str(olderSnapshotConfig["awsTotalNumberAccounts"])+ "</B> to <B>" + str(newerSnapshotConfig["awsTotalNumberAccounts"]) + "</B></P>\n"
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


html=html+"</body>\n"
html=html+"</head>\n"
  
with open('./comparisonReport.html', 'w') as f: #The report name is harcoded.
    f.write(html)
    


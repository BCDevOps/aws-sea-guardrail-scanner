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

print('Enter the name of the Configuration snapshot before the upgrade')
jsonFileBefore=input()
jsonFileBefore = jsonFileBefore if len(jsonFileBefore)>0 else "./resultsKeyParametersBefore.json"

jsonDataBefore=suppFunct.importJsonFile(jsonFileBefore)

print('Enter the name of the Configuration snapshot after the upgrade')
jsonFileAfter=input()
jsonFileAfter = jsonFileAfter if len(jsonFileAfter)>0 else "./resultsKeyParametersAfter.json"

jsonDataAfter=suppFunct.importJsonFile(jsonFileAfter)

############################################################################################
########   Comparing the files
############################################################################################


title = "LZ2 Configuration comparison between " + jsonDataBefore["TestInformation"]["DateTime"]  + " and " + jsonDataAfter["TestInformation"]["DateTime"] #The title of the report

html = suppFunct.addHeader(title)



html=html+ "<H2>LZ2 configuration values</H2>\n"

changeFlag=0
if jsonDataBefore["awsNumberIamUsers"]!=jsonDataAfter["awsNumberIamUsers"]:
    html=html+"<P>The number of <B>AWS IAM users</B> in LZ2 has changed from : <B>" + str(jsonDataBefore["awsNumberIamUsers"])+ "</B> to <B>" + str(jsonDataAfter["awsNumberIamUsers"]) + "</B></P>\n"
    changeFlag=1
    
if jsonDataBefore["awsNumberIamUsers"]!=jsonDataAfter["awsNumberIamUsers"]:
    html=html+"<P>The number of <B>AWS IAM groups</B> in LZ2 has changed from : <B>" + str(jsonDataBefore["awsNumberIamUsers"])+ "</B> to <B>" + str(jsonDataAfter["awsNumberIamUsers"]) + "</B></P>\n"
    changeFlag=1

if jsonDataBefore["awsNumberIamRoles"]!=jsonDataAfter["awsNumberIamRoles"]:
    html=html+"<P>The number of <B>AWS IAM roles</B> in LZ2 has changed from: <B>" + str(jsonDataBefore["awsNumberIamRoles"])+ "</B> to <B>" + str(jsonDataAfter["awsNumberIamRoles"]) + "</B></P>\n"
    changeFlag=1

if jsonDataBefore["awsNumberIamRoles"]!=jsonDataAfter["awsNumberIamRoles"]:
    html=html+"<P>The number of <B>AWS IAM roles</B> in LZ2 has changed from  : <B>" + str(jsonDataBefore["awsNumberIamRoles"])+ "</B> to <B>" + str(jsonDataAfter["awsNumberIamRoles"]) + "</B></P>\n"
    changeFlag=1

if jsonDataBefore["awsNumberIamPolicies"]!=jsonDataAfter["awsNumberIamPolicies"]:
    html=html+"<P>The number of <B>AWS IAM policies</B> in LZ2 has changed from  : <B>" + str(jsonDataBefore["awsNumberIamPolicies"])+ "</B> to <B>" + str(jsonDataAfter["awsNumberIamPolicies"]) + "</B></P>\n"
    changeFlag=1


if jsonDataBefore["awsNumberRoles"]!=jsonDataAfter["awsNumberRoles"]:
    html=html+"<P>The number of <B>roles</B> associated to the user in LZ2 has changed from  : <B>" + str(jsonDataBefore["awsNumberRoles"])+ "</B> to <B>" + str(jsonDataAfter["awsNumberRoles"]) + "</B></P>\n"
    changeFlag=1

if jsonDataBefore["awsNumberAvailablePolicies"]!=jsonDataAfter["awsNumberAvailablePolicies"]:
    html=html+"<P>The number of <B>Policies</B> available to the AWS account in LZ2 has changed from  : <B>" + str(jsonDataBefore["awsNumberAvailablePolicies"])+ "</B> to <B>" + str(jsonDataAfter["awsNumberAvailablePolicies"]) + "</B></P>\n"
    changeFlag=1

if jsonDataBefore["awsTotalNumberAccounts"]!=jsonDataAfter["awsTotalNumberAccounts"]:
    html=html+"<P>The number of <B>accounts</B> in LZ2 has changed from  : <B>" + str(jsonDataBefore["awsTotalNumberAccounts"])+ "</B> to <B>" + str(jsonDataAfter["awsTotalNumberAccounts"]) + "</B></P>\n"
    changeFlag=1

if jsonDataBefore["numberCloudfrontDistributions"]!=jsonDataAfter["numberCloudfrontDistributions"]:
    html=html+"<P>The number of <B>Cloudfront Distributions</B> associated to this account has changed from  : <B>" + str(jsonDataBefore["numberCloudfrontDistributions"])+ "</B> to <B>" + str(jsonDataAfter["numberCloudfrontDistributions"]) + "</B></P>\n"
    changeFlag=1

if jsonDataBefore["numberCloudfrontFunctions"]!=jsonDataAfter["numberCloudfrontFunctions"]:
    html=html+"<P>The number of <B>Cloudfront Functions</B> associated to this account has changed from  : <B>" + str(jsonDataBefore["numberCloudfrontFunctions"])+ "</B> to <B>" + str(jsonDataAfter["numberCloudfrontFunctions"]) + "</B></P>\n"
    changeFlag=1    

if jsonDataBefore["numberClusters"]!=jsonDataAfter["numberClusters"]:
    html=html+"<P>The number of <B>clusters</B> associated to this account has changed from  : <B>" + str(jsonDataBefore["numberClusters"])+ "</B> to <B>" + str(jsonDataAfter["numberClusters"]) + "</B></P>\n"
    changeFlag=1  

if jsonDataBefore["numberEC2Instances"]!=jsonDataAfter["numberEC2Instances"]:
    html=html+"<P>The number of <B>EC2 instances</B> associated to this account has changed from  : <B>" + str(jsonDataBefore["numberEC2Instances"])+ "</B> to <B>" + str(jsonDataAfter["numberEC2Instances"]) + "</B></P>\n"
    changeFlag=1  

if changeFlag==0:
    html=html+"<P>There have been no changes on the configuration values</P>\n"
    


html=html+ "<H2>S3 Buckets</H2>\n"
html=html+ "<H3>S3 Buckets policies change</H3>\n"

changeFlag=0 # Reset the flag
for key,value in jsonDataBefore["S3Buckets_AccessPolicy"].items():
    if key in jsonDataAfter["S3Buckets_AccessPolicy"]:
        if jsonDataBefore["S3Buckets_AccessPolicy"][key]!=jsonDataAfter["S3Buckets_AccessPolicy"][key]:
            html=html+"<P>The policy for S3 bucket <B>" + key + "</B> has changed from <I>" + jsonDataBefore["S3Buckets_AccessPolicy"][key] + "</I> to <I>" + jsonDataAfter["S3Buckets_AccessPolicy"][key] + "</I></P>\n"
            changeFlag=1   
            
if changeFlag==0:
    html=html+"<P>There have been no changes on any S3 Bucket access policy</P>\n"

html=html+ "<H3>New S3 Buckets</H3>\n"
changeFlag=0 # Reset the flag
for key,value in jsonDataAfter["S3Buckets_AccessPolicy"].items():
    if key not in jsonDataBefore["S3Buckets_AccessPolicy"]:
        html=html+"<P>There is a new S3 bucket <B>" + key + "</B> with policy <B>" +  jsonDataAfter["S3Buckets_AccessPolicy"][key] +"</B></P>\n"
        changeFlag=1   

if changeFlag==0:
    html=html+"<P>No new S3 buckets have been added</P>\n"

html=html+ "<H3>Deleted S3 Buckets</H3>\n"
changeFlag=0 # Reset the flag
for key,value in jsonDataBefore["S3Buckets_AccessPolicy"].items():
    if key not in jsonDataAfter["S3Buckets_AccessPolicy"]:
        html=html+"<P>The S3 bucket <B>" + key + "</B> has been deleted</P>\n"
        changeFlag=1   

if changeFlag==0:
    html=html+"<P>No S3 buckets have been deleted</P>\n"









##################################

html=html+ "<H2>Organizational Units</H2>\n"

if jsonDataBefore["OrganizationsInformation"]["numberOrganizationUnits"]!=jsonDataAfter["OrganizationsInformation"]["numberOrganizationUnits"]:
    html=html+"<P>The number of <B>Organizations</B> associated to this account has changed from  : <B>" + str(jsonDataBefore["OrganizationsInformation"]["numberOrganizationUnits"])+ "</B> to <B>" + str(jsonDataAfter["OrganizationsInformation"]["numberOrganizationUnits"]) + "</B></P>\n"

html=html+ "<H3>Deleted Organizations</H3>\n"
changeFlag=0 # Reset the flag
for key,value in jsonDataBefore["OrganizationsInformation"].items():
    if key not in jsonDataAfter["OrganizationsInformation"] and key!="numberOrganizationUnits":
        html=html+"<P>The Organization <B>" + key + "</B> has been deleted</P>\n"
        changeFlag=1   

if changeFlag==0:
    html=html+"<P>No organizations have been deleted</P>\n"

html=html+ "<H3>New Organizations</H3>\n"
changeFlag=0 # Reset the flag
for key,value in jsonDataAfter["OrganizationsInformation"].items():
    if key not in jsonDataBefore["OrganizationsInformation"] and key!="numberOrganizationUnits":
        html=html+"<P>The Organization <B>" + key + "</B> has been deleted</P>\n"
        changeFlag=1   

if changeFlag==0:
    html=html+"<P>No new organizations have been added</P>\n"


html=html+"</body>\n"
html=html+"</head>\n"
  
with open('./comparisonReport.html', 'w') as f: #The report name is harcoded.
    f.write(html)
    


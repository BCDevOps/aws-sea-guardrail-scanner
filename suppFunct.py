import os
import datetime
import json
from os.path import exists
import subprocess

##############################################
# Functions
##############################################

##### Save the key/value pair in a given json file
def saveValues(fileName,Name,Value,flag): 
    with open(fileName, 'a') as f:
        if flag: #if true save with a comma at the end
            f.write('   '+ Name.rstrip('\r\n') + ' : ' +Value.rstrip('\r\n')+ ',\n')
        else:# false no comma
            f.write('   '+ Name.rstrip('\r\n') + ' : ' +Value.rstrip('\r\n')+ '\n')
                
            
def addQuotes(Value):
    return '\"'+ Value.rstrip('\r\n') + '\"'           

def addTab(Value):
    return '   '+ Value     

##### To read files that contain a single piece of information
def getOutput(fileName):
    if os.path.exists(fileName):
        fp = open(fileName, "r")
        output=fp.read()
        fp.close()
        os.remove(fileName)
        if len(output)>0:
            return output
        else:
            return "\"n/a\""

##### returns the length of a given key in a json file
def getOutputApi(fileName,node): 
    if os.path.exists(fileName):    
        os.system( ' jq \'.' + node + ' | length\' '+ fileName + ' > borrar.json')
        output=getOutput('./borrar.json')
        delFile('./borrar.json')
        return output


##### Returns the value of a given key in a json file
def returnValue(fileName,key): 
    if os.path.exists(fileName):  
        os.system( 'jq \'.' + key + '\'' + ' ./' + fileName + ' > borrar.json')
        output=getOutput('./borrar.json')
        delFile('./borrar.json')
        return str(output).replace('"','').replace('\n','')


    
def closeResultsFile(resultsFile,LicensePlate,awsRoleUsed,LZ):
    with open(resultsFile, 'a') as f:
        f.write('   \"TestInformation\": ' +' {\n')
        f.write('       \"DateTime\" : "' +str(datetime.datetime.now())+ '",\n')
        f.write('       \"awsRoleUsed\" : "' + awsRoleUsed + '",\n')
        f.write('       \"AWS_DEFAULT_REGION\" : "' + os.environ.get('AWS_DEFAULT_REGION') + '",\n')
        f.write('       \"LicensePlate\" : "' + LicensePlate + '",\n')
        f.write('       \"Landing Zone\" : \"LZ' + str(LZ) + '"\n')
        f.write('   }\n')
        f.write('}')
        
        return

def delFile(fileName):
    if os.path.exists(fileName):
        os.remove(fileName)
        return


def checkExistCreate(fileName): # Checks the existence of the results file, if already exist it will be deleted...
    if os.path.exists(fileName):
        print("Script will remove  the existing file " + fileName)
        os.remove(fileName)
    
    if not os.path.exists("./results"):
        print("Folder ./results has been created")
        os.mkdir("./results")
    
    
    print("Script will (re)create the file " + fileName)
    with open(fileName, 'w') as f:
        f.write('{\n')
        
    return    
        
def addHeader(title):
    html="<html xmlns=\"https://www.w3.org/1999/xhtml\" lang=\"ca\" xml:lang=\"ca\">\n"     
    html=html+ "<head>\n"
    html=html+ "<style>\n"
    html=html+ "body {\n"
    html=html+ "    font-family: Arial, Helvetica, sans-serif;\n"
    html=html+ "}\n"

    html=html+ "/* Dashed border */\n"
    html=html+ "hr.dashed {\n"
    html=html+ "    border-top: 3px dashed #bbb;\n"
    html=html+ "}\n"

    html=html+ "/* Dotted border */\n"
    html=html+ "hr.dotted {\n"
    html=html+ "    border-top: 3px dotted #bbb;\n"
    html=html+ "}\n"

    html=html+ "/* Solid border */\n"
    html=html+ "hr.solid {\n"
    html=html+ "    border-top: 3px solid #bbb;\n"
    html=html+ "}\n"

    html=html+ "/* Rounded border */\n"
    html=html+ "hr.rounded {\n"
    html=html+ "    border-top: 8px solid #bbb;\n"
    html=html+ "    border-radius: 5px;\n"
    html=html+ "}\n"

    html=html+ "table, th, td {\n"
    html=html+ "border: 1px solid black;\n"
    html=html+ "border-collapse: collapse;\n"
    html=html+ "}\n"   
    html=html+ "</style>\n"
    
    html=html+ "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />\n"
    html=html+ "<link href='https://fonts.googleapis.com/css?family=Open+Sans+Condensed:300' rel='stylesheet' type='text/css' />\n"
    html=html+ "<title>Guardrails Snapshot - " + title + "</title>\n"
    html=html+ "</head>\n"
    html=html+ "<body>\n"
    html=html+ "<H1><center>Guardrails Snapshot - " + title + "</center></H1>\n"
    html=html+ "<hr class=\"rounded\">\n"
    html=html+ "<H2>Test Information</H2>\n"
    
    return html


def importJsonFile(jsonFile):
    try:
        with open(jsonFile, 'r') as json_file:
            json_data = json.load(json_file)
            return json_data
    except FileNotFoundError:
        print('\"'+ jsonFile + '\"' + 'not found')
        quit()   

        
##### Changes the values of the env variables for the AWS credentials        
def setCredentials(Credentials):  
    os.environ["AWS_ACCESS_KEY_ID"] = str(Credentials[0])
    os.environ["AWS_SECRET_ACCESS_KEY"] = str(Credentials[1])
    os.environ["AWS_SESSION_TOKEN"] = str(Credentials[2]) 
    return
        

 
 
##### Function to compare the guardrails 
def compareFile(olderSnapshotConfigName,newerSnapshotConfigName,olderSnapshotPoliciesName,newerSnapshotPoliciesName): 
  
    # This function process two different kinds of files. 
    # The ones produced by getSnapshot.py (the "manual" snapshot) produces files like
    #        20220829_workloadAdminConfig_f2u30s-dev_LZ1.json
    # while the files produced by getFullSnapshot.py (the "automated" snapshot)produces files like
    #        20220913_AWSCloudFormationStackSetExecutionRole_Policies_f2u30s-tools_LZ1.json
    if len(olderSnapshotConfigName.split("_"))==4:
        # "Manual" snapshot
        roleType=olderSnapshotConfigName.split("_")[1]
        licensePlate=olderSnapshotConfigName.split("_")[2]
    elif  len(olderSnapshotConfigName.split("_"))==5: 
        # "Automated" snapshot
        roleType=olderSnapshotConfigName.split("_")[1]+"_"+olderSnapshotConfigName.split("_")[2]
        licensePlate=olderSnapshotConfigName.split("_")[3]
    elif  len(olderSnapshotConfigName.split("_"))>5: 
        # "BCGOV_MASTER" account snapshot
        roleType=olderSnapshotConfigName.split("_")[1]+ "_" + olderSnapshotConfigName.split("_")[2] + "_" + olderSnapshotConfigName.split("_")[3]+ "_" + olderSnapshotConfigName.split("_")[4]+ "_" + olderSnapshotConfigName.split("_")[5] # Gets the role + config string
        licensePlate=olderSnapshotConfigName.split("_")[6] # Gets the license plate 
    else:
        print("The name of the file does not follow the standard format")
        quit()    
        

    
    
    olderSnapshotConfig=importJsonFile("./results/"+olderSnapshotConfigName)
    newerSnapshotConfig=importJsonFile("./results/"+newerSnapshotConfigName)
    
    olderSnapshotPolicies=importJsonFile("./results/"+olderSnapshotPoliciesName)
    newerSnapshotPolicies=importJsonFile("./results/"+newerSnapshotPoliciesName)

    LZ=olderSnapshotConfig["TestInformation"]["Landing Zone"][-1]
    olderDate=olderSnapshotConfig["TestInformation"]["DateTime"].split(" ")[0].replace("-","")
    newerDate=newerSnapshotConfig["TestInformation"]["DateTime"].split(" ")[0].replace("-","")
        
 #   if olderSnapshotConfig["TestInformation"]["awsRoleUsed"]!=newerSnapshotConfig["TestInformation"]["awsRoleUsed"] or olderSnapshotConfig["TestInformation"]["AWS_DEFAULT_REGION"]!=newerSnapshotConfig["TestInformation"]["AWS_DEFAULT_REGION"] or olderSnapshotConfig["TestInformation"]["Landing Zone"]!=newerSnapshotConfig["TestInformation"]["Landing Zone"]or olderSnapshotConfig["TestInformation"]["LicensePlate"]!=newerSnapshotConfig["TestInformation"]["LicensePlate"]:
 #       print("You are comparing the wrong snapshots, either the account, region or Landing Zone are not the same")
 #       quit()


    title = "LZ" + LZ + " Configuration comparison between " + olderSnapshotConfig["TestInformation"]["DateTime"]  + " and " + newerSnapshotConfig["TestInformation"]["DateTime"] #The title of the report
    html = addHeader(title)


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

        
    if olderSnapshotConfig["awsNumberIamGroups"]!=newerSnapshotConfig["awsNumberIamGroups"]:
        html=html+"<P>The number of <B>AWS IAM groups</B> in LZ" + LZ + "  has changed from : <B>" + str(olderSnapshotConfig["awsNumberIamGroups"])+ "</B> to <B>" + str(newerSnapshotConfig["awsNumberIamGroups"]) + "</B></P>\n"
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


    ################################## AWS IAM Users
    html=html+ "<hr class=\"dashed\">\n"
    html=html+ "<H2>AWS IAM Users</H2>\n"

    if olderSnapshotConfig["awsNumberIamUsers"]!=newerSnapshotConfig["awsNumberIamUsers"]:
        html=html+"<P>The number of <B>AWS IAM Users</B> in LZ" + LZ+ "  has changed from  : <B>" + str(olderSnapshotConfig["awsNumberIamUsers"])+ "</B> to <B>" + str(newerSnapshotConfig["awsNumberIamUsers"]) + "</B></P>\n"

    html=html+ "<H3>AWS IAM Users with Attached policies changes</H3>\n"

    changeFlag=0 # Reset the flag
    
    if "ListIAMUsers" in olderSnapshotConfig:
        for key,value in olderSnapshotConfig["ListIAMUsers"].items():
            if key in newerSnapshotConfig["ListIAMUsers"]:
                if olderSnapshotConfig["ListIAMUsers"][key]!=newerSnapshotConfig["ListIAMUsers"][key]:
                    html=html+"<P>The AWS IAM User with name <B>" + key + "</B> has changed its Arn from <I>" + str(olderSnapshotConfig["ListIAMUsers"][key]) + "</I> to <I>" + str(newerSnapshotConfig["ListIAMUsers"][key]) + "</I></P>\n"
                    changeFlag=1   
                    
        if changeFlag==0:
            html=html+"<P>There have been no changes in any AWS IAM Users Attached policies</P>\n"

    html=html+ "<H3>New AWS IAM Users</H3>\n"
    changeFlag=0 # Reset the flag
    
    #if "ListIAMUsers" in newerSnapshotConfig:
    #    for key,value in newerSnapshotConfig["ListIAMUsers"].items():
    #        if len(olderSnapshotConfig["ListIAMUsers"])>0 and key not in olderSnapshotConfig["ListIAMUsers"]:
    #            html=html+"<P>There is a new AWS IAM User with name <B>" + key + "</B> and with Arn <B>" +  newerSnapshotConfig["ListIAMUsers"][key] +"</B></P>\n"
    #            changeFlag=1   

    #if changeFlag==0:
    #    html=html+"<P>No new AWS IAM Users have been added</P>\n"

    html=html+ "<H3>Deleted AWS IAM Users</H3>\n"
    changeFlag=0 # Reset the flag
    if "ListIAMUsers" in olderSnapshotConfig:
        for key,value in olderSnapshotConfig["ListIAMUsers"].items():
            if "ListIAMUsers" in newerSnapshotConfig:
                if len(newerSnapshotConfig["ListIAMUsers"])>0 and key not in newerSnapshotConfig["ListIAMUsers"]:
                    html=html+"<P>The AWS IAM User with name <B>" + key + "</B> has been deleted</P>\n"
                    changeFlag=1
            else: changeFlag=1

    if changeFlag==0:
        html=html+"<P>No AWS IAM Users have been deleted</P>\n"


    ################################## Accounts
    html=html+ "<hr class=\"dashed\">\n"
    html=html+ "<H2>Accounts</H2>\n"

    if olderSnapshotConfig["awsTotalNumberAccounts"]!=newerSnapshotConfig["awsTotalNumberAccounts"]:
        html=html+"<P>The number of <B>accounts</B> in LZ" + LZ + "  has changed from  : <B>" + str(olderSnapshotConfig["awsTotalNumberAccounts"])+ "</B> to <B>" + str(newerSnapshotConfig["awsTotalNumberAccounts"]) + "</B></P>\n"


    html=html+ "<H3>Account with Arn change</H3>\n"

    changeFlag=0 # Reset the flag
    for key,value in olderSnapshotConfig["List_of_Accounts"].items():
        if key in newerSnapshotConfig["List_of_Accounts"]:
            if olderSnapshotConfig["List_of_Accounts"][key]!=newerSnapshotConfig["List_of_Accounts"][key]:
                html=html+"<P>The Account with name <B>" + key + "</B> has changed its Arn from <I>" + olderSnapshotConfig["List_of_Accounts"][key] + "</I> to <I>" + newerSnapshotConfig["List_of_Accounts"][key] + "</I></P>\n"
                changeFlag=1   
                
    if changeFlag==0:
        html=html+"<P>There have been no changes in any Account Arn</P>\n"

    html=html+ "<H3>New Accounts</H3>\n"
    changeFlag=0 # Reset the flag
    for key,value in newerSnapshotConfig["List_of_Accounts"].items():
        if key not in olderSnapshotConfig["List_of_Accounts"]:
            html=html+"<P>There is a Account with name <B>" + key + "</B> and with Arn <B>" +  newerSnapshotConfig["List_of_Accounts"][key] +"</B></P>\n"
            changeFlag=1   

    if changeFlag==0:
        html=html+"<P>No new Accounts have been added</P>\n"

    html=html+ "<H3>Deleted Accounts</H3>\n"
    changeFlag=0 # Reset the flag
    for key,value in olderSnapshotConfig["List_of_Accounts"].items():
        if key not in newerSnapshotConfig["List_of_Accounts"]:
            html=html+"<P>The Account with name <B>" + key + "</B> has been deleted</P>\n"
            changeFlag=1   

    if changeFlag==0:
        html=html+"<P>No accounts have been deleted</P>\n"


    ################################## Lambda Functions
    html=html+ "<hr class=\"dashed\">\n"
    html=html+ "<H2>Lambda Functions</H2>\n"

    if olderSnapshotConfig["numberLambdaFunctions"]!=newerSnapshotConfig["numberLambdaFunctions"]:
        html=html+"<P>The number of <B>Lambda Functions</B> associated to this account has changed from  : <B>" + str(olderSnapshotConfig["numberLambdaFunctions"])+ "</B> to <B>" + str(newerSnapshotConfig["numberLambdaFunctions"]) + "</B></P>\n"


    html=html+ "<H3>Lambda functions with Arn change</H3>\n"

    changeFlag=0 # Reset the flag
    for key,value in olderSnapshotConfig["List_of_Lambda_Functions"].items():
        if key in newerSnapshotConfig["List_of_Lambda_Functions"]:
            if olderSnapshotConfig["List_of_Lambda_Functions"][key]!=newerSnapshotConfig["List_of_Lambda_Functions"][key]:
                html=html+"<P>The Lambda Function <B>" + key + "</B> has changed from <I>" + olderSnapshotConfig["List_of_Lambda_Functions"][key] + "</I> to <I>" + newerSnapshotConfig["List_of_Lambda_Functions"][key] + "</I></P>\n"
                changeFlag=1   
                
    if changeFlag==0:
        html=html+"<P>There have been no changes in any Lambda Function Arn</P>\n"

    html=html+ "<H3>New Lambda Functions</H3>\n"
    changeFlag=0 # Reset the flag
    for key,value in newerSnapshotConfig["List_of_Lambda_Functions"].items():
        if key not in olderSnapshotConfig["List_of_Lambda_Functions"]:
            html=html+"<P>There is a new Lambda Function <B>" + key + "</B> with Arn <B>" +  newerSnapshotConfig["List_of_Lambda_Functions"][key] +"</B></P>\n"
            changeFlag=1   

    if changeFlag==0:
        html=html+"<P>No new Lambda Functions have been added</P>\n"

    html=html+ "<H3>Deleted Lambda Functions</H3>\n"
    changeFlag=0 # Reset the flag
    for key,value in olderSnapshotConfig["List_of_Lambda_Functions"].items():
        if key not in newerSnapshotConfig["List_of_Lambda_Functions"]:
            html=html+"<P>The Lambda Function <B>" + key + "</B> has been deleted</P>\n"
            changeFlag=1   

    if changeFlag==0:
        html=html+"<P>No Lambda Functions have been deleted</P>\n"


    ################################## S3 Buckets
    html=html+ "<hr class=\"dashed\">\n"
    html=html+ "<H2>S3 Buckets</H2>\n"


    if olderSnapshotConfig["awsNumber_S3_Buckets"]!=newerSnapshotConfig["awsNumber_S3_Buckets"]:
        html=html+"<P>The number of <B>S3 Buckets</B> associated to this account has changed from  : <B>" + str(olderSnapshotConfig["awsNumber_S3_Buckets"])+ "</B> to <B>" + str(newerSnapshotConfig["awsNumber_S3_Buckets"]) + "</B></P>\n"


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



    ################################## Roles

    html=html+ "<hr class=\"dashed\">\n"
    html=html+ "<H2>Roles</H2>\n"

    if olderSnapshotConfig["awsNumberRoles"]!=newerSnapshotConfig["awsNumberRoles"]:
        html=html+"<P>The number of <B>roles</B> associated to the user in LZ" + LZ+ "  has changed from  : <B>" + str(olderSnapshotConfig["awsNumberRoles"])+ "</B> to <B>" + str(newerSnapshotConfig["awsNumberRoles"]) + "</B></P>\n"
        changeFlag=1

    html=html+ "<H3>Roles changes: It keeps the same name, but arn has changed</H3>\n"

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
    html=html+"</html>\n"
    

    with open('./'+ olderDate + '_' + newerDate + '_' + roleType + "_" + licensePlate + "_LZ" + LZ+ '.html', 'w') as f: #The report name is harcoded.
        f.write(html)
        
    return
                


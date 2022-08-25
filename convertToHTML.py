import os
import json
import suppFunct
from os.path import exists


#def convertToHTML(value):
#    convertKeyParam() if value=="1" else  convertPoliciesRoles() if  value=="2"  else print("Not a valid input number")
#    return
###########################################  

def importJsonFile(jsonFile):
    try:
        with open(jsonFile, 'r') as json_file:
            json_data = json.load(json_file)
            return json_data
    except FileNotFoundError:
        print("my_file not found")
    return    
        
###########################################     
def convertKeyParam(resultsFile,LZ):
    jsonData=importJsonFile(resultsFile)  #The json file used as input    
    title = "LZ" + LZ + "</B>: Configuration - " + jsonData["TestInformation"]["DateTime"] #The title of the report

    html = suppFunct.addHeader(title)
       
    jsn_list = jsonData['TestInformation']
    for key in jsn_list:
        html=html+"<P><B>" + key + "</B> : " + jsn_list[key] + " </P>\n"

    html=html+ "<hr class=\"dashed\">\n"

    html=html+ "<H2>LZ" + LZ + "</B> :  configuration values</H2>\n"
    html=html+"<P><B>Number of AWS IAM users in LZ" + LZ + "</B> : " + str(jsonData["awsNumberIamUsers"])+ " </P>\n"
    html=html+"<P><B>Number of AWS IAM groups in LZ" + LZ + "</B> : " + str(jsonData["awsNumberIamGroups"]) + " </P>\n"
    html=html+"<P><B>Number of AWS IAM policies in LZ" + LZ + "</B> : " +str(jsonData["awsNumberIamPolicies"]) + " </P>\n"

    html=html+"<P><B>Number of IAM roles associated to the user in LZ" + LZ + "</B> : " + str(jsonData["awsNumberIamRoles"]) + " </P>\n"
    html=html+"<P><B>Number of Policies available to the AWS account in LZ" + LZ + "</B> : " + str(jsonData["awsNumberAvailablePolicies"]) + " </P>\n"
    html=html+"<P><B>Number of accounts in LZ" + LZ + "</B> : " +str(jsonData["awsTotalNumberAccounts"]) + " </P>\n"

    html=html+"<P><B>Number of Cloudfront Distributions associated to this account</B> : " +str(jsonData["numberCloudfrontDistributions"]) + " </P>\n"
    html=html+"<P><B>Number of Cloudfront Functions associated to this account</B> : " +str(jsonData["numberCloudfrontFunctions"]) + " </P>\n"
    html=html+"<P><B>Number of clusters associated to this account</B> : " +str(jsonData["numberClusters"]) + " </P>\n"
    html=html+"<P><B>Number of EC2 instances associated to this account</B> : " +str(jsonData["numberEC2Instances"]) + " </P>\n"    
   
    html=html+ "<hr class=\"dashed\">\n"
    html=html+ "<H2>Lambda Functions</H2>\n"
    html=html+"<P><B>Number of Lambda functions associated to this account</B> : " +str(jsonData["numberLambdaFunctions"]) + " </P>\n"    
    html=html+ "<H3>List of Lambda Functions- <I> Name : Arn</I></H3>\n"
    html=html+"<UL>"
    jsn_list = jsonData['List_of_Lambda_Functions']
    for key in jsn_list:
        html=html+"<LI><B>      " + key + "</B> : " + jsn_list[key] + " </LI>\n"
    html=html+"</UL>"

    html=html+ "<hr class=\"dashed\">\n"
    html=html+ "<H2>S3 buckets values</H2>\n"
    html=html+"<P><B>Number of S3 buckets in LZ" + LZ + "</B> : " +str(jsonData["awsNumber_S3_Buckets"]) + " </P>\n"
    html=html+ "<H3>List of S3 buckets and block access policy status</H3>\n"
    html=html+ "<P>a n/a label means there is no policy associated to the S3 Bucket, by default, access is denied so there is no public access </P>\n"
    html=html+"<UL>"
    jsn_list = jsonData['S3Buckets_AccessPolicy']
    for key in jsn_list:
        html=html+"<LI><B>      " + key + "</B> : " + jsn_list[key] + " </LI>\n"
    html=html+"</UL>"
    
    html=html+ "<hr class=\"dashed\">\n"
    html=html+ "<H2>Roles for this account</H2>\n"
    html=html+"<P><B>Number of roles for this account in LZ" + LZ + "</B> : " + str(jsonData["awsNumberRoles"]) + " </P>\n"
    html=html+ "<H3>List of Roles - <I>Role Name : Arn</I></H3>\n"
    html=html+"<UL>"
    jsn_list = jsonData['List_of_Roles_for_the_Account']
    for key in jsn_list:
        html=html+"<LI><B>      " + key + "</B> : " + jsn_list[key] + " </LI>\n"
    html=html+"</UL>"
    
    html=html+ "<hr class=\"dashed\">\n"
    html=html+ "<H2>Task Definitions</H2>\n"
    html=html+"<P><B>Number of task definitions associated to this LZ" + LZ + " account</B> : " +str(jsonData["numberOfTaskDefinition"]) + " </P>\n"
    html=html+ "<H3>List of Tasks definitions Arns </H3>\n"
   #html=html+ "<P>a n/a label means there is no policy associated to the S3 Bucket, by default, access is denied so there is no public access </P>\n"
    html=html+"<UL>"
    jsn_list = jsonData['TaskDefinitionArns']
    for key in jsn_list:
        html=html+"<LI><B>      " + key + "</B></LI>\n"
    html=html+"</UL>"
    
    html=html+ "<hr class=\"dashed\">\n"
    html=html+ "<H2>Organization Information</H2>\n"
    html=html+"<P><B>Number of organizations in LZ" + LZ + "</B> : " +str(jsonData["OrganizationsInformation"]["numberOrganizationUnits"]) + " </P>\n"
    html=html+"<UL>"
    jsn_list = jsonData['OrganizationsInformation']
    for key in jsn_list:
        if key !="numberOrganizationUnits":
            html=html+"<LI><B>      " + key.split("_",1)[1] + "</B> : " + str(jsn_list[key]) + " </LI>\n"
    html=html+"</UL>"
    html=html+"</body>\n"
    html=html+"</head>\n"
  
    with open('./' + resultsFile.split('.')[1] + '.html', 'w') as f: 
        f.write(html)
    
    return  

###########################################
    
def convertPoliciesRoles(resultsFile,LZ):
    jsonData=importJsonFile(resultsFile)  #The json file used as input      
    title = "LZ" + LZ + "</B> : Policies - " + jsonData["TestInformation"]["DateTime"] 

    html =  suppFunct.addHeader(title)
       
    jsn_list = jsonData['TestInformation']
    for key in jsn_list:
        html=html+"<P><B>" + key + "</B> : " + jsn_list[key] + " </P>\n"

    html=html+ "<hr class=\"dashed\">\n"

    html=html+ "<H2>Managed Policies Attached to IAM Role</H2>\n"
    
    #jsn_list = jsonData['S3Buckets_AccessPolicy']
    html=html+"<UL>"
    for key in jsonData:
        mykey=key.split("_",1)
        if mykey[0] =="managedPoliciesAttachedToIAMRole":
            html=html+"<LI><B>      " + mykey[1]+ "</B> : " + str(jsonData[key]) + " </LI>\n"
    html=html+"</UL>"
    
    html=html+ "<hr class=\"dashed\">\n"
    html=html+ "<H2>In Line Policies Embedded to IAM Role</H2>\n"
    html=html+"<UL>"
    for key in jsonData:
        mykey=key.split("_",1)
        if mykey[0] =="inlinePoliciesEmbeddedToIamRole":
            html=html+"<LI><B>      " + mykey[1] + "</B> : " + str(jsonData[key]) + " </LI>\n"
    html=html+"</UL>"
      
    html=html+"</body>\n"
    html=html+"</head>\n"
  
    with open('./' + resultsFile.split('.')[1] + '.html', 'w') as f: 
        f.write(html)  
        
    return  
      

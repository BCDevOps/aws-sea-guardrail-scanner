import os
import json
import suppFunct
from os.path import exists


def convertToHTML(value):
    convertKeyParam() if value=="1" else  convertPoliciesRoles() if  value=="2"  else print("Not a valid input number")
    return


 

def importJsonFile(jsonFile):
    try:
        with open(jsonFile, 'r') as json_file:
            json_data = json.load(json_file)
            return json_data
    except FileNotFoundError:
        print("my_file not found")
        
###########################################     
def convertKeyParam():
    jsonData=importJsonFile('./resultsKeyParameters.json')  #The json file used as input    
    title = "LZ2 Configuration - " + jsonData["TestInformation"]["DateTime"] #The title of the report

    html = suppFunct.addHeader(title)
       
    jsn_list = jsonData['TestInformation']
    for key in jsn_list:
        html=html+"<P><B>" + key + "</B> : " + jsn_list[key] + " </P>\n"

    html=html+ "<hr class=\"dashed\">\n"

    html=html+ "<H2>LZ2 configuration values</H2>\n"
    html=html+"<P><B>Number of AWS IAM users in LZ2</B> : " + str(jsonData["awsNumberIamUsers"])+ " </P>\n"
    html=html+"<P><B>Number of AWS IAM groups in LZ2</B> : " + str(jsonData["awsNumberIamGroups"]) + " </P>\n"
    html=html+"<P><B>Number of AWS IAM roles in LZ2</B> : " + str(jsonData["awsNumberIamRoles"]) + " </P>\n"
    html=html+"<P><B>Number of AWS IAM policies in LZ2</B> : " +str(jsonData["awsNumberIamPolicies"]) + " </P>\n"

    html=html+"<P><B>Number of roles associated to the admin user in LZ2</B> : " + str(jsonData["awsNumberRoles"]) + " </P>\n"
    html=html+"<P><B>Number of Policies available to the AWS account in LZ2</B> : " + str(jsonData["awsNumberAvailablePolicies"]) + " </P>\n"
    html=html+"<P><B>Number of accounts in LZ2</B> : " +str(jsonData["awsTotalNumberAccounts"]) + " </P>\n"

    html=html+"<P><B>Number of Cloudfront Distributions associated to this account</B> : " +str(jsonData["numberCloudfrontDistributions"]) + " </P>\n"
    html=html+"<P><B>Number of Cloudfront Functions associated to this account</B> : " +str(jsonData["numberCloudfrontFunctions"]) + " </P>\n"
    html=html+"<P><B>Number of clusters associated to this account</B> : " +str(jsonData["numberClusters"]) + " </P>\n"
    html=html+"<P><B>Number of EC2 instances associated to this account</B> : " +str(jsonData["numberEC2Instances"]) + " </P>\n"    


    html=html+ "<hr class=\"dashed\">\n"
    html=html+ "<H2>S3 buckets values</H2>\n"
    html=html+"<P><B>Number of S3 buckets in LZ2</B> : " +str(jsonData["awsNumber_S3_Buckets"]) + " </P>\n"
    html=html+ "<H3>List of S3 buckets and block access policy status</H3>\n"
    html=html+"<UL>"
    jsn_list = jsonData['S3Buckets_AccessPolicy']
    for key in jsn_list:
        html=html+"<LI><B>      " + key + "</B> : " + jsn_list[key] + " </LI>\n"
    html=html+"</UL>"
    
    html=html+ "<hr class=\"dashed\">\n"
    html=html+ "<H2>Organization Information</H2>\n"
    html=html+"<P><B>Number of organizations in LZ2</B> : " +str(jsonData["OrganizationsInformation"]["numberOrganizationUnits"]) + " </P>\n"
    html=html+"<UL>"
    jsn_list = jsonData['OrganizationsInformation']
    for key in jsn_list:
        if key !="numberOrganizationUnits":
            html=html+"<LI><B>      " + key.split("_")[1] + "</B> : " + str(jsn_list[key]) + " </LI>\n"
    html=html+"</UL>"
    html=html+"</body>\n"
    html=html+"</head>\n"
  
    with open('./resultsKeyParameters.html', 'w') as f: #The report name is harcoded.
        f.write(html)


###########################################
    
def convertPoliciesRoles():
    jsonData=importJsonFile('./resultsPoliciesInRoles.json')
    title = "LZ2 Policies - " + jsonData["TestInformation"]["DateTime"] 

    html =  suppFunct.addHeader(title)
       
    jsn_list = jsonData['TestInformation']
    for key in jsn_list:
        html=html+"<P><B>" + key + "</B> : " + jsn_list[key] + " </P>\n"

    html=html+ "<hr class=\"dashed\">\n"

    html=html+ "<H2>Managed Policies Attached to IAM Role</H2>\n"
    
    #jsn_list = jsonData['S3Buckets_AccessPolicy']
    html=html+"<UL>"
    for key in jsonData:
        mykey=key.split("_")
        if mykey[0] =="managedPoliciesAttachedToIAMRole":
            html=html+"<LI><B>      " + mykey[1]+ "</B> : " + str(jsonData[key]) + " </LI>\n"
    html=html+"</UL>"
    
    html=html+ "<hr class=\"dashed\">\n"
    html=html+ "<H2>In Line Policies Embedded to IAM Role</H2>\n"
    html=html+"<UL>"
    for key in jsonData:
        mykey=key.split("_")
        if mykey[0] =="inlinePoliciesEmbeddedToIamRole":
            html=html+"<LI><B>      " + mykey[1] + "</B> : " + str(jsonData[key]) + " </LI>\n"
    html=html+"</UL>"
      
    html=html+"</body>\n"
    html=html+"</head>\n"
  
    with open('./resultsPoliciesInRoles.html', 'w') as f:
        f.write(html)  
      
###########################################
# Main program
###########################################

print('Enter a number to convert the following predefined files from json to HTML')
print('- 1 parse resultsKeyParameters.json')
print('- 2 parse resultsPoliciesRoles.json')
sel = input()

myFlag=convertToHTML(sel)



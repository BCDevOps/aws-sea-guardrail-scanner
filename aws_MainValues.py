
import os

import suppFunct
from os.path import exists

# To run the script you need to export the following values as env variables, or if executing
# the script in GiHub action, you need to add these values as secrets
#  AWS_ACCESS_KEY_ID
#  AWS_SECRET_ACCESS_KEY
#  AWS_SESSION_TOKEN
#  AWS_DEFAULT_REGION


AWS_ACCESS_KEY_ID=os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY=os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_SESSION_TOKEN=os.environ.get('AWS_SESSION_TOKEN')
AWS_DEFAULT_REGION=os.environ.get('AWS_DEFAULT_REGION')


awsAccountUsed="BCGOV_MASTER_admin_umafubc9"
resultsFile="./resultsKeyParameters.json"


suppFunct.checkExistCreate(resultsFile)


############################################################################################
########   Gathering the data section
############################################################################################


##############################################
# Using the get-account-authorization-details  API
##############################################
# Checks the number of AWS users with access to LZ2 Landing Zone (IAM > Users)
##############################################    
os.system('aws iam  get-account-authorization-details > apiResults.json')
output=suppFunct.getOutputApi('./apiResults.json','UserDetailList') 
suppFunct.saveValues(resultsFile,suppFunct.addQuotes('awsNumberIamUsers'),output, True)   
##############################################
# Checks the number of IAM groups inLZ2 Landing Zone (IAM > User Groups)
##############################################    
#os.system('aws iam  get-account-authorization-details  | jq \'.GroupDetailList | length\' > borrar.json')
output=suppFunct.getOutputApi('./apiResults.json','GroupDetailList')
suppFunct.saveValues(resultsFile,suppFunct.addQuotes('awsNumberIamGroups'),output, True)    
##############################################
# Checks the number of IAM roles in LZ2 Landing Zone (IAM > Roles)
##############################################    
#os.system('aws iam  get-account-authorization-details  | jq \'.RoleDetailList | length\' > borrar.json')
output=suppFunct.getOutputApi('./apiResults.json','RoleDetailList')
suppFunct.saveValues(resultsFile,suppFunct.addQuotes('awsNumberIamRoles'),output, True)   
##############################################
# Checks the number of IAM Policies in LZ2 Landing Zone  (IAM > Policies)
##############################################    
#os.system('aws iam  get-account-authorization-details  | jq \'.Policies | length\' > borrar.json')
output=suppFunct.getOutputApi('./apiResults.json','Policies')
suppFunct.saveValues(resultsFile,suppFunct.addQuotes('awsNumberIamPolicies'),output, True)   

suppFunct.delFile('./apiResults.json')


##############################################
# Checks the number of S3 Buckets associated to the admin user in LZ2
##############################################    
os.system('aws s3 ls > ./apiResults.txt')

os.system('wc -l < ./apiResults.txt >borrar.json')
numberOfBuckets=suppFunct.getOutput('./borrar.json') 
suppFunct.saveValues(resultsFile,suppFunct.addQuotes('awsNumber_S3_Buckets'),numberOfBuckets, True)    

with open(resultsFile, 'a') as f:
    f.write(suppFunct.addTab(suppFunct.addQuotes('S3Buckets_AccessPolicy')) +' : {\n')
    
myApiResults=open('./apiResults.txt',"r")

myCounter=1

for line in myApiResults:
    print(str(myCounter) + ' ' + numberOfBuckets)
    myLine = line.replace('\"',"").replace('\'',"").split(" ") #myLine[2] is the  Name of the bucket
    os.system('aws s3api get-public-access-block --bucket '+ myLine[2].rstrip('\r\n') + ' | jq \'.PublicAccessBlockConfiguration |{BlockPublicAcls,IgnorePublicAcls,BlockPublicPolicy,RestrictPublicBuckets}\' > myBlocks.json')
    
    os.system('jq -r \'[.[]] | @csv \' myBlocks.json > myBlocks.txt') #Convert the json file to csv, makes life easier for next iteration
    myBlocks=open('./myBlocks.txt',"r")
    blocks=myBlocks.read()
    
    if myCounter<int(numberOfBuckets):
        if len(blocks)>2: 
            suppFunct.saveValues(resultsFile,suppFunct.addTab(suppFunct.addQuotes(myLine[2])),suppFunct.addQuotes('Has Public Access Block'),True)
        else:
            suppFunct.saveValues(resultsFile,suppFunct.addTab(suppFunct.addQuotes(myLine[2])),suppFunct.addQuotes('Does not have a Public Access Block'),True)
    else:
        if len(blocks)>2: 
            suppFunct.saveValues(resultsFile,suppFunct.addTab(suppFunct.addQuotes(myLine[2])),suppFunct.addQuotes('Has Public Access Block'),False)
        else:
            suppFunct.saveValues(resultsFile,suppFunct.addTab(suppFunct.addQuotes(myLine[2])),suppFunct.addQuotes('Does not have a Public Access Block'),False)
   
    myCounter+=1    
    suppFunct.delFile('./myBlocks.txt')
    suppFunct.delFile('./myBlocks.json')
      




   
#    os.system('jq -r \'[.[]] | @csv \' myBlocks.json > myBlocks.txt') #Convert the json file to csv, makes life easier for next iteration
#    myBlocks=open('./myBlocks.txt',"r")
    
#    blocks=myBlocks.read() #Read the contents, should be a collection of true/false
#    blocks = blocks.replace('\"',"").replace('\'',"").split(",") #We get the  Name of the bucket
    
#    if myCounter<int(numberOfBuckets):
#        if (blocks[0].rstrip('\r\n')=='true' and blocks[1].rstrip('\r\n')=='true' and blocks[2].rstrip('\r\n')=='true' and blocks[3].rstrip('\r\n')=='true'):
#            saveValues(addTab(suppFunct.addQuotes('isBlocked_'+myLine[2])),"True","True")
#        else:
#            saveValues(addTab(suppFunct.addQuotes('isBlocked_'+myLine[2])),"False","True")
#    else:
#        if (blocks[0].rstrip('\r\n')=='true' and blocks[1].rstrip('\r\n')=='true' and blocks[2].rstrip('\r\n')=='true' and blocks[3].rstrip('\r\n')=='true'):
#            saveValues(addTab(suppFunct.addQuotes('isBlocked_'+myLine[2])),"True","False")
#        else:
#            saveValues(addTab(suppFunct.addQuotes('isBlocked_'+myLine[2])),"False","False")
                        
#    myCounter+=1    
#    delFile('./myBlocks.txt')
#    delFile('./myBlocks.json')
    
            
with open(resultsFile, 'a') as f:
    f.write('    },\n')


##############################################
# Checks the number of roles associated to the admin user in LZ2
##############################################    
os.system('aws iam  list-roles | jq \'.Roles | length\' > borrar.json')
output=suppFunct.getOutput('./borrar.json') 
suppFunct.saveValues(resultsFile,suppFunct.addQuotes('awsNumberRoles'),output, True)    

##############################################
# Checks the number of Policies available to the AWS account in LZ2
##############################################    
os.system('aws iam  list-policies | jq \'.Policies | length\' > borrar.json')
output=suppFunct.getOutput('./borrar.json') 
suppFunct.saveValues(resultsFile,suppFunct.addQuotes('awsNumberAvailablePolicies'),output, True)   



##############################################
# Checks the number of accounts in LZ2
##############################################
os.system('aws organizations list-accounts | jq \'.Accounts | length\' > borrar.json')
output=suppFunct.getOutput('./borrar.json')   
suppFunct.saveValues(resultsFile,suppFunct.addQuotes('awsTotalNumberAccounts'),output,True)    

##############################################
# Using the list-organizational-units-for-parent   API
##############################################
# Checks the number of Organizational units in the Landing Zone
# the r-t8h3 was extracted from the GUI. Do not know how to do it from API with the account I am using
##############################################    
os.system('aws organizations list-organizational-units-for-parent --parent-id r-t8h3| jq \'.OrganizationalUnits[] | {Id, Name} \'  > apiResults.json')
os.system('jq -r \'[.[]] | @csv\' apiResults.json > apiResults.txt') #Convert the json file to csv, makes life easier for next iteration
##############################################
# Now, it checks the number of accounts associated to each of the organizational units
##############################################    
myApiResults=open('./apiResults.txt',"r")
numberOrganizationalUnits=0

with open(resultsFile, 'a') as f:
        f.write(suppFunct.addTab(suppFunct.addQuotes('OrganizationsInformation')) +' : {\n')

for line in myApiResults:
    myLine = line.replace('\"',"").replace('\'',"").split(",") #We get the Id and the Name of the organizational Units
    os.system('aws organizations list-accounts-for-parent --parent-id ' + myLine[0] + ' | jq \'.Accounts | length\' > borrar.json')
    output=suppFunct.getOutput('./borrar.json') 
    suppFunct.saveValues(resultsFile,suppFunct.addTab(suppFunct.addQuotes('accountsInOU_'+myLine[1])),output,True)
    numberOrganizationalUnits+=1
    
with open(resultsFile, 'a') as f:
    suppFunct.saveValues(resultsFile,suppFunct.addTab(suppFunct.addQuotes('numberOrganizationUnits')),str(numberOrganizationalUnits),  False)
    f.write('    },\n')







suppFunct.delFile('./apiResults.txt')
suppFunct.delFile('./apiResults.json')

suppFunct.closeResultsFile(resultsFile,awsAccountUsed)


#Perhaps check how many   "AttachedManagedPolicies":  are associated to each role
#conserving the number and the name will be another test of stability
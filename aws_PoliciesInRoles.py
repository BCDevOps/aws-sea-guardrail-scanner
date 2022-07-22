
import os

import suppFunct
import datetime
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
resultsFile="./resultsPoliciesInRoles.json"

suppFunct.checkExistCreate(resultsFile)


############################################################################################
########   Gathering the data section
############################################################################################
os.system('aws iam  get-account-authorization-details | jq \'.RoleDetailList[] | {RoleName, RoleId}\' > apiResults.json')
os.system('jq -r \'[.[]] | @csv\' apiResults.json > apiResults.txt') #Convert the json file to csv, makes life easier for next iteration

os.system('wc -l < ./apiResults.txt >borrar.txt')
myNumRes=open('./borrar.txt',"r") 
numberOfPolicies=myNumRes.read()
numberOfPolicies=int(numberOfPolicies.rstrip('\r\n'))
##############################################
# Lists all managed policies that are attached to the specified IAM role.
##############################################    
myApiResults=open('./apiResults.txt',"r")

policiesCounter=1
for line in myApiResults:
    myLine = line.replace('\"',"").replace('\'',"").split(",") #We get the Id and the Name of the organizational Units
    os.system('aws iam list-attached-role-policies --role-name ' + myLine[0] + ' | jq \'.AttachedPolicies | length\' > borrar.json')
    
    myBorrar=open('./borrar.json',"r") 
    borrar=myBorrar.read()
 
    if len(borrar.rstrip('\r\n'))>0: #I write 3 just in case there is some role with more than ten policies attached to it    
        output=suppFunct.getOutput('./borrar.json') 
        suppFunct.saveValues(resultsFile,suppFunct.addTab(suppFunct.addQuotes('managedPoliciesAttachedToIAMRole_'+myLine[0])),output,True)
    else:
        suppFunct.saveValues(resultsFile,suppFunct.addTab(suppFunct.addQuotes('managedPoliciesAttachedToIAMRole_'+myLine[0])),suppFunct.addQuotes('n/a'),True)

myApiResults.close()


##############################################
# Lists the names of the inline policies that are embedded in the specified IAM role.
##############################################    
myApiResults=open('./apiResults.txt',"r")

policiesCounter=1
for line in myApiResults:
    myLine = line.replace('\"',"").replace('\'',"").split(",") #We get the Id and the Name of the organizational Units
    os.system('aws iam list-role-policies --role-name ' + myLine[0] + ' | jq \'.PolicyNames | length\' > borrar.json')
    
    myBorrar=open('./borrar.json',"r") 
    borrar=myBorrar.read()
 
    if policiesCounter<numberOfPolicies:
        if len(borrar.rstrip('\r\n'))>0: #I write 3 just in case there is some role with more than ten policies attached to it    
            output=suppFunct.getOutput('./borrar.json') 
            suppFunct.saveValues(resultsFile,suppFunct.addTab(suppFunct.addQuotes('inlinePoliciesEmbeddedToIamRole_'+myLine[0])),output,True)
        else:
            suppFunct.saveValues(resultsFile,suppFunct.addTab(suppFunct.addQuotes('inlinePoliciesEmbeddedToIamRole_'+myLine[0])),suppFunct.addQuotes('n/a'),True)
        
    else:        
        if len(borrar.rstrip('\r\n'))>0: #I write 3 just in case there is some role with more than ten policies attached to it    
            output=suppFunct.getOutput('./borrar.json') 
            suppFunct.saveValues(resultsFile,suppFunct.addTab(suppFunct.addQuotes('inlinePoliciesEmbeddedToIamRole_'+myLine[0])),output,False)
        else:    
            suppFunct.saveValues(resultsFile,suppFunct.addTab(suppFunct.addQuotes('inlinePoliciesEmbeddedToIamRole_'+myLine[0])),suppFunct.addQuotes('n/a'),False)
    
    policiesCounter+=1 
    
with open(resultsFile, 'a') as f:
    f.write('    },\n')



suppFunct.delFile('./borrar.json')
suppFunct.delFile('./borrar.txt')

suppFunct.delFile('./apiResults.txt')
suppFunct.delFile('./apiResults.json')

suppFunct.closeResultsFile(resultsFile,awsAccountUsed)


#Perhaps check how many   "AttachedManagedPolicies":  are associated to each role
#conserving the number and the name will be another test of stability
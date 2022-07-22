import os
import datetime
from os.path import exists

##############################################
# Functions
##############################################

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


def getOutput(fileName):
    if os.path.exists(fileName):
        fp = open(fileName, "r")
        output=fp.read()
        fp.close()
        os.remove(fileName)
        return output

def getOutputApi(fileName,node):
    if os.path.exists(fileName):    
        os.system( ' jq \'.' + node + ' | length\' '+ fileName + ' > borrar.json')
        output=getOutput('./borrar.json')
        delFile('./borrar.json')
        return output

    
def closeResultsFile(resultsFile,awsAccountUsed):
    with open(resultsFile, 'a') as f:
        f.write('   \"TestInformation\": ' +' {\n')
        f.write('       \"DateTime\" : "' +str(datetime.datetime.now())+ '",\n')
        f.write('       \"awsAccountUsed\" : "' + awsAccountUsed + '",\n')
        f.write('       \"AWS_DEFAULT_REGION\" : "' + os.environ.get('AWS_DEFAULT_REGION') + '"\n')
        f.write('   }\n')
        f.write('}')

def delFile(fileName):
    if os.path.exists(fileName):
        os.remove(fileName)
        return


def checkExistCreate(fileName): # Checks the existence of the results file, if already exist it will be deleted...
    if os.path.exists(fileName):
        print("Script will remove  the existing file " + fileName)
        os.remove(fileName)

    print("Script will (re)create the file " + fileName)
    with open(fileName, 'w') as f:
        f.write('{\n')
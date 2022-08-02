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
        if len(output)>0:
            return output
        else:
            return "\"n/a\""


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
        
        return

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
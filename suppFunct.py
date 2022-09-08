import os
import datetime
import json
from os.path import exists
import subprocess

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

# To read files that contain a single piece of information
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


def getOutputApi(fileName,node): # returns the length of a given key in a json file
    if os.path.exists(fileName):    
        os.system( ' jq \'.' + node + ' | length\' '+ fileName + ' > borrar.json')
        output=getOutput('./borrar.json')
        delFile('./borrar.json')
        return output



def returnValue(fileName,key): #Returns the value of a given key in a json file
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
        
        
        
def setCredentials(Credentials):
   # print('*******************************')
    
    #print(os.environ)
    
    #print('*******************************') 
    # cmd='export AWS_ACCESS_KEY_ID=' + eval(Credentials[0])
    # os.system(cmd)
    
  # print('1--->'+os.environ.get('AWS_ACCESS_KEY_ID'))
   # print('2--->'+os.getenv('AWS_ACCESS_KEY_ID')) 
    
       
   # os.environ.setdefault('AWS_ACCESS_KEY_ID', str(eval(Credentials[0])))
    os.environ["AWS_ACCESS_KEY_ID"] = str(Credentials[0])
    os.environ["AWS_SECRET_ACCESS_KEY"] = str(Credentials[1])
    os.environ["AWS_SESSION_TOKEN"] = str(Credentials[2])
    caca1=os.environ.get('AWS_ACCESS_KEY_ID')
    caca2=os.getenv('AWS_ACCESS_KEY_ID')
    print('1--->'+caca1) 
    print('2--->'+caca2) 
      #  os.system('export AWS_ACCESS_KEY_ID=' + Credentials[0].replace('\"','').rstrip() + '\'')
      #  os.system('export AWS_SECRET_ACCESS_KEY=' + Credentials[1].strip('\"').strip('\"').rstrip() + '\'')
      #  os.system('export AWS_SESSION_TOKEN=' + Credentials[2].strip('\"').strip('\"').rstrip() + '\'')   
    return
        
 
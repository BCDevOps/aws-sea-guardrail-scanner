import os
#from os.path import isfile, join
#from os import listdir
import re
from this import d
import subprocess
import datetime

import aws_PoliciesInRoles
import suppFunct
from os.path import exists


print("############################################################################################################")
print("This script looks at the files in the ./results folder, then filter them by the Landing Zone (LZ0, LZ1, LZ2) you enter ")
print("then sorts them by date and compare the each version of the Config and Policies files for each license plate")
print("")
print("Notice the format of the files produces by the getFullSnapshor.py is YYYYMMDD_AWSCloudFormationStackSetExecutionRole")
print("   YYYYMMDD_AWSCloudFormationStackSetExecutionRole_<Config/Policies>_<LicensePlate>_<LZ#>.json")
print("For example:")
print("   ßYYYYMMDD_AWSCloudFormationStackSetExecutionRole_<Config/Policies>_<LicensePlate>_<LZ#>.json")
print("and this script expects the files contained in ./results to follow this format")
print("############################################################################################################")
print("It produces a file for each consecutive dates. If there is only one file for the combination of ")
print("Config/Policies, License Plate and Landing Zone, then no comparison file will be produced")
print("############################################################################################################")
print("")


LZ=""
while LZ not in ["0","1","2"]:
    print('Which Landing zone LZ are you using 0/1/2')
    LZ=input()


resultsFiles = [f for f in os.listdir("./results") if os.path.isfile(os.path.join("./results", f))]


r = re.compile(".*_LZ" + LZ + ".json")
jsonFiles = list(filter(r.match, resultsFiles)) # Get all json files in the folder

r = re.compile(".*Config_")
configFiles = list(filter(r.match, jsonFiles)) # Get all json files in the folder

r = re.compile(".*Policies_")
policyFiles = list(filter(r.match, jsonFiles)) # Get all json files in the folder


while len(configFiles)>2:
    licensePlate=configFiles[0].split("_")[3]
    print("----->"+ licensePlate)
    r = re.compile(".*_"+ licensePlate +"_")
    workingFiles = list(filter(r.match, configFiles)) # Get all config files with the same license plate and sort them
    workingFiles.sort() #List of Config files with same license plate ordered by date
    
    x=0
    
    for x in range (len(workingFiles)-1):
        print("Compare " + str(workingFiles[x]) + " with "+ str(workingFiles[x+1]))
        olderSnapshotConfigName=str(workingFiles[x]) 
        newerSnapshotConfigName=str(workingFiles[x+1])
        #The Policies files have the same name patters as the Config files
        olderSnapshotPoliciesName=str(workingFiles[x]).replace("Config","Policies") 
        newerSnapshotPoliciesName=str(workingFiles[x+1]).replace("Config","Policies") 

        suppFunct.compareFile(olderSnapshotConfigName,newerSnapshotConfigName,olderSnapshotPoliciesName,newerSnapshotPoliciesName)
        
        configFiles.remove(workingFiles[x])
        x=x+1
        
    configFiles.remove(workingFiles[x])
    

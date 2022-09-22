# aws-sea-guardrail-scanner

The repo contains a set of scripts that allow:
- Run a single guardrails scan
- Run multiple guardrails scans
- Compare json files to detect the differences creating a html report

Running the script before and after an upgrade, and then running the comparison between these two scans will produce a report with the changes in the main parameters, roles and policies if any. The report needs to be checked manually to determine if changes are expected or not.


# Preconditions

You need to have on your machine
- AWS CLI (https://aws.amazon.com/cli/)
- jq (brew install jq)
- python 3 or higher (brew install python)
- The AWS credentials for the specific account you are going to check. Export them so they are part of the environment variables on your terminal 

        export AWS_ACCESS_KEY_ID="A..."
        export AWS_SECRET_ACCESS_KEY="N...="
        export AWS_DEFAULT_REGION=ca-central-1



# Creating a single Guardrails snapshot

On the command line, run

    getSnapshot.py

The script will ask you for the name of the account defined by the License Plate and the role (actually, the KeyCloak role equivalent to a bundle of AWS roles) you are checking. The AWS credentials must be associated to this account. By default it will use 
    *BCGOV_MASTER_admin_tmhl5tvs*


Please, keep the format of the account name as **BCGOV_Type_Role_LicensePlate**, this allows to better classify and keep track of the records.
- Values for **Type** are: *CORE*, *WORKLOAD*, *MASTER*
- Values for **Role** are : *Admin*, *billing*, *developer*, *readonly*, *security*

Then it will ask you for the LicensePlate, by default will use **tmhl5tvs-dev**


After the name, it will ask you to enter 0, 1 or 2, corresponding to the Landing Zone where the account name is deployed.

There is no linkage between the AWS credential, the account name and the Landing Zone number. If you mix these values you will get a snapshot of an account that you will not be able to later recognize .

The program will run a series of API calls. Depending of the account used, its configuration and the state of the network it may take up to 10' to complete all the requests and finish process.

The script will generate four files. 
- YYYYMMDD_<Type><Role>ConfigLZ#.json
- YYYYMMDD_<Type><Role>ConfigLZ#.html
- YYYYMMDD_<Type><Role>PoliciesLZ#.json
- YYYYMMDD_<Type><Role>PoliciesLZ#.html

Where *YYYYMMDD* is the date the script has been ran and *#* is the Landing Zone number.

Config refers to the snapshot containing general values and settings for the account, for example the number of S3 buckets. Policies refers to the snapshot that describes the policies associated to the different roles. The reason to separate these two files is that combining them may result in a file with too much data to understand at a glance.

The json and html versions of the file contain the same information, with the html being more human readable.

All files are stored in the *./results* folder 


# Comparing snapshots

To compare two snapshots you run the

    compareGuardrails.py

script. It assumes you are comparing snapshots associated to the same account and the same Landing Zone, otherwise the script will stop

When you start the script it ask if the files are stored in a folder other than ./results and/or the file names do not follow the standard form described above.
Enter **y** if you want to enter non-standard location/names for the files. It will ask first the name of the older file to compare with the newer one.

If you enter a key other than **y** it will ask you the following questions:
- Account name, but default will use *BCGOV_MASTER_admin_tmhl5tvs*
- Number of the Landing Zone
- Date in which the older snapshot was taken in *YYYMMDD* format
- Date in which the newer snapshot was taken in *YYYMMDD* format

The script will parse the account name and try to find the corresponding json files in the *./results* directory. If it fails I will display a message and the program will end.

Currently the comparison file is saved in the same folder where the script is running with the format ***yyyymmdd_YYYMMDD_TypeRoleLZ#.html***

where *yyyymmdd* is the date for the older snapshot, *YYYYMMDD* is the date for the newer snapshot, *Type* and *Role* are the values extracted from the account name, and *#* is the Landing Zone number.


# Creating a multiple Guardrails snapshots
In this case, you need to have in the same folder where you run the script the file **accountsToScan.json**. The first level nodes refers to the landing zone, and the other. Inside the LZ# node you have a second level with the Master account for the node, and then another node for all the secondary accounts you want to scan. A third level indicates the roles the Master account will assume as secondary account.

Currently, we only scan the role **AWSCloudFormationStackSetExecutionRole** as it is the only role that has a trust relationship with the master account.

As in the case of a single scan, it will save all the files in the ./results folder and the pattern will be 

- YYYYMMDD_AWSCloudFormationStackSetExecutionRoleConfigLZ#.json
- YYYYMMDD_AWSCloudFormationStackSetExecutionRoleConfigLZ#.html
- YYYYMMDD_AWSCloudFormationStackSetExecutionRolePoliciesLZ#.json
- YYYYMMDD_AWSCloudFormationStackSetExecutionRolePoliciesLZ#.html


There are four files produce for every single aws role associated to and account in the  **accountsToScan.json** file, including snapshots for the master account.

To run, fulfill the prerequisites plus have prepared the **accountsToScan.json** file in the same folder as the script. You can find the template for this file in this readme or in the Sharepoint/Teams CPF site (https://bcgov.sharepoint.com/:u:/t/01368-CPFScrumTeam/EV0O0Ne_ExRIocJXHb9Dq6oBdOs7RJQpH8H21t8nkLkZfA?e=wsOWiZ).

On the command line, enter the AWS credentials for the Landing Zone master account and then run

    getFullSnapshot.py



# Comparing multiple Guardrails snapshots
The files produced at different times by getFullSnapshot.py are stored in the ./results folder (with root being the folder where you will run the script to compare the snapshots)

Run the script

    compareAllGuardrails.py

The script will request the number of the Landing Zone that holds the accounts you want to compare. Then it will read the list of files in ,/results, group them by License Plate and sort them by date. It will compare and produce a file for consecutive dates

The produced files will only list the differences. However, due the structure of the original JSON file, it will also generate lines indicated there are no changes (instead of writing nothing)


# accountsToScan.json Template


{
    "LZ1": {
        "Master":{
            "accountNumber" : "111111111111", 
            "licensePlate" : "Master Account for the zone",
            "role" : "XXXXXX_MASTER_admin_12345678"
        },
        "Accounts": {
             "222222222222": {
                "licensePlate":"123456-tools",
                "roles":[
                    "AWSRoleWithTrustRelationshipWithMaster_1"
                ]
            },    
            "333333333333":{
                "licensePlate":"123456-dev",
                "roles":[
                    "AWSRoleWithTrustRelationshipWithMaster_1",
                    "AWSRoleWithTrustRelationshipWithMaster_3"
                ]
            },
            "444444444444": {
                "licensePlate":"234567-dev",
                "roles":[
                    "AWSRoleWithTrustRelationshipWithMaster_1"
                ]
            },  
            "555555555555": {
                "licensePlate":"234567-sandbox",
                "roles":[
                    "AWSRoleWithTrustRelationshipWithMaster_1",
                    "AWSRoleWithTrustRelationshipWithMaster_2"
                ]
            }
        }
    }
}

# aws-sea-guardrail-scanner

The repo contains a set of scripts that allow:
- Run a single guardrails scan
- Run multiple guardrails scans
- Compare json files to detect the differences creating a html report

Running the script before and after an upgrade, and then running the comparison between these two scans will produce a report with the changes in the main parameters, roles and policies if any. The report needs to be checked manually to determine if changes are expected or not.


# Preconditions

You need to have on your machine
- AWS CLI (https://aws.amazon.com/cli/)
- jq (brew install jq)
- python 3 or higher (brew install python)
- The AWS credentials for the specific account you are going to check. Export them so they are part of the environment variables on your terminal 

        export AWS_ACCESS_KEY_ID="A..."
        export AWS_SECRET_ACCESS_KEY="N...="
        export AWS_DEFAULT_REGION=ca-central-1



# Creating a single Guardrails snapshot

On the command line, run

    getSnapshot.py

The script will ask you for the name of the account defined by the License Plate and the role (actually, the KeyCloak role equivalent to a bundle of AWS roles) you are checking. The AWS credentials must be associated to this account. By default it will use 
    *BCGOV_MASTER_admin_tmhl5tvs*


Please, keep the format of the account name as **BCGOV_Type_Role_LicensePlate**, this allows to better classify and keep track of the records.
- Values for **Type** are: *CORE*, *WORKLOAD*, *MASTER*
- Values for **Role** are : *Admin*, *billing*, *developer*, *readonly*, *security*

Then it will ask you for the LicensePlate, by default will use **tmhl5tvs-dev**


After the name, it will ask you to enter 0, 1 or 2, corresponding to the Landing Zone where the account name is deployed.

There is no linkage between the AWS credential, the account name and the Landing Zone number. If you mix these values you will get a snapshot of an account that you will not be able to later recognize .

The program will run a series of API calls. Depending of the account used, its configuration and the state of the network it may take up to 10' to complete all the requests and finish process.

The script will generate four files. 
- YYYYMMDD_<Type><Role>ConfigLZ#.json
- YYYYMMDD_<Type><Role>ConfigLZ#.html
- YYYYMMDD_<Type><Role>PoliciesLZ#.json
- YYYYMMDD_<Type><Role>PoliciesLZ#.html

Where *YYYYMMDD* is the date the script has been ran and *#* is the Landing Zone number.

Config refers to the snapshot containing general values and settings for the account, for example the number of S3 buckets. Policies refers to the snapshot that describes the policies associated to the different roles. The reason to separate these two files is that combining them may result in a file with too much data to understand at a glance.

The json and html versions of the file contain the same information, with the html being more human readable.

All files are stored in the *./results* folder 


# Comparing snapshots

To compare two snapshots you run the

    compareGuardrails.py

script. It assumes you are comparing snapshots associated to the same account and the same Landing Zone, otherwise the script will stop

When you start the script it ask if the files are stored in a folder other than ./results and/or the file names do not follow the standard form described above.
Enter **y** if you want to enter non-standard location/names for the files. It will ask first the name of the older file to compare with the newer one.

If you enter a key other than **y** it will ask you the following questions:
- Account name, but default will use *BCGOV_MASTER_admin_tmhl5tvs*
- Number of the Landing Zone
- Date in which the older snapshot was taken in *YYYMMDD* format
- Date in which the newer snapshot was taken in *YYYMMDD* format

The script will parse the account name and try to find the corresponding json files in the *./results* directory. If it fails I will display a message and the program will end.

Currently the comparison file is saved in the same folder where the script is running with the format ***yyyymmdd_YYYMMDD_TypeRoleLZ#.html***

where *yyyymmdd* is the date for the older snapshot, *YYYYMMDD* is the date for the newer snapshot, *Type* and *Role* are the values extracted from the account name, and *#* is the Landing Zone number.


# Creating a multiple Guardrails snapshots
In this case, you need to have in the same folder where you run the script the file **accountsToScan.json**. The first level nodes refers to the landing zone, and the other. Inside the LZ# node you have a second level with the Master account for the node, and then another node for all the secondary accounts you want to scan. A third level indicates the roles the Master account will assume as secondary account.

Currently, we only scan the role **AWSCloudFormationStackSetExecutionRole** as it is the only role that has a trust relationship with the master account.

As in the case of a single scan, it will save all the files in the ./results folder and the pattern will be 

- YYYYMMDD_AWSCloudFormationStackSetExecutionRoleConfigLZ#.json
- YYYYMMDD_AWSCloudFormationStackSetExecutionRoleConfigLZ#.html
- YYYYMMDD_AWSCloudFormationStackSetExecutionRolePoliciesLZ#.json
- YYYYMMDD_AWSCloudFormationStackSetExecutionRolePoliciesLZ#.html


There are four files produce for every single aws role associated to and account in the  **accountsToScan.json** file, including snapshots for the master account.

To run, fulfill the prerequisites plus have prepared the **accountsToScan.json** file in the same folder as the script. You can find the template for this file in this readme or in the Sharepoint/Teams CPF site (https://bcgov.sharepoint.com/:u:/t/01368-CPFScrumTeam/EV0O0Ne_ExRIocJXHb9Dq6oBdOs7RJQpH8H21t8nkLkZfA?e=wsOWiZ).

On the command line, enter the AWS credentials for the Landing Zone master account and then run

    getFullSnapshot.py



# Comparing multiple Guardrails snapshots
The files produced at different times by getFullSnapshot.py are stored in the ./results folder (with root being the folder where you will run the script to compare the snapshots)

Run the script

    compareAllGuardrails.py

The script will request the number of the Landing Zone that holds the accounts you want to compare. Then it will read the list of files in ,/results, group them by License Plate and sort them by date. It will compare and produce a file for consecutive dates

The produced files will only list the differences. However, due the structure of the original JSON file, it will also generate lines indicated there are no changes (instead of writing nothing)


# accountsToScan.json Template


{
    "LZ1": {
        "Master":{
            "accountNumber" : "111111111111", 
            "licensePlate" : "Master Account for the zone",
            "role" : "XXXXXX_MASTER_admin_12345678"
        },
        "Accounts": {
             "222222222222": {
                "licensePlate":"123456-tools",
                "roles":[
                    "AWSRoleWithTrustRelationshipWithMaster_1"
                ]
            },    
            "333333333333":{
                "licensePlate":"123456-dev",
                "roles":[
                    "AWSRoleWithTrustRelationshipWithMaster_1",
                    "AWSRoleWithTrustRelationshipWithMaster_3"
                ]
            },
            "444444444444": {
                "licensePlate":"234567-dev",
                "roles":[
                    "AWSRoleWithTrustRelationshipWithMaster_1"
                ]
            },  
            "555555555555": {
                "licensePlate":"234567-sandbox",
                "roles":[
                    "AWSRoleWithTrustRelationshipWithMaster_1",
                    "AWSRoleWithTrustRelationshipWithMaster_2"
                ]
            }
        }
    }
}


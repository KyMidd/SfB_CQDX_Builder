# version3, loop through site codes and subnets and creates report files
#  Author: Kyler Middleton, Touchbase

# Imports
import csv,os,shutil,fileinput

# Open CSV that contains site codes and subnets
with open('SubnetsList.csv', 'rt') as f:
    csvReturn = ['Sites', 'Subnet1', 'etc']
    for row in f:
        for x in range(0, str(row).count(',')):
            row = str.replace(str(row), ',,', ',')
        rowList = row.split(",")
        csvReturn.append(rowList)
## Remove "\n" from last entry of each imported string
for x in range(3, (len(csvReturn) - 3)):
    del(csvReturn[x][-1])
    #print(csvReturn[x])

# Template Variables - replace these values (caps sensitive) in template doc
#  This will allow script to replace them iteratively with site-specific values.
## SITE = site code should be inserted
## SUBNETS1 = Subnets divided by " | ", e.g.: 10-5-17-0 | 10-101-16-0
## SUBNETS2 = Subnets in "[]", divided by ",", e.g.: [10-5-17-0],[10-101-16-0]
## Template filename = SfB_CQM_ReportSite_Template.cqdx

## Build variables for report
for x in range(3, (len(csvReturn))):
    #print(csvReturn[x])
    
    # Set regioncode on each loop
    regionCode = csvReturn[x][0]
    #print(regionCode)

    # Get all subnets as a variable
    del csvReturn[x][0]

    # subnets1 - transform to correctly format string
    SUBNETS1 = str(csvReturn[x])
    SUBNETS1 = str(SUBNETS1).strip('[]')
    SUBNETS1 = str.replace(str(SUBNETS1), ',', ' |')
    SUBNETS1 = str.replace(str(SUBNETS1), '\'', '')
    SUBNETS1 = str.replace(str(SUBNETS1), '.', '-')
    #print(SUBNETS1)

    # subnets2 - transform to correctly format string
    SUBNETS2 = str(csvReturn[x])
    SUBNETS2 = str(SUBNETS2).strip('[]')
    SUBNETS2 = str.replace(str(SUBNETS2), '\', \'', '] [')
    SUBNETS2 = str.replace(str(SUBNETS2), '\'1', '[1')
    SUBNETS2 = str.replace(str(SUBNETS2), '\'', ']')
    SUBNETS2 = str.replace(str(SUBNETS2), '.', '-')
    #print(SUBNETS2)

    # Path for new reports
    path = "SfB_CQM_ReportSiteFolder/"

    # Template file (modified with variables for find/replace
    sourceFile = "SfB_CQM_ReportSite_Template.cqdx"
    
    # Target file iterative
    targetFile = "generatedReports/" + "SfB_CQM_ReportSite_" + str(regionCode) + ".cqdx"
    #print(targetFile)

    # Read template, modify in-memory buffer with site-specific info, write out file with new name
    fileInput = open(sourceFile)
    fileOutput = open(targetFile, "wt")
    for line in fileInput:
        buffer = line
        buffer = buffer.replace('REGION', regionCode)
        buffer = buffer.replace('SUBNETS1', SUBNETS1)
        buffer = buffer.replace('SUBNETS2', SUBNETS2)
        buffer = buffer.replace(' | \n', '')
        buffer = buffer.replace(' [\\n]', '')
        buffer = buffer.replace('\\n\\', '\\')
        buffer = buffer.replace('\\n]', ']')
        fileOutput.write(buffer)
    fileInput.close()
    fileOutput.close()

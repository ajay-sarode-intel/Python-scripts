from itertools import izip_longest
import csv

# This part of code open and reads the two input csv files

t1 = open('/nfs/sc/disks/sc_rtl_users_0002/asarode/script_automation/old_file.csv', 'r')
t2 = open('/nfs/sc/disks/sc_rtl_users_0002/asarode/script_automation/new_file.csv', 'r')

with open('/nfs/sc/disks/sc_rtl_users_0002/asarode/script_automation/old_file.csv', 'r') as t1, open('/nfs/sc/disks/sc_rtl_users_0002/asarode/script_automation/new_file.csv', 'r') as t2:
    fileone = t1.readlines()
    filetwo = t2.readlines()

# This part of code copies old violations with comments and keep violation as it is if previous comment was not present     

with open('update.csv', 'w') as outFile:
    outFile.write('*** Old violations that has not resolved ***\n')
    for line in filetwo:
        array2 = line.split(',')
        for line in fileone:
            array1 = line.split(',')
            if array2[0] == array1[0] :
                outFile.write(",".join(array1)) 

# This part of code writes only new violations which are not present in old file    

with open('update.csv', 'a') as outFile:
    outFile.write('*** New Violations ***\n')
    for line in filetwo:
        array2 = line.split(',')
        s=0   # s is initialized as zero
        for line in fileone:
            array1 = line.split(',')
            if array2[0] == array1[0] :
                s = s+1 # s incrments only if violation from two files matches
        if s==0 :
            outFile.write(",".join(array2))

# This part of code writes violations which are resolved and not present in old file 

with open('update.csv', 'a') as outFile:
    outFile.write('*** Old violations that has resolved ***\n')
    for line in fileone:
        array1 = line.split(',')
        p=0   # p is initialized as zero
        for line in filetwo:
            array2 = line.split(',')
            if array1[0] == array2[0] :
                p = p+1 # p incrments only if violation from two files matches
        if p==0 :
            outFile.write(",".join(array1))

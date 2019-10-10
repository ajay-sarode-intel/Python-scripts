from itertools import izip_longest
import csv

t1 = open('/nfs/sc/disks/sc_rtl_users_0002/asarode/script_automation/old_file.csv', 'r')
t2 = open('/nfs/sc/disks/sc_rtl_users_0002/asarode/script_automation/new_file.csv', 'r')

with open('/nfs/sc/disks/sc_rtl_users_0002/asarode/script_automation/old_file.csv', 'r') as t1, open('/nfs/sc/disks/sc_rtl_users_0002/asarode/script_automation/new_file.csv', 'r') as t2:
    fileone = t1.readlines()
    filetwo = t2.readlines()

# This part of code copies old comments and keep old violations     

with open('update.csv', 'w') as outFile:
    for line in filetwo:
        array2 = line.split(',')
        #print(array2)
        #print array2[0] is violation
        #print array2[1] is comment
        for line in fileone:
            array1 = line.split(',')
            #print(arra12)
            #print array1[0] is violation
            #print array1[1] is comment
            data = [array1[0], array1[1]]

            if array2[0] == array1[0] :
                outFile.write(",".join(data))                

# This part of code writes only new violations which are absent in old file    

with open('update.csv', 'a') as outFile:
    for line in filetwo:
        array2 = line.split(',')
        #print array2[0] is violation
        #print array2[1] is comment
        s=0   # s is initialized as zero
        for line in fileone:
            array1 = line.split(',')
            #print(arra12)
            #print array1[0] is violation
            #print array1[1] is comment

            if array2[0] == array1[0] :
                s = s+1 # s incrments only if violation from two files matches
        if s==0 :
            outFile.write(",".join(array2))

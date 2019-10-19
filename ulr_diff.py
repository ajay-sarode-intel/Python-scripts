from itertools import izip_longest
import csv
import argparse   # Module for arguments parsing

## Script Owner : Ajay Sarode

# Argument Parser

parser = argparse.ArgumentParser(description='Script for unloaded registers report')
parser.add_argument('-input_ref', type=str, help='Old/Reference file path')
parser.add_argument('-input_new', type=str, help='new file path')
parser.add_argument('-output', type=str, help='output file path')
parser.add_argument('--Help', help='Script for finding diff between two reports of unloaded registers. Script is format dependent, script will not work if format is changed')
args = parser.parse_args()
old_file_name = args.input_ref  # Old file location with file name ex. /path/old.xls
new_file_name = args.input_new  # New file location with file name
output_file_name = args.output  # Output file location with file name

# This part of code open and reads the two input csv files

t1 = open(old_file_name, 'r')
t2 = open(new_file_name, 'r')

with open(old_file_name, 'r') as t1, open(new_file_name, 'r') as t2:
    fileone = t1.readlines()
    filetwo = t2.readlines()

# This part of code copies old violations with comments and keep violation as it is if previous comment was not present 

with open(output_file_name, 'w') as outFile:
    outFile.write('*** Propagated Violations ***\n')
    for line in filetwo:
        array2 = line.split(',')
        for line in fileone:
            array1 = line.split(',')
            if array2[0] == array1[0] :
                outFile.write(",".join(array1)) 

# This part of code writes only new violations which are not present in old file    

with open(output_file_name, 'a') as outFile:
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

with open(output_file_name, 'a') as outFile:
    outFile.write('*** Fixed Violations ***\n')
    for line in fileone:
        array1 = line.split(',')
        p=0   # p is initialized as zero
        for line in filetwo:
            array2 = line.split(',')
            if array1[0] == array2[0] :
                p = p+1 # p incrments only if violation from two files matches
        if p==0 :
            outFile.write(",".join(array1))


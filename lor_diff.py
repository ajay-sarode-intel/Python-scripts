#!/usr/intel/pkgs/python3/3.6.3a/bin/python3
## Script Owner : Ajay Sarode

import sys
sys.path.append('/usr/intel/pkgs/python3/3.6.3/modules/r1/lib/python3.6/site-packages/')

import xlrd       # Module for Reading an excel file 
import xlsxwriter # Module for Writing an excel file 
import argparse   # Module for arguments parsing

# Argument Parser

parser = argparse.ArgumentParser(description='Script for Logic on Reset report')
parser.add_argument('-input_ref', type=str, help='Old/Reference file path')
parser.add_argument('-input_new', type=str, help='new file path')
parser.add_argument('-output', type=str, help='output file path')
parser.add_argument('--Help', help='Script for finding diff between two reports of logic on reset. Script is format dependent, script will not work if format is changed')
args = parser.parse_args()
old_file_name = args.input_ref
new_file_name = args.input_new
output_file_name = args.output
  
# Opening old file and its logic on reset sheet for reading 
old_file = xlrd.open_workbook(old_file_name) 
lor_sheet_old_file = old_file.sheet_by_name('LogicOnResetPathByComb') 

# Opening new file and its logic on reset sheet for reading 
new_file = xlrd.open_workbook(new_file_name) 
lor_sheet_new_file = new_file.sheet_by_name('LogicOnResetPathByComb') 

# Creating a new file of given name to store the bucket splitted (diff) version
update_file = xlsxwriter.Workbook(output_file_name)
lor_sheet_diff = update_file.add_worksheet('LogicOnResetPathByComb')

# Add a bold format to use to highlight cells.
bold = update_file.add_format({'bold': 1})

# Number of rows in sheets old and new files
no_rows_old_sheet = lor_sheet_old_file.nrows
no_rows_new_sheet = lor_sheet_new_file.nrows

# Number of columns in old and new files
no_columns_old_sheet = lor_sheet_old_file.ncols
no_columns_new_sheet = lor_sheet_new_file.ncols

row_of_diff_file = 4  # initializing row number of a diff file with 0

# Initializing the New xls with writing its column names

cell_format = update_file.add_format({'bold': True, 'bg_color': '#33CCCC'})
cell_format2 = update_file.add_format({'bold': True, 'font_color': 'red'})

for col_no in range(no_columns_old_sheet):
    lor_sheet_diff.write(row_of_diff_file, col_no, str(lor_sheet_old_file.col_values(col_no)[4]),cell_format)
row_of_diff_file = row_of_diff_file + 1

# Adding comment line for first section
lor_sheet_diff.write(row_of_diff_file, 2, '*** Propagated Violations ***',cell_format2)
row_of_diff_file = row_of_diff_file + 1

col_no_list = [1,2,3,5,6]

# First section algorithm 
for l1 in range(5,no_rows_new_sheet):
    
    temp_row_new_list = []
    for m in col_no_list: # making a temporary list of a particular row from new file   
        temp_row_new_list.append(str(lor_sheet_new_file.col_values(m)[l1]))

    for l2 in range(5,no_rows_old_sheet):
        temp_row_old_list = []
        for n in col_no_list: # making a temporary list of a particular row from old file 
            temp_row_old_list.append(str(lor_sheet_old_file.col_values(n)[l2]))        

        if(temp_row_new_list==temp_row_old_list): 
            
            for col_no in range(1,no_columns_old_sheet):
                lor_sheet_diff.write(row_of_diff_file, col_no, str(lor_sheet_old_file.col_values(col_no)[l2]))
            lor_sheet_diff.write(row_of_diff_file, 4, str(lor_sheet_new_file.col_values(4)[l1]))
            lor_sheet_diff.write(row_of_diff_file, 5, int(lor_sheet_old_file.col_values(5)[l2])) # reading column as integer
            lor_sheet_diff.write(row_of_diff_file, 6, int(lor_sheet_old_file.col_values(6)[l2])) # reading column as integer
            row_of_diff_file = row_of_diff_file + 1

# Adding comment line for second section
lor_sheet_diff.write(row_of_diff_file,2, '*** New Violations ***',cell_format2)
row_of_diff_file = row_of_diff_file + 1

# Second section algorithm
for l1 in range(5,no_rows_new_sheet):
    
    temp_row_new_list = []

    for m in col_no_list: # making a temporary list of a particular row from new file   
        temp_row_new_list.append(str(lor_sheet_new_file.col_values(m)[l1]))
    x=0
    for l2 in range(5,no_rows_old_sheet):
        
        temp_row_old_list = []
        for n in col_no_list: # making a temporary list of a particular row from old file 
            temp_row_old_list.append(str(lor_sheet_old_file.col_values(n)[l2]))
        
        if(temp_row_new_list==temp_row_old_list): 
            x = 1
    if(x==0):
        for col_no in range(1,no_columns_new_sheet):
            lor_sheet_diff.write(row_of_diff_file, col_no, str(lor_sheet_new_file.col_values(col_no)[l1]))
        lor_sheet_diff.write(row_of_diff_file, 5, int(lor_sheet_new_file.col_values(5)[l1])) # reading column as integer
        lor_sheet_diff.write(row_of_diff_file, 6, int(lor_sheet_new_file.col_values(6)[l1])) # reading column as integer
        row_of_diff_file = row_of_diff_file + 1

# Adding comment line for third section
lor_sheet_diff.write(row_of_diff_file,2, '*** Fixed Violations ***',cell_format2)
row_of_diff_file = row_of_diff_file + 1

# Third section algorithm
for l1 in range(5,no_rows_old_sheet):
    
    temp_row_old_list = []
    for m in col_no_list: # making a temporary list of a particular row from old file   
        temp_row_old_list.append(str(lor_sheet_old_file.col_values(m)[l1]))
    x=0
    for l2 in range(5,no_rows_new_sheet):
        temp_row_new_list = []
        for n in col_no_list: # making a temporary list of a particular row from new file 
            temp_row_new_list.append(str(lor_sheet_new_file.col_values(n)[l2]))
        
        if(temp_row_old_list==temp_row_new_list): 
            x = 1
    if(x==0):
        for col_no in range(1,no_columns_old_sheet):
            lor_sheet_diff.write(row_of_diff_file, col_no, str(lor_sheet_old_file.col_values(col_no)[l1]))
        lor_sheet_diff.write(row_of_diff_file, 5, int(lor_sheet_old_file.col_values(5)[l1])) # reading column as integer
        lor_sheet_diff.write(row_of_diff_file, 6, int(lor_sheet_old_file.col_values(6)[l1])) # reading column as integer
        row_of_diff_file = row_of_diff_file + 1

# Closing the file
update_file.close()



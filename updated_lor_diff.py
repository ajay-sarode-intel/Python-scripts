#!/usr/intel/pkgs/python3/3.6.3a/bin/python3
## Script Owner : Ajay Sarode

import sys
sys.path.append('/usr/intel/pkgs/python3/3.6.3/modules/r1/lib/python3.6/site-packages/')

import xlrd       # Module for Reading an excel file 
import xlsxwriter # Module for Writing an excel file 
import argparse   # Module for arguments parsing

#### Arguments Parser ####
parser = argparse.ArgumentParser(description='Script for Logic on Reset report')
parser.add_argument('-input_ref', type=str, help='Old/Reference file path')
parser.add_argument('-input_new', type=str, help='New file path')
parser.add_argument('-output', type=str, help='Diffd/Output file path')
parser.add_argument('--Help', help='Script for finding diff between two reports of logic on reset. Script is format dependent, script will not work if format is changed')
args = parser.parse_args()
old_file_name = args.input_ref
new_file_name = args.input_new
output_file_name = args.output

# Opening old file, opening specific sheet if exists otherwise terminate the program with error message
old_file = xlrd.open_workbook(old_file_name) 
#sheet_names_old_file = old_file.sheet_names()
#if 'LogicOnResetPathByComb' not in sheet_names_old_file: # Or if 'LogicOnResetPathByComb' not in str(sheet_names_old_file) : 
#  sys.exit('LogicOnResetPathByComb Sheet in Reference/Old file does not exists')
sheet_old_file = old_file.sheet_by_name('LogicOnResetPathByComb') 

# Opening new file, opening specific sheet if exists otherwise terminate the program with error message 
new_file = xlrd.open_workbook(new_file_name) 
#sheet_names_new_file = new_file.sheet_names()
#if 'LogicOnResetPathByComb' not in sheet_names_new_file: # Or if 'LogicOnResetPathByComb' not in str(sheet_names_new_file) : 
#  sys.exit('LogicOnResetPathByComb Sheet in New file does not exists')
sheet_new_file = new_file.sheet_by_name('LogicOnResetPathByComb') 

# Creating a new file of given name to store the bucket splitted (diff) version
update_file = xlsxwriter.Workbook(output_file_name)
sheet_diff = update_file.add_worksheet('LogicOnResetPathByComb')

# Various formats to highlight/bold/color cells.
bold = update_file.add_format({'bold': 1})
bold_bg_color = update_file.add_format({'bold': True, 'bg_color': '#33CCCC'})
bold_font_color = update_file.add_format({'bold': True, 'font_color': 'red'})

# Number of rows in sheets old and new files
no_rows_old_sheet = sheet_old_file.nrows
no_rows_new_sheet = sheet_new_file.nrows

# Number of columns in old and new files
no_columns_old_sheet = sheet_old_file.ncols
no_columns_new_sheet = sheet_new_file.ncols

row_of_diff_file = 4  # initializing row number of a diff file sheet with 4th column (starting from 0)

# Initializing the New xls with writing its column names same as of old file and adding Result column
for col_no in range(no_columns_old_sheet):
    sheet_diff.write(row_of_diff_file, col_no, str(sheet_old_file.col_values(col_no)[4]),bold_bg_color)
sheet_diff.write(row_of_diff_file, 0, 'Result',bold_bg_color)
row_of_diff_file = row_of_diff_file + 1

##################### Subroutine for conversion of Whole row to Comparable String #######################
col_no_list = [1,2,3,5,6]  # Columns to be Compared
def row_2_list (row_no,sheet_name)
    temp_list = [] 
    for s in col_no_list: # making a temporary list of a particular row from new file   
        temp_list.append(str(sheet_name.col_values(s)[l1]))
    
    return temp_list
#########################################################################################################

#### First section algorithm for Same as Before

for l1 in range(5,no_rows_new_sheet):
    
    temp_row_new_list = []  # making a temporary list of a particular row from new file
    temp_row_new_list = row_2_list(l1,sheet_new_file)
    
    for l2 in range(5,no_rows_old_sheet):
    
        temp_row_old_list = [] # making a temporary list of a particular row from old file  
        temp_row_old_list = row_2_list(l2,sheet_old_file)        

        if(temp_row_new_list==temp_row_old_list): 
            
            for col_no in range(1,no_columns_old_sheet):
                sheet_diff.write(row_of_diff_file, col_no, str(sheet_old_file.col_values(col_no)[l2]))
            sheet_diff.write(row_of_diff_file, 4, str(sheet_new_file.col_values(4)[l1])) # ref_name Copying from sheet of new file
            sheet_diff.write(row_of_diff_file, 0, 'Same as Before') # Writing its category in 0th column
            sheet_diff.write(row_of_diff_file, 5, int(sheet_old_file.col_values(5)[l2])) # reading column as integer
            sheet_diff.write(row_of_diff_file, 6, int(sheet_old_file.col_values(6)[l2])) # reading column as integer 
            
            row_of_diff_file = row_of_diff_file + 1

#### Second section algorithm for New Violations

for l1 in range(5,no_rows_new_sheet):
    
    temp_row_new_list = []  # making a temporary list of a particular row from new file
    temp_row_new_list = row_2_list(l1,sheet_new_file)
    x=0
    
    for l2 in range(5,no_rows_old_sheet):
        
        temp_row_old_list = [] # making a temporary list of a particular row from old file  
        temp_row_old_list = row_2_list(l2,sheet_old_file) 
        
        if(temp_row_new_list==temp_row_old_list): 
            x = 1
            
    if(x==0):
        for col_no in range(1,no_columns_new_sheet):
            sheet_diff.write(row_of_diff_file, col_no, str(sheet_new_file.col_values(col_no)[l1]))
        sheet_diff.write(row_of_diff_file, 0, 'New Violation') # Writing its category in 0th column
        sheet_diff.write(row_of_diff_file, 5, int(sheet_new_file.col_values(5)[l1])) # reading column as integer
        sheet_diff.write(row_of_diff_file, 6, int(sheet_new_file.col_values(6)[l1])) # reading column as integer
        row_of_diff_file = row_of_diff_file + 1

#### Third section algorithm for Removed Violations

for l1 in range(5,no_rows_old_sheet):
    
    temp_row_old_list = [] # making a temporary list of a particular row from old file
    temp_row_old_list = row_2_list(l1,sheet_old_file)
    x=0
    
    for l2 in range(5,no_rows_new_sheet):
    
        temp_row_new_list = [] # making a temporary list of a particular row from new file
        temp_row_new_list = row_2_list(l2,sheet_new_file)

        if(temp_row_old_list==temp_row_new_list): 
            x = 1
            
    if(x==0):
        for col_no in range(1,no_columns_old_sheet):
            sheet_diff.write(row_of_diff_file, col_no, str(sheet_old_file.col_values(col_no)[l1]))
        sheet_diff.write(row_of_diff_file, 5, int(sheet_old_file.col_values(5)[l1])) # reading column as integer
        sheet_diff.write(row_of_diff_file, 6, int(sheet_old_file.col_values(6)[l1])) # reading column as integer
        row_of_diff_file = row_of_diff_file + 1

# Closing the file
update_file.close()

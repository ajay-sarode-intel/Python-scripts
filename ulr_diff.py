#!/usr/intel/pkgs/python3/3.6.3a/bin/python3
## Script Owner : Ajay Sarode

import sys
sys.path.append('/usr/intel/pkgs/python3/3.6.3/modules/r1/lib/python3.6/site-packages/')

import xlrd       # Module for Reading an excel file 
import xlsxwriter # Module for Writing an excel file 
import argparse   # Module for arguments parsing

#### Arguments Parser ####
parser = argparse.ArgumentParser(description='Script for Unloadeded registers report')
parser.add_argument('-input_ref', type=str, help='Old/Reference file path')
parser.add_argument('-input_new', type=str, help='New file path')
parser.add_argument('-output', type=str, help='Diffd/Output file path')
parser.add_argument('--Help', help='Script for finding diff between two reports of Unloadeded registers. Script is strictly format dependent, hence will not work if format is changed')
args = parser.parse_args()
old_file_name = args.input_ref
new_file_name = args.input_new
output_file_name = args.output

name_of_sheet = 'UnloadedRegisters'
# Opening old file, opening specific sheet if exists otherwise terminate the program with error message
old_file = xlrd.open_workbook(old_file_name) 
sheet_names_old_file = old_file.sheet_names()
if name_of_sheet not in sheet_names_old_file: 
    sys.exit('UnloadedRegisters Sheet in Reference/Old file does not exists')
sheet_old_file = old_file.sheet_by_name(name_of_sheet) 

# Opening new file, opening specific sheet if exists otherwise terminate the program with error message 
new_file = xlrd.open_workbook(new_file_name) 
sheet_names_new_file = new_file.sheet_names()
if name_of_sheet not in sheet_names_new_file: 
    sys.exit('UnloadedRegisters Sheet in New file does not exists')
sheet_new_file = new_file.sheet_by_name(name_of_sheet) 

# Creating a new file of given name to store the bucket splitted (diff) version
update_file = xlsxwriter.Workbook(output_file_name)
sheet_diff = update_file.add_worksheet(name_of_sheet)

# Various formats to highlight/bold/color cells.
bold = update_file.add_format({'bold': 1})
bold_bg_cyan = update_file.add_format({'bold': True, 'bg_color': '#33CCCC'})
bold_font_red = update_file.add_format({'bold': False, 'font_color': 'red'})
bold_font_green = update_file.add_format({'bold': False, 'font_color': 'green'})
bold_font_blue = update_file.add_format({'bold': False, 'font_color': 'blue'})

# Number of rows in sheets old and new files
no_rows_old_sheet = sheet_old_file.nrows
no_rows_new_sheet = sheet_new_file.nrows

# Number of columns in old and new files
no_columns_old_sheet = sheet_old_file.ncols
no_columns_new_sheet = sheet_new_file.ncols

row_of_diff_file = 0  # initializing row number of a diff file sheet with 4th column (starting from 0)

# Initializing the New xls with writing its column names same as of old file and adding Result column
for col_no in range(no_columns_old_sheet):
    sheet_diff.write(row_of_diff_file, col_no, str(sheet_old_file.col_values(col_no)[0]),bold_bg_cyan)
sheet_diff.write(row_of_diff_file, 2, 'Result',bold_bg_cyan)
sheet_diff.write(row_of_diff_file, 1, 'Comments',bold_bg_cyan)
row_of_diff_file = row_of_diff_file + 1

#### First section algorithm for Same as Before

for l1 in range(1,no_rows_new_sheet):
    
    temp_row_new_list = str(sheet_new_file.col_values(0)[l1])
    for l2 in range(1,no_rows_old_sheet):
           
        temp_row_old_list = str(sheet_old_file.col_values(0)[l2])

        if(temp_row_new_list==temp_row_old_list): 
            
            for col_no in range(no_columns_old_sheet):
                sheet_diff.write(row_of_diff_file, col_no, str(sheet_old_file.col_values(col_no)[l2]))
            sheet_diff.write(row_of_diff_file, 2, 'Same as Before',bold_font_blue) # Writing its category in 10th column            
            row_of_diff_file = row_of_diff_file + 1

#### Second section algorithm for New Violations

for l1 in range(1,no_rows_new_sheet):
    
    temp_row_new_list = str(sheet_new_file.col_values(0)[l1])
    x=0
    
    for l2 in range(1,no_rows_old_sheet):

        temp_row_old_list = str(sheet_old_file.col_values(0)[l2])
        if(temp_row_new_list==temp_row_old_list): 
            x = 1
            
    if(x==0):
        for col_no in range(no_columns_new_sheet):
            sheet_diff.write(row_of_diff_file, col_no, str(sheet_new_file.col_values(col_no)[l1]))
        sheet_diff.write(row_of_diff_file, 2, 'New Violation',bold_font_red) # Writing its category in 10th column
        row_of_diff_file = row_of_diff_file + 1

#### Third section algorithm for Removed Violations

for l1 in range(1,no_rows_old_sheet):

    temp_row_old_list = str(sheet_old_file.col_values(0)[l1])
    x=0
    
    for l2 in range(1,no_rows_new_sheet):
    
        temp_row_new_list = str(sheet_new_file.col_values(0)[l2])
        if(temp_row_old_list==temp_row_new_list): 
            x = 1           

    if(x==0):
        for col_no in range(no_columns_old_sheet):
            sheet_diff.write(row_of_diff_file, col_no, str(sheet_old_file.col_values(col_no)[l1]))
        sheet_diff.write(row_of_diff_file, 2, 'Removed Violation',bold_font_green) # Writing its category in 10th column
        row_of_diff_file = row_of_diff_file + 1

# Closing the file
update_file.close()


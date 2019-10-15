#!/usr/intel/pkgs/python3/3.6.3a/bin/python3
import sys
sys.path.append('/usr/intel/pkgs/python3/3.6.3/modules/r1/lib/python3.6/site-packages/')

import xlrd       # Module for Reading an excel file 
import xlsxwriter # Module for Writing an excel file 
import argparse   # Module for arguments parsing

# Argument Parser

parser = argparse.ArgumentParser(description='Script for Logic on Reset report')
parser.add_argument('old_file_path', type=str, help='Old file path')
parser.add_argument('new_file_path', type=str, help='new file path')
parser.add_argument('output_file_path', type=str, help='output file path')
args = parser.parse_args()
old_file_name = args.old_file_path
new_file_name = args.new_file_path
output_file_name = args.output_file_path

# Giving the location of the old and new files 
#location_oldfile = ("/nfs/sc/disks/sc_rtl_users_0002/asarode/script_automation/old_file_lor_fake_wo_ref.xls") 
#location_newfile = ("/nfs/sc/disks/sc_rtl_users_0002/asarode/script_automation/new_file_lor_fake_wo_ref.xls") 
  
# Opening old file and its logic on reset sheet for reading 
old_file = xlrd.open_workbook(old_file_name) 
lor_sheet_old_file = old_file.sheet_by_index(7) 

# Opening new file and its logic on reset sheet for reading 
new_file = xlrd.open_workbook(new_file_name) 
lor_sheet_new_file = new_file.sheet_by_index(7) 

# Creating a new file to store the bucket splitted (diff) version
#update_file = xlsxwriter.Workbook('lor_update.xlsx')
update_file = xlsxwriter.Workbook(output_file_name)
lor_sheet_diff = update_file.add_worksheet('lor_difference_report')

# Add a bold format to use to highlight cells.
bold = update_file.add_format({'bold': 1})

# Number of rows in sheets old and new files
no_rows_old_sheet = lor_sheet_old_file.nrows
no_rows_new_sheet = lor_sheet_new_file.nrows

# Number of columns in old and new files
no_columns_old_sheet = lor_sheet_old_file.ncols
no_columns_new_sheet = lor_sheet_new_file.ncols

row_of_diff_file = 0  # initializing row number from 3rd row onwards

# Initializing the New xls with writing its column names

cell_format = update_file.add_format({'bold': True, 'bg_color': '#33CCCC'})
cell_format2 = update_file.add_format({'bold': True, 'font_color': 'red'})

for col_no in range(no_columns_old_sheet):
    lor_sheet_diff.write(row_of_diff_file, col_no, str(lor_sheet_old_file.col_values(col_no)[0]),cell_format)
row_of_diff_file = row_of_diff_file + 1

# Adding comment line for first section
lor_sheet_diff.write(row_of_diff_file, 2, '*** Old Violations that has not resolved ***',cell_format2)
row_of_diff_file = row_of_diff_file + 1

col_no_list = [0,1,2,4,5]

# First section algorithm 
for l1 in range(1,no_rows_new_sheet):
    
    temp_row_new_list = []
    for m in col_no_list: # making a temporary list of a particular row from new file   
        temp_row_new_list.append(str(lor_sheet_new_file.col_values(m)[l1]))

    for l2 in range(1,no_rows_old_sheet):
        temp_row_old_list = []
        for n in col_no_list: # making a temporary list of a particular row from old file 
            temp_row_old_list.append(str(lor_sheet_old_file.col_values(n)[l2]))        

        if(temp_row_new_list==temp_row_old_list): 
            
            for col_no in range(no_columns_old_sheet):
                lor_sheet_diff.write(row_of_diff_file, col_no, str(lor_sheet_old_file.col_values(col_no)[l2]))
            lor_sheet_diff.write(row_of_diff_file, 3, str(lor_sheet_new_file.col_values(3)[l1]))
            row_of_diff_file = row_of_diff_file + 1

# Adding comment line for second section
lor_sheet_diff.write(row_of_diff_file,2, '*** New Violations ***',cell_format2)
row_of_diff_file = row_of_diff_file + 1

# Second section algorithm
for l1 in range(1,no_rows_new_sheet):
    
    temp_row_new_list = []

    for m in col_no_list: # making a temporary list of a particular row from new file   
        temp_row_new_list.append(str(lor_sheet_new_file.col_values(m)[l1]))
    x=0
    for l2 in range(1,no_rows_old_sheet):
        
        temp_row_old_list = []
        for n in col_no_list: # making a temporary list of a particular row from old file 
            temp_row_old_list.append(str(lor_sheet_old_file.col_values(n)[l2]))
        
        if(temp_row_new_list==temp_row_old_list): 
            x = 1
    if(x==0):
        for col_no in range(no_columns_new_sheet):
            lor_sheet_diff.write(row_of_diff_file, col_no, str(lor_sheet_new_file.col_values(col_no)[l1]))
        row_of_diff_file = row_of_diff_file + 1

# Adding comment line for third section
lor_sheet_diff.write(row_of_diff_file,2, '*** Old Violations that has resolved ***',cell_format2)
row_of_diff_file = row_of_diff_file + 1

# Third section algorithm
for l1 in range(1,no_rows_old_sheet):
    
    temp_row_old_list = []
    for m in col_no_list: # making a temporary list of a particular row from old file   
        temp_row_old_list.append(str(lor_sheet_old_file.col_values(m)[l1]))
    x=0
    for l2 in range(1,no_rows_new_sheet):
        temp_row_new_list = []
        for n in col_no_list: # making a temporary list of a particular row from new file 
            temp_row_new_list.append(str(lor_sheet_new_file.col_values(n)[l2]))
        
        if(temp_row_old_list==temp_row_new_list): 
            x = 1
    if(x==0):
        for col_no in range(no_columns_old_sheet):
            lor_sheet_diff.write(row_of_diff_file, col_no, str(lor_sheet_old_file.col_values(col_no)[l1]))
        row_of_diff_file = row_of_diff_file + 1

# Closing the file
update_file.close()



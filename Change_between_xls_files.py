#!/nfs/sc/disks/sc_rtl_users_0002/ryanjose/python/bin/python2.7
import sys
sys.path.append('/usr/intel/pkgs/python3/3.6.3/modules/r1/lib/python3.6/site-packages/')

import xlrd       # Module for Reading an excel file 
import xlsxwriter # Module for Writing an excel file 

# Giving the location of the old and new files 
location_oldfile = ("/nfs/sc/disks/sc_rtl_users_0002/asarode/script_automation/old_file_lor_fake.xls") 
location_newfile = ("/nfs/sc/disks/sc_rtl_users_0002/asarode/script_automation/new_file_lor_fake.xls") 
  
# Opening old file and its logic on reset sheet for reading 
old_file = xlrd.open_workbook(location_oldfile) 
lor_sheet_old_file = old_file.sheet_by_index(7) 

# Opening new file and its logic on reset sheet for reading 
new_file = xlrd.open_workbook(location_newfile) 
lor_sheet_new_file = new_file.sheet_by_index(7) 

# Creating a new file to store the bucket splitted (diff) version
update_file = xlsxwriter.Workbook('lor_update.xlsx')
lor_sheet_diff = update_file.add_worksheet('lor_difference_report')

# Number of rows in sheets old and new files
no_rows_old_sheet = lor_sheet_old_file.nrows
no_rows_new_sheet = lor_sheet_new_file.nrows

# Number of columns in old and new files
no_columns_old_sheet = lor_sheet_old_file.ncols
no_columns_new_sheet = lor_sheet_new_file.ncols

row_of_diff_file = 0  # initializing row number from 3rd row onwards

# Initializing the New xls with writing its column names
#lor_sheet_diff.write(1, 2, '*** Old Violations that has not resolved ***')
#lor_sheet_diff.write(1, 2, '*** Old Violations that has not resolved ***')

for col_no in range(no_columns_old_sheet):
    lor_sheet_diff.write(row_of_diff_file, col_no, str(lor_sheet_old_file.col_values(col_no)[0]))
row_of_diff_file = row_of_diff_file + 1

# Adding comment line for first section
lor_sheet_diff.write(row_of_diff_file, 2, '*** Old Violations that has not resolved ***')
row_of_diff_file = row_of_diff_file + 1

# First section algorithm 
for l1 in range(1,no_rows_new_sheet):
    
    temp_row_new_list = []
    for m in range(6): # making a temporary list of a particular row from new file   
        temp_row_new_list.append(str(lor_sheet_new_file.col_values(m)[l1]))

    for l2 in range(1,no_rows_old_sheet):
        temp_row_old_list = []
        for n in range(6): # making a temporary list of a particular row from old file 
            temp_row_old_list.append(str(lor_sheet_old_file.col_values(n)[l2]))        

        if(temp_row_new_list==temp_row_old_list): 
            
            for col_no in range(no_columns_old_sheet):
                lor_sheet_diff.write(row_of_diff_file, col_no, str(lor_sheet_old_file.col_values(col_no)[l2]))
            row_of_diff_file = row_of_diff_file + 1

# Adding comment line for second section
lor_sheet_diff.write(row_of_diff_file,2, '*** New Violations ***')
row_of_diff_file = row_of_diff_file + 1

# Second section algorithm
for l1 in range(1,no_rows_new_sheet):
    
    temp_row_new_list = []

    for m in range(6): # making a temporary list of a particular row from new file   
        temp_row_new_list.append(str(lor_sheet_new_file.col_values(m)[l1]))
    x=0
    for l2 in range(1,no_rows_old_sheet):
        
        temp_row_old_list = []
        for n in range(6): # making a temporary list of a particular row from old file 
            temp_row_old_list.append(str(lor_sheet_old_file.col_values(n)[l2]))
        
        if(temp_row_new_list==temp_row_old_list): 
            x = 1
    if(x==0):
        for col_no in range(no_columns_new_sheet):
            lor_sheet_diff.write(row_of_diff_file, col_no, str(lor_sheet_new_file.col_values(col_no)[l1]))
        row_of_diff_file = row_of_diff_file + 1

# Adding comment line for third section
lor_sheet_diff.write(row_of_diff_file,2, '*** Old Violations that has resolved ***')
row_of_diff_file = row_of_diff_file + 1

# Third section algorithm
for l1 in range(1,no_rows_old_sheet):
    
    temp_row_old_list = []
    for m in range(6): # making a temporary list of a particular row from old file   
        temp_row_old_list.append(str(lor_sheet_old_file.col_values(m)[l1]))
    x=0
    for l2 in range(1,no_rows_new_sheet):
        temp_row_new_list = []
        for n in range(6): # making a temporary list of a particular row from new file 
            temp_row_new_list.append(str(lor_sheet_new_file.col_values(n)[l2]))
        
        if(temp_row_old_list==temp_row_new_list): 
            x = 1
    if(x==0):
        for col_no in range(no_columns_old_sheet):
            lor_sheet_diff.write(row_of_diff_file, col_no, str(lor_sheet_old_file.col_values(col_no)[l1]))
        row_of_diff_file = row_of_diff_file + 1

# Closing the file
update_file.close()

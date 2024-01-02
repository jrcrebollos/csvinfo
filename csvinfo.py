import pandas as pd
import numpy as np

def csvinfo(
        df = pd.DataFrame(),
        csvfile = '',
        filter_typ ='DVDD== 0.9 and VDDIO == 2.6 and temperature == 25 and mos_mod=="Mtt"', 
        filter = '',
        output_variables = None,
        file_name = None,

        ):
    
    # ANSI escape code for red text
    red_text    = "\033[91m"
    green_text  = "\033[92m"
    orange_text = "\033[93m"
    yellow_text = "\033[93m"
    reset_color = "\033[0m"

    # Info, Warnings and Errors Messages
    INFO_MSG1   = green_text+"Reading csv/dataframe.........."+reset_color
    ERROR_MSG1  = red_text + "Error: No csvfile or data." + reset_color
    
    # Check if a file name is provided for saving the plot
    if file_name is not None:
        save = True    
    # Print Messages to know it is starting processing
    print(INFO_MSG1)

    # Check for errors and load data if needed
    if len(csvfile) == 0 and df.empty == True:
        print(ERROR_MSG1)
        return 
    if len(csvfile) > 0 and df.empty == False:
        print(red_text + "Error: Both csvfile and df input variables are entered. Please choose only one." + reset_color)
        return 
    if len(csvfile) == 0 and df.empty == False:
        pass
    if len(csvfile) > 0 and df.empty == True:
        df = pd.read_csv(csvfile)
        
    #Applying filtering
    if len(filter)>0:
        print("Applying filter...")
        df = df.query(filter)   
    print("Done loading csv file..")   
    print(save)

    index_of_target_column = df.columns.get_loc("Pass/Fail")
    output_variables = df.columns[index_of_target_column+1:].values

    max_values=df[output_variables].max().values
    min_values=df[output_variables].min().values
    typical_values = df.query(filter_typ)[output_variables].values
    df_min_val = pd.DataFrame(min_values, columns = ['Min'])
    df_max_val = pd.DataFrame(max_values, columns = ['Max'])
    df_typ_val = pd.DataFrame(typical_values[0], columns = ['Typical'])
    df_output_var = pd.DataFrame(output_variables, columns = ['Parameters'])
    df_summary = pd.concat([df_output_var, df_min_val,df_typ_val,df_max_val],axis=1)

    if save == True:
        df_summary.to_csv(file_name,index=False)

    return df_summary
    

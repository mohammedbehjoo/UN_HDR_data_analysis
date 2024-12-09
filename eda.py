import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os
from pathlib import Path

# a function for deleting every .txt file in the root directory and its sub-directories 
def delete_txt_file(directory):
    path=Path(directory)
    for txt_file in path.rglob("*.txt"):
        txt_file.unlink()
        print(f"Deleted: {txt_file}\n","-"*30)


# a function to cast to float and integer datatypes. use for desired columns.
def cast_number(item):
    try:
        # First, try to cast to float
        return float(item) if isinstance(float(item), float) else item
    except (TypeError, ValueError):
        try:
            # If float conversion fails, try casting to int
            return int(item)
        except (TypeError, ValueError):
            return item
    
# check if the config file exits
try:
    print("the dataset exists: ",os.path.exists("config.env"),"\n")
except:
    print("the dataset file is either missing or empty\n")
# load the config file from the config.env file
load_dotenv("config.env")

# root directory of the output
root_dir=os.getenv("root_dir_output")

# directory for saving the result text file of the HDI dataframe
save_txt_hdi=os.path.join(root_dir,"txt/hdi")
os.makedirs(save_txt_hdi,exist_ok=True)
print(f"the result txt director of HDI:\n{save_txt_hdi}\n","-"*30)

# create the file of the txt output of HDI dataframe.
df_hdi_txt=os.path.join(save_txt_hdi,"output.txt")

# delete the .txt files before starting. it makes sure that every .txt file is being created from scratch
delete_txt_file(root_dir)

# check the path of the dataset
print(f"path of the dataset:\n{os.getenv('data_path')}","\n","-"*30)

# excel filepath
filepath=os.path.join(os.getenv("data_path"),"HDR23-24_Statistical_Annex_Tables_1-7.xlsx")
print(f"excel file path is:\n{filepath}\n")

# let's load the dataset file
df_HDI=pd.read_excel(filepath,sheet_name="HDI")

# let's filter and remove the columns that their names contain "unnamed".
df_HDI=df_HDI.loc[:,~df_HDI.columns.str.contains("^Unnamed")]

# describe the dataset to have an insight of it.
print(f"Describe df_HDI:\n{df_HDI.describe()}\n","-"*30)
with open(df_hdi_txt,"a") as file:
    file.write("Describe the df_HDI dataframe:\n")
    file.write(df_HDI.describe().to_string())
    file.write("\n"+"-"*30)
    print(f"df_HDI describe is written to the file {df_hdi_txt}\n","-"*30)
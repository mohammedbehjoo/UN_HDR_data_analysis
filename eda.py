import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

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

print(f"path to the dataset:\n{os.getenv('data_path')}","\n","-"*30)

# excel filepath
filepath=os.path.join(os.getenv("data_path"),"HDR23-24_Statistical_Annex_Tables_1-7.xlsx")
print(f"file path is:\n{filepath}\n")

# let's load the dataset file
df_HDI=pd.read_excel(filepath,sheet_name="HDI")

# let's filter and remove the columns that their names contain "unnamed".
df_HDI=df_HDI.loc[:,~df_HDI.columns.str.contains("^Unnamed")]

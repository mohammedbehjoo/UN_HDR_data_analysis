import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os
from pathlib import Path

# a function for deleting every .txt file in the root directory and its sub-directories


def delete_txt_file(directory):
    path = Path(directory)
    for txt_file in path.rglob("*.txt"):
        txt_file.unlink()
        print(f"Deleted: {txt_file}\n", "-"*30)


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
    print("the dataset exists: ", os.path.exists("config.env"), "\n")
except:
    print("the dataset file is either missing or empty\n")
# load the config file from the config.env file
load_dotenv("config.env")

# root directory of the output
root_dir = os.getenv("root_dir_output")

# directory for saving the result text file of the HDI dataframe
save_txt_hdi = os.path.join(root_dir, "txt/hdi")
os.makedirs(save_txt_hdi, exist_ok=True)
print(f"the result txt director of HDI:\n{save_txt_hdi}\n", "-"*30)

# create the file of the txt output of HDI dataframe.
df_hdi_txt = os.path.join(save_txt_hdi, "output.txt")

# delete the .txt files before starting. it makes sure that every .txt file is being created from scratch
delete_txt_file(root_dir)

# check the path of the dataset
print(f"path of the dataset:\n{os.getenv('data_path')}", "\n", "-"*30)

# excel filepath
filepath = os.path.join(os.getenv("data_path"),
                        "HDR23-24_Statistical_Annex_Tables_1-7.xlsx")
print(f"excel file path is:\n{filepath}\n")

# let's load the dataset file
df_HDI = pd.read_excel(filepath, sheet_name="HDI")

# let's filter and remove the columns that their names contain "unnamed".
df_HDI = df_HDI.loc[:, ~df_HDI.columns.str.contains("^Unnamed")]

# let's rename the columns to have better namings
df_HDI.rename(columns={"Human Development Index (HDI) ": "HDI",
              "HDI rank.1": "HDI_rank"}, inplace=True)

# cast the specified columns to the numeric values
df_HDI[["HDI", "Expected years of schooling", "Mean years of schooling", "Gross national income (GNI) per capita", "GNI per capita rank minus HDI rank", "HDI_rank"]] = df_HDI[[
    "HDI", "Expected years of schooling", "Mean years of schooling", "Gross national income (GNI) per capita", "GNI per capita rank minus HDI rank", "HDI_rank"]].apply(pd.to_numeric, errors="coerce")

# drop the HDI rank column. it was redundant.
df_HDI.drop("HDI rank", inplace=True, axis=1)

# # describe the dataset to have an insight of it.
# print(f"Describe df_HDI:\n{df_HDI.describe()}\n","-"*30)
# with open(df_hdi_txt,"a") as file:
#     file.write("Describe the df_HDI dataframe:\n")
#     file.write(df_HDI.describe().to_string())
#     file.write("\n"+"-"*30+"\n")
#     print(f"df_HDI describe is written to the file {df_hdi_txt}\n","-"*30)

# # check the dtypes of the dataframe.
# print(f"dtypes of df_HDI:\n{df_HDI.dtypes}\n","-"*30)

# with open(df_hdi_txt,"a") as file:
#     file.write("dtypes of df_HDI:\n")
#     file.write(df_HDI.dtypes.to_string())
#     file.write("\n"+"-"*30+"\n")
#     print(f"dtypes of df_HDI is written at {df_hdi_txt}.\n","-"*30)

# check fr missing values
print(f"check for number of null values: {df_HDI.isnull().sum()}\n","-"*30)

# write the number of null values to the output txt file.
with open(df_hdi_txt, "a") as file:
    file.write("number of null values of df_HDI:\n")
    file.write(df_HDI.isnull().sum().to_string())
    file.write("\n"+"-"*30+"\n")
    print(
        f"number of null values of df_HDI is written at {df_hdi_txt}.\n", "-"*30)
    
# check the rows with missing values
missing_rows=df_HDI[df_HDI.isna().any(axis=1)]
print(f"missing rows of df_HDI:\n{missing_rows}\n","-"*30)

# write the rows with missing values to the output file
with open(df_hdi_txt,"a") as file:
    file.write("rows with missing values:\n")
    file.write(missing_rows.to_string())
    file.write("\n"+"-"*30+"\n")
    print(
        f"rows with missing values of df_HDI is written at {df_hdi_txt}.\n", "-"*30)
    
# get rid rows with missing values
df_HDI_clean=df_HDI.dropna()


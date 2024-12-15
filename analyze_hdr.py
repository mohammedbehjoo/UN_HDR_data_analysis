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

# function for detecting outliers using IQR method
def detect_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3-Q1
    lower_bound = Q1-1.5*IQR
    upper_bound = Q3+1.5*IQR
    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    return outliers


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

# let's create a folder for saving figures and charts
save_figures_hdi=os.path.join(root_dir,"figures/hdi")
os.makedirs(save_figures_hdi,exist_ok=True)
print(f"save hdi figures at: {save_figures_hdi}")


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

# describe the dataset to have an insight of it.
print(f"Describe df_HDI:\n{df_HDI.describe()}\n","-"*30)
with open(df_hdi_txt,"a") as file:
    file.write("Describe the df_HDI dataframe:\n")
    file.write(df_HDI.describe().to_string())
    file.write("\n"+"-"*30+"\n")
    print(f"df_HDI describe is written to the file {df_hdi_txt}\n","-"*30)

# check the dtypes of the dataframe.
print(f"dtypes of df_HDI:\n{df_HDI.dtypes}\n","-"*30)

with open(df_hdi_txt,"a") as file:
    file.write("dtypes of df_HDI:\n")
    file.write(df_HDI.dtypes.to_string())
    file.write("\n"+"-"*30+"\n")
    print(f"dtypes of df_HDI is written at {df_hdi_txt}.\n","-"*30)

# check fr missing values
print(f"check for number of null values: {df_HDI.isnull().sum()}\n", "-"*30)

# write the number of null values to the output txt file.
with open(df_hdi_txt, "a") as file:
    file.write("number of null values of df_HDI:\n")
    file.write(df_HDI.isnull().sum().to_string())
    file.write("\n"+"-"*30+"\n")
    print(
        f"number of null values of df_HDI is written at {df_hdi_txt}.\n", "-"*30)

# check the rows with missing values
missing_rows = df_HDI[df_HDI.isna().any(axis=1)]
print(f"missing rows of df_HDI:\n{missing_rows}\n", "-"*30)

# write the rows with missing values to the output file
with open(df_hdi_txt, "a") as file:
    file.write("rows with missing values:\n")
    file.write(missing_rows.to_string())
    file.write("\n"+"-"*30+"\n")
    print(
        f"rows with missing values of df_HDI is written at {df_hdi_txt}.\n", "-"*30)

# get rid rows with missing values
df_HDI_clean = df_HDI.dropna()

# detecting outliers
# first, select only the numeric columns
numeric_columns = df_HDI_clean.select_dtypes(include="float64").columns
for column in numeric_columns:
    outliers = detect_outliers_iqr(df_HDI_clean, column)
    # only print the columns iwth outliers
    if len(outliers) == 0:
        continue
    print(f"Outliers in {column}: {len(outliers)}\n")
    print(outliers, "\n", "-"*30)

# write the columns with outliers to the output .txt file
with open(df_hdi_txt, "a") as file:
    file.write("Outlier of df_HDI_clean dataframe:\n")
    for column in numeric_columns:
        outliers = detect_outliers_iqr(df_HDI_clean, column)
        # only print the columns iwth outliers
        if len(outliers) == 0:
            continue
        file.write(f"Outliers in {column}: {len(outliers)}\n")
        file.write(outliers.to_string())
        file.write("\n" + "-" * 30 + "\n")
    print(
        f"columns with outliers of df_HDI_clean is written at {df_hdi_txt}.\n", "-"*30)

# TODO: remove outliers for statsitcal and ML purposes only.


# let's do dome EDA
# plot the distirbution of columns
for column in numeric_columns:
    if column=="HDI_rank":
        continue
    plt.figure(figsize=(8,6))
    sns.histplot(df_HDI_clean[column],kde=True)
    plt.title(f"Distribution of {column}")
    figures_save_file=os.path.join(save_figures_hdi,f"Disribution of {column}.jpg")
    plt.savefig(figures_save_file,format="jpg")
    plt.close()
    print(f"Distribution figure of {column} column is saved at:{figures_save_file}"+"\n"+"-"*30,"\n")

# let's check for outliers using boxplots
for column in numeric_columns:
    if column=="HDI_rank":
        continue
    plt.figure(figsize=(8,6))
    sns.boxplot(x=df_HDI_clean[column])
    plt.title(f"Boxplot of {column}")
    figures_save_file=os.path.join(save_figures_hdi,f"Boxplot of {column}.jpg")
    plt.savefig(figures_save_file,format="jpg")
    plt.close()
    print(f"Outliers of {column} column is saved at:{figures_save_file}"+"\n"+"-"*30,"\n")
    

# check the correlation between numeric variables
correlation_matrix=df_HDI_clean[numeric_columns].corr()
sns.heatmap(correlation_matrix,annot=True,cmap="Pastel2_r",linewidths="0.5",linecolor="gray")
figures_save_file=os.path.join(save_figures_hdi,f"Correlation matrix of df_HDI_clean.jpg")
plt.savefig(figures_save_file,format="jpg")
plt.close()
print(f"Correlation matrix of df_HDI_clean is saved at:{figures_save_file}"+"\n"+"-"*30,"\n")

# pairplot
sns.pairplot(df_HDI_clean[numeric_columns],corner=True)
figures_save_file=os.path.join(save_figures_hdi,f"Pairplot of df_HDI_clean.jpg")
plt.savefig(figures_save_file,format="jpg")
plt.close()
print(f"Pairplot of df_HDI_clean is saved at:{figures_save_file}"+"\n"+"-"*30,"\n")

# plot the HDI of top 10 countries
top_countries=df_HDI_clean[["Country","HDI"]].head(10)
plt.figure(figsize=(12,10))
sns.scatterplot(x="Country",y="HDI",data=top_countries)
plt.title("Top 10 countries by HDI")
plt.xticks(rotation=45)
figures_save_file=os.path.join(save_figures_hdi,f"Top 10 countries by HDI.jpg")
plt.savefig(figures_save_file,format="jpg")
plt.close()
print(f"Top 10 countries by HDI is saved at:{figures_save_file}"+"\n"+"-"*30,"\n")


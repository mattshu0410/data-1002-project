import pandas as pd
import numpy as np
import re

from plotnine import *

#Reading in the data
world_happiness = pd.read_csv("https://raw.githubusercontent.com/mattshu0410/data-1002-project/master/world_happiness_2017.csv")
freedom_index = pd.read_csv("https://raw.githubusercontent.com/mattshu0410/data-1002-project/master/hfi_cc_2019.csv")
gni_capita = pd.read_csv("https://raw.githubusercontent.com/mattshu0410/data-1002-project/master/GNI_percapita_ppp.csv")
iso_code = pd.read_csv("https://raw.githubusercontent.com/mattshu0410/data-1002-project/master/wikipedia-iso-country-codes.csv")

#Extract only 2017 Data for Freedom Index
index_not_2017 = freedom_index[freedom_index["year"] != 2017].index
freedom_index.drop(index_not_2017, inplace=True)

#Extract only 2017 Data from GNI/capita PPP
gni_capita_2017 = gni_capita.iloc[:,[0,1,61]]
print(gni_capita_2017)

#Extract only ISO code & Countries from iso_code
iso_code = iso_code.iloc[:,[0,2]]

#Change Headings of all datasets to Match Freedom Index Dataset
world_happiness = world_happiness.rename(columns={"Country":"countries"})
gni_capita_2017 = gni_capita_2017.rename(columns={"Country Code":"ISO_code",
                                                  "Country Name":"countries",
                                                  "2017":"GNI_capita"})
iso_code = iso_code.rename(columns={"English short name lower case":"countries",
                                    "Alpha-3 code":"ISO_code"})

#Add ISO Code to World Happiness (It doesn't originally have ISO code)
world_happiness = pd.merge(world_happiness, iso_code, on=["countries"])

#Drops redundant country columns from Freedom Index, GNI/capita
del gni_capita_2017['countries']
del world_happiness['countries']

#Changes all empty values in all datasets to NaN (i.e. empty)
gni_capita_2017 = gni_capita_2017.replace('', np.nan)
world_happiness = world_happiness.replace(0, np.nan)
freedom_index = freedom_index.replace('-', np.nan)

#Merges data based on matching ISO Codes to avoid errors in different spelling of countries
#Implicitly removes country data that is not present in all three sources
merged_data = pd.merge(freedom_index, world_happiness, on=["ISO_code"])
merged_data = pd.merge(merged_data, gni_capita_2017, on=["ISO_code"])
print(merged_data)

#Selects columns that are relevant to our analysis
merged_data = merged_data[["year", "ISO_code", "countries", "region", "hf_score", "hf_rank", "Happiness.Rank", "Happiness.Score", "GNI_capita"]]

#Remove row entries that have empty cells in any of the columns
merged_data.dropna(inplace=True)

#Remove duplicates
merged_data.drop_duplicates()

#Output the dataset
print(merged_data)
merged_data.to_csv(r'C:\Users\bigha\OneDrive\University Notes\First Year SEM 2\DATA1002\Project\merged_data.csv',index = False)



#Checks if all data values are within their expected ranges: returns True if data is within ranges
print((merged_data["hf_score"].astype(float) >= 0).all() and (merged_data["hf_score"].astype(float) <= 10).all()) #Between 0 and 10 inclusive
print((merged_data["Happiness.Score"].astype(float) >= 0).all() and (merged_data["Happiness.Score"].astype(float) <= 10).all()) #Between 0 and 10 inclusive
print((merged_data["hf_rank"].astype(float) >= 1).all() and (merged_data["hf_rank"].astype(float) <= 159).all()) #Between 1 and 159 inclusive
print((merged_data["Happiness.Rank"].astype(float) >= 1).all() and (merged_data["Happiness.Rank"].astype(float) <= 155).all())
print((merged_data["GNI_capita"].astype(float) >= 0).all()) #Ensuring non-negative values



#This function check every item of a given column in a given dataframe for special characters that shouldn't be present and returns a bool
def check_special(column, dataframe):
    special_char = True
    string_check= re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    for item in dataframe[column]:
        if string_check.search(str(item)) == None:
            special_char = False
        else:
            special_char = True
    return special_char

#The following for loop checks all code to ensure the correct types of characters are present for each column i.e. alphabetic, numeric
for column_name in merged_data:
    if check_special(column_name, merged_data) == True:
        print(column_name, ": some entries have special characters that are invalid" )
    else:
        if pd.to_numeric(merged_data[column_name], errors='coerce').notnull().all() == True:
            print(column_name, ": is entirely numeric")
        elif not merged_data[column_name].str.isnumeric().all() == True:
            print(column_name, " is entirely alphabetical letters or normal punctuation")
        else:
            print(column_name, ": column contains inappropriately mixed data")

#Changes data from string to numerical values
merged_data['hf_score'] = pd.to_numeric(merged_data['hf_score'])

#Basic Summary
print("Happiness Data Summary")
happiness_summary = merged_data['Happiness.Score'].describe()
print(happiness_summary)
print("Maximum Happiness in:", merged_data.loc[merged_data['Happiness.Score'].idxmax(),'countries'])
print("Minimum Happiness in:", merged_data.loc[merged_data['Happiness.Score'].idxmin(),'countries'])

print("Human Freedom Data Summary")
hf_summary = merged_data['hf_score'].describe()
print(hf_summary)
print("Maximum Human Freedom in:", merged_data.loc[merged_data['hf_score'].idxmax(),'countries'])
print("Minimum Human Freedom in:", merged_data.loc[merged_data['hf_score'].idxmin(),'countries'])

print("GNI/capita Data Summary")
GNI_summary = merged_data['GNI_capita'].describe()
print(GNI_summary)
print("Maximum GNI/capita in:", merged_data.loc[merged_data['GNI_capita'].idxmax(),'countries'])
print("Minimum GNI/capita in:", merged_data.loc[merged_data['GNI_capita'].idxmin(),'countries'])

#Basic Plots
p1 = (ggplot(merged_data, aes(x="GNI_capita", y="hf_score", color = 'Happiness.Score'))+
      geom_point() +
      xlab("GNI per Capita (PPP)") +
      ylab("Human Freedom Score") +
      labs(title = "Human Freedom Score versus GNI per Capita by Happiness Score"))
p2 = (ggplot(merged_data, aes(x="GNI_capita", y="Happiness.Score", color = 'hf_score'))+ \
      geom_point() +
      xlab("GNI per Capita (PPP)") +
      ylab("Happiness Score") +
      labs(title = "Happiness versus GNI per Capita by Human Freedom Score"))
print(p1,p2)

#Grouped Aggregates
#Average GNI for each quartile of Happiness
merged_data["Happiness_Quartile"] = pd.qcut(merged_data["Happiness.Score"], q=4, labels=[1,2,3,4])
print(merged_data.groupby("Happiness_Quartile").agg(
    average_GNI_capita = pd.NamedAgg(column = "GNI_capita", aggfunc=np.mean)
))
#Maximum Happiness grouped by Region
print(merged_data.groupby("region")["Happiness.Score"].max())
#SD of happiness in each Income Brackets
merged_data["GNI_capita_bins"] = pd.cut(merged_data["GNI_capita"], bins=[0,1025,4035,12475,float('inf')]) #These values from World Bank, Max is Arbitrary
print(merged_data.groupby("GNI_capita_bins").agg(
    sd_happiness = pd.NamedAgg(column="Happiness.Score", aggfunc=np.std)
))
#Median GNI/capita for each quartile of Freedom Index
merged_data["Freedom_Quartile"] = pd.qcut(merged_data["hf_score"], q=4, labels=[1,2,3,4])
print(merged_data.groupby("Freedom_Quartile").agg(
    median_GNI_capita = pd.NamedAgg(column = "GNI_capita", aggfunc=np.median)
))

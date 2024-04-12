# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 21:32:53 2023

@author: admin
"""

###Using sql to python database connectivity to load the cleaned dtaset from sql database.
####pip install mysql-connector-python
import mysql.connector
import pandas as pd

# Replace these values with your MySQL server details
host = "localhost"
user = "root"
password = "23012002"
database = "pallet"

# Establish a connection to the MySQL server
connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database)

# Create a cursor object to interact with the database
cursor = connection.cursor()

#load the cleaned data from pallet_masked_fulldata1 table in sql to the result variable as list.
cursor.execute("select * from pallet_masked_fulldata1")
result = cursor.fetchall()

#the result list have to be convert into data frame so we use this codes for df dataframe to store clean data.
columns = [i[0] for i in cursor.description]
pallet_Data = pd.DataFrame(result, columns=columns)


########### EDA ON RAW DATA #########

######## FIRST MOMENT BUSINESS DECISION/ MEASURE OF CENTRAL TENDENCY #########

## MEAN ##
QTY_mean = pallet_Data.QTY.mean()
print("mean of QTY:",QTY_mean)
# mean of QTY: 42.96495886959314

## MEDIAN ##
QTY_median = pallet_Data.QTY.median()
print("median of QTY:",QTY_median)
## median of QTY: 100.0

## MODE ## 
QTY_mode = pallet_Data.QTY.mode()
print("mode of QTY:",QTY_mode)
## mode of QTY: 0    100

### CustName
CustName_mode = pallet_Data.CustName.mode()
print("mode of CustName:",CustName_mode)
## mode of CustName: 0    11

### City
City_mode = pallet_Data.City.mode()
print("mode of City:",City_mode)
## mode of City:  Ahmedabad

### Region
Region_mode = pallet_Data.Region.mode()
print("mode of Region:",Region_mode)
## mode of Region: North

### State
State_mode = pallet_Data.State.mode()
print("mode of State:",State_mode)

### Product Code
Product_Code_mode = pallet_Data.Product_Code.mode()
print("mode of Product_Code:",Product_Code_mode)
## # Maharashtra

###Transaction Type
Transaction_type_mode = pallet_Data.Transaction_type.mode()
print("mode of Transaction Type:",Transaction_type_mode)
## # Allot

### WHName
WHName_mode = pallet_Data.WHName.mode()
print("mode of WHName:",WHName_mode)
## mode of WHName: 0    1009
##### SECOND MOMENT BUSINESS DECISION / MEASURE OF DISPERSION #######
## VARIANCE
QTY_variance = pallet_Data.QTY.var()
print("variance of QTY:",QTY_variance)
## variance of QTY: 45242.06274117576

### STANDARD DEVIATION ###
QTY_std = pallet_Data.QTY.std()
print("standard deviation of QTY:",QTY_std)
## standard deviation of QTY: 212.70181649712293

### RANGE ###
QTY_range = max(pallet_Data.QTY) - min(pallet_Data.QTY)
print("range of QTY:",QTY_range)
## range of QTY: 1140


###### THIRD MOMENT BUSINESS DECISION / SKEWNESS ######
QTY_skew = pallet_Data.QTY.skew()
print("skewness of QTY:",QTY_skew)
## skewness of QTY: -0.2139977431626821

###### FOURTH MOMENT BUSINESS DECISION / KURTOSIS #####
QTY_kurtosis = pallet_Data.QTY.kurt()
print("kurtosis of QTY:",QTY_kurtosis)
 ## kurtosis of QTY: -0.9177810283949985
 
######## DATA PREPROCESSING #####

### FINDING NULL VALUE COUNT ######
pallet_Data.isna().sum()
 ## No of Null Values = 0
 
### FINDING DUPLICATE COUNT
duplicate=pallet_Data.duplicated()
duplicate.unique()
sum(duplicate)
### 16938 duplicates found

#Removing the duplicates from the dataset
pallet_Data.drop_duplicates(keep = 'first', inplace = True)

###Again checking no of duplicates in the Dataset 
duplicate=pallet_Data.duplicated()
duplicate.unique()
sum(duplicate)
 ### 0 duplicates found
 
### FINDING OUTLIERS COUNT
from feature_engine.outliers import Winsorizer
import matplotlib.pyplot as plt 
pallet_Data.plot(kind="box",subplots=True,sharey=False,figsize=(15,15)) 
# outlers = 0 (There is no outliers in the dataset)
                    #or#
Q1 = pallet_Data['QTY'].quantile(0.25)
Q3 = pallet_Data['QTY'].quantile(0.75)
IQR = Q3-Q1
pallet_Data = pallet_Data[(pallet_Data['QTY']>= Q1 - 1.5*IQR) & (pallet_Data['QTY']<= Q3 + 1.5*IQR)]
print(pallet_Data)
plt.boxplot(pallet_Data.QTY)    
#### No outliers found        

##### GRAPHICAL REPRESENTATION ##### 
import numpy as np
import matplotlib.pyplot as pt
import seaborn as sns
from scipy import stats
from sqlalchemy import create_engine

######## BOX PLOT ##############
pallet_Data.plot(kind="box",subplots=True,sharey=False,figsize=(15,15))
# With the help of box plot we find the median,quantiles and potential outliers
# 0 Outliers

######## HISTOGRAM PLOT ##############
plt.hist(pallet_Data.CustName,color='green', bins=100 , alpha = 1)
plt.hist(pallet_Data.QTY,color='orange', bins=100 , alpha = 1)
plt.hist(pallet_Data.WHName,color='blue', bins=100, alpha = 1)
# This graph visually represents the distribution of the dataset by dividing into intervals(bins)
# and displaying the frequency or count of values within each bin.

########### DENSITY PLOT ############
sns.kdeplot(pallet_Data.QTY)
# It helps visualize the probability density of a continuous variable, 
#offering insights into the shape and features of the underlying data distribution,
#similar to a histogram but with a focus on the continuous nature of the data.

########## SCATTER PLOT #############
sns.pairplot(pallet_Data)
plt.scatter(x=pallet_Data.QTY, y=pallet_Data.CustName)
plt.scatter(x=pallet_Data.QTY, y=pallet_Data.WHName)
#displays individual data points on a two-dimensional graph, allowing the examination of the relationship between two numerical variables
# It helps identify patterns, trends, and potential correlations or outliers in the data by visualizing the pairwise interaction between the variables.

############# DISTRIBUTION PLOT ###############
sns.distplot(pallet_Data.QTY)
#provides a comprehensive visualization of the univariate distribution of a variable.
# it is particularly useful for understanding the probability density across different values of a continuous variable.

############ LINE CHART ##############
# set the figure size:
plt.figure(figsize = (10,10))
plt.plot(pallet_Data['Date'], pallet_Data['QTY'], color='r', marker='*', linestyle='--')
Date = np.arange(1,13)
# Add labels and title
plt.xlabel('Date')
plt.ylabel('Quantity')
plt.title('Quantity Over Time')
# Add a grid with green color and solid linestyle
plt.grid(color='g', linestyle='--')
# displaying the plot
plt.show
## A line chart visually represents trends and patterns in data through connected markers on a graph, 
# making it useful for displaying continuous information or time series.

########### VIOLIN PLOT ########
sns.violinplot(data = pallet_Data,x = "Region", y = "QTY", palette = ['red','green','pink','purple'] )
# It is the similar to a Boxplot, the Displays the kernel Density estimator for the underlying distribution
# It shows the distributionn of the quantitative data across categorical variables such that those distribution can be compared
# Here, we can identify the distribution of QTY data across Region variable
sns.violinplot(data = pallet_Data,x = "Transaction Type", y = "QTY", palette = ['red','green'])

######## BAR PLOT #######
sns.barplot(data = pallet_Data, x = 'CustName', y = 'QTY')
plt.show()
# Identify which customers are major contributors to the overall quantity, allowing for targeted customer management strategies.
sns.barplot(data = pallet_Data, x = 'Transaction Type', y = 'QTY')
plt.show()
# Understand the balance between incoming and outgoing pallets and identify any trends or irregularities.
sns.barplot(data = pallet_Data, x = 'Product Code', y = 'QTY')
plt.show()
# Insights: Identify which products contribute the most to the overall quantity, helping in inventory management and demand forecasting.
sns.barplot(data = pallet_Data, x = 'WHName', y = 'QTY')
plt.show()
# Identify high-performing or low-performing warehouses, helping in optimizing inventory storage and distribution.
sns.barplot(data = pallet_Data, x = 'Transaction Type', y = 'WHName')
plt.show()
# Understand how different transaction types impact individual warehouses.

##### AUTO EDA ON CLEANED DATA #########

# SWEETVIZ
# pip install sweetviz
import sweetviz as sv
sv.analyze(pallet_Data)
s = sv.analyze(pallet_Data)
s.show_html('sweetviz_report.html')


# DTALE
# pip install datle
import dtale
d = dtale.show(pallet_Data)
d.open_browser()

# Extracting cleaned data to the desktop 
pallet_Data = pd.DataFrame(pallet_Data)
pallet_Data.to_excel("C:\\Users\\admin\\OneDrive\\Desktop\\SCM Cleaned data.xlsx", index=False)
print("Done")

# AUTOVIZ
# pip install autoviz
from autoviz.AutoViz_Class import AutoViz_Class
av = AutoViz_Class()
%matplotlib inline
a = av.AutoViz(r"C:\Users\admin\OneDrive\Desktop\SCM Cleaned data.xlsx")

## PANDAS PROFILING ##
## pip install pandasprofiling
from pandas_profiling import ProfileReport
# pip install --upgrade typing
# pip install ydata_profiling
import sys
import webbrowser
from ydata_profiling import ProfileReport
Pallet_Profile = ProfileReport(pallet_Data, title = "Panda Profiling Report")
Pallet_Profile.to_notebook_iframe()
webbrowser.open("Panda Profiling Report.html")

## DATAPREP ##
# pip install dataprep
import dataprep
from dataprep.eda import create_report
report = create_report(df, title='My Report')
report.show_browser()







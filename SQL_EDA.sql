CREATE DATABASE pallet;
SHOW DATABASES;
USE pallet;
SELECT * FROM pallet_masked_fulldata1;

######## EXPLORATORY DATA ANALYSIS (EDA) BEFORE PREPROCEESING #########
##### FIRST MOMENT BUSINESS/MEASURES OF CENTRAL TENDENCY #####
#### MEAN ######
SELECT AVG(QTY) AS mean_QTY FROM pallet_masked_fulldata1;
# QTY MEAN = 42.9650

###### MEDIAN #######
SELECT QTY AS Median_QTY
FROM (
SELECT QTY, ROW_NUMBER() OVER (ORDER BY QTY) AS row_num,
COUNT(*) OVER() AS total_count
FROM  pallet_masked_fulldata1
) AS subquery
WHERE row_num = (total_count + 1)/2 OR row_num 
= (total_count + 2)/2;
## QTY MEDIAN = 100

######### MODE ###########
SELECT QTY AS mode_QTY
FROM (
SELECT QTY, COUNT(*) AS frequency 
FROM pallet_masked_fulldata1
GROUP BY QTY
ORDER BY frequency DESC
LIMIT 1
) AS subquery;
### QTY MODE = 100

########### SECOND MOMENT BUSINESS DECISION/MEASURES OF DISPERSION ############
#### VARIANCE #####
SELECT VARIANCE(QTY) AS performance_variance FROM pallet_masked_fulldata1;
## VARIANCE OF QTY = 45241.50393503548

######## STANDARD DEVIATION ########
SELECT STDDEV(QTY) AS QTY_std_variance FROM pallet_masked_fulldata1;
## StdVariance of QTY = 212.70050290263885

### RANGE ####
SELECT MAX(QTY) - MIN(QTY) AS QTY_range
FROM pallet_masked_fulldata1;
# range of QTY = 1140

#######  THIRD MOMENT BUSINESS DECISION / SKEWNESS #######
SELECT
(
SUM(POWER(QTY- (SELECT AVG(QTY) FROM pallet_masked_fulldata1), 3)) /
(COUNT(*) * POWER((SELECT STDDEV(QTY) FROM pallet_masked_fulldata1), 3))
) AS skewness
FROM pallet_masked_fulldata1;
# SKEW of QTY = -0.21399377835270877

######### FOURTH MOMENT BUSINESS DECISION/ KURTOSIS ##########
SELECT
(
(SUM(POWER(QTY- (SELECT AVG(QTY) FROM pallet_masked_fulldata1), 4)) /
(COUNT(*) * POWER((SELECT STDDEV(QTY) FROM pallet_masked_fulldata1), 4))) - 3
) AS kurtosis
FROM pallet_masked_fulldata1;
# KURT of QTY = -0.9177984575625486

####### DATA PREPROCESSING ###### 
### FIND THE NULL VALUES ######
SELECT
COUNT(*) AS total_rows,
SUM(CASE WHEN 'Date' IS NULL THEN 1 ELSE 0 END) AS Date_missing,
SUM(CASE WHEN CustName IS NULL THEN 1 ELSE 0 END) AS CustName_missing,
SUM(CASE WHEN City IS NULL THEN 1 ELSE 0 END) AS City_missing,
SUM(CASE WHEN Region IS NULL THEN 1 ELSE 0 END) AS Region_missing,
SUM(CASE WHEN State IS NULL THEN 1 ELSE 0 END) AS State_missing,
SUM(CASE WHEN 'Product Code' IS NULL THEN 1 ELSE 0 END) AS 'Product Code_missing',
SUM(CASE WHEN 'Transaction Type' IS NULL THEN 1 ELSE 0 END) AS 'Transaction Type_missing',
SUM(CASE WHEN QTY IS NULL THEN 1 ELSE 0 END) AS QTY_missing,
SUM(CASE WHEN WHName IS NULL THEN 1 ELSE 0 END) AS WHName_missing
FROM pallet_masked_fulldata1;
### There is No null Values in the Given dataset i will check each column it returns 0 rows null values

######## UNIQUE VALUES ###########
SELECT DISTINCT `Date` FROM pallet_masked_fulldata1;
# 1608

SELECT DISTINCT CustName FROM pallet_masked_fulldata1;
# 4183

SELECT DISTINCT City FROM pallet_masked_fulldata1;
#696

SELECT DISTINCT Region FROM pallet_masked_fulldata1;
# 4

SELECT DISTINCT State FROM pallet_masked_fulldata1;
# 33

SELECT DISTINCT `Product Code` FROM pallet_masked_fulldata1;
# 70

SELECT DISTINCT `Transaction Type` FROM pallet_masked_fulldata1;
# 2

SELECT DISTINCT QTY FROM pallet_masked_fulldata1;
# 961

SELECT DISTINCT WHName FROM pallet_masked_fulldata1;
# 87

 ######### HANDLING DUPLICATES ##########
##### COUNT DUPLICATES #######
SELECT `Date`,CustName,City,Region,State,
`Product Code`,`Transaction Type`,QTY,WHName,
COUNT(*) AS duplicate_count
FROM pallet_masked_fulldata1
GROUP BY 
`Date`,CustName,City,Region,State,
`Product Code`,`Transaction Type`,QTY,WHName
HAVING COUNT(*) > 1;

### NO.OF DUPLICATES = 11291

#### REMOVE DUPLICATES #####
CREATE TABLE clean_pallet_data AS SELECT DISTINCT * FROM  pallet_masked_fulldata1;
SELECT * FROM clean_pallet_data;

### AFTER REMOVING DUPLICATES COUNT ###
SELECT `Date`,CustName,City,Region,State,
`Product Code`,`Transaction Type`,QTY,WHName,
COUNT(*) AS duplicate_count
FROM clean_pallet_data
GROUP BY 
`Date`,CustName,City,Region,State,
`Product Code`,`Transaction Type`,QTY,WHName
HAVING COUNT(*) > 1;
 ### NO OF DUPLICATES = 0
 
##### OUTLIERS #######
#### Outliers
#### Detection of number of outliers
select count(case when abs((CustName - mean_stats.mean_value) / std_dev_stats.std_dev) > 3 then 1 end)
            as CustName_outliers
from clean_pallet_data
cross join (select avg(CustName) as mean_value from clean_pallet_data) as mean_stats
cross join (SELECT stddev(CustName) as std_dev from clean_pallet_data) as std_dev_stats;

#### outliers in CustName = 0

select count(case when abs((QTY - mean_stats.mean_value) / std_dev_stats.std_dev) > 3 then 1 end)
            as QTY_outliers
from clean_pallet_data
cross join (select avg(QTY) as mean_value from clean_pallet_data) as mean_stats
cross join (SELECT stddev(QTY) as std_dev from clean_pallet_data) as std_dev_stats;

#### Outliers in QTY = 0

select count(case when abs((WHName - mean_stats.mean_value) / std_dev_stats.std_dev) > 3 then 1 end)
            as WHName_outliers
from clean_pallet_data
cross join (select avg(WHName) as mean_value from clean_pallet_data) as mean_stats
cross join (SELECT stddev(WHName) as std_dev from clean_pallet_data) as std_dev_stats;

### Outliers in WhName = 8

##### ZERO VARIANCE AND NEAR ZERO VARIANCE FEATURE ######
SELECT
  VARIANCE(QTY) AS QTY_variance
  FROM clean_pallet_data
HAVING QTY_variance <= 0.01;
# there is no zero and near zero variance 
# the variance of the above used columns variance is high   


###### EDA AFTER DATA PREPROCESSING ##########
##### FIRST MOMENT BUSINESS/MEASURES OF CENTRAL TENDENCY #####
#### MEAN ######
SELECT AVG(QTY) AS mean_QTY FROM clean_pallet_data;
# QTY MEAN = 43.0152

###### MEDIAN #######
SELECT QTY AS Median_QTY
FROM (
SELECT QTY, ROW_NUMBER() OVER (ORDER BY QTY) AS row_num,
COUNT(*) OVER() AS total_count
FROM clean_pallet_data
) AS subquery
WHERE row_num = (total_count + 1)/2 OR row_num 
= (total_count + 2)/2;
## QTY MEDIAN = 100

######### MODE ###########
SELECT QTY AS mode_QTY
FROM (
SELECT QTY, COUNT(*) AS frequency 
FROM clean_pallet_data
GROUP BY QTY
ORDER BY frequency DESC
LIMIT 1
) AS subquery;
### QTY MODE = 100

########### SECOND MOMENT BUSINESS DECISION/MEASURES OF DISPERSION ############
#### VARIANCE #####
SELECT VARIANCE(QTY) AS performance_variance FROM clean_pallet_data;
## VARIANCE OF QTY = 44528.05101544596

######## STANDARD DEVIATION ########
SELECT STDDEV(QTY) AS QTY_std_variance FROM clean_pallet_data;
## StdVariance of QTY = 211.01670790590484

### RANGE ####
SELECT MAX(QTY) - MIN(QTY) AS QTY_range
FROM clean_pallet_data;
# range of QTY = 1140

#######  THIRD MOMENT BUSINESS DECISION / SKEWNESS #######
SELECT
(
SUM(POWER(QTY- (SELECT AVG(QTY) FROM clean_pallet_data), 3)) /
(COUNT(*) * POWER((SELECT STDDEV(QTY) FROM clean_pallet_data), 3))
) AS skewness
FROM clean_pallet_data;
# SKEW of QTY = -0.17298168861613322

######### FOURTH MOMENT BUSINESS DECISION/ KURTOSIS ##########
SELECT
(
(SUM(POWER(QTY- (SELECT AVG(QTY) FROM clean_pallet_data), 4)) /
(COUNT(*) * POWER((SELECT STDDEV(QTY) FROM clean_pallet_data), 4))) - 3
) AS kurtosis
FROM clean_pallet_data;
# KURT of QTY = -0.8636504387372224



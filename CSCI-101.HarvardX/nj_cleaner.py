'''
I-101 Foundations of Data Science and Engineering
Term: 2022 Summer
PSET #4: Managing Data Exercise 2
Name: Roger W Zeng
'''

import pandas as pd 
import numpy as np 
import mysql.connector as sql

# submssion flag, set to False in dev and unit testing
submission = True

# dictionary of column types to be used later
col_dtypes = {'last_name': str, 'first_name': str, 'county': str, 'district': str, 'school': str, 'primary_job': str, 'fte': float, 'salary': int, 'certificate': str, 'subcategory': str, 'teaching_route': str,	'highly_qualified': str, 'experience_district': int, 'experience_nj': int, 'experience_total': int}

if submission:
    df = pd.read_csv('/autograder/source/nj_state_teachers_salaries.csv', on_bad_lines="warn", index_col=None, header=0, skipinitialspace=True)    # submission spec
else: 
    df = pd.read_csv('nj_state_teachers_salaries.csv', on_bad_lines="warn", index_col=None, header=0, skipinitialspace=True)  # unit test spec
    print(f"Read in {len(df)} rows and {len(df.columns)} columns")

# drop rows if all elements are blank
df.dropna(how="all", inplace = True)

# check for invalid integer numbers
for i, j in col_dtypes.items():
    if j == int:
        df[i] = df[i].replace('[^0-9]', np.NaN, regex=True)
    elif j == float:
        df[i] = df[i].replace('[^0-9.]', np.NaN, regex=True)

# drop NaN records
df.dropna(how="any", inplace = True)

if not submission:
    df.to_csv('/autograder/submission/nj_state_teachers_salaries.csv', index=False)  # submission spec
else:
    print(df.head())
    print(f"Clean Dataframe is {len(df)} rows and {len(df.columns)} columns")
    df.to_csv('nj_state_teachers_salaries_cleaned.csv', index=False)  # unit test spec


# open connection to mySQL
if submission:
    mydb = sql.connect(host="localhost", user="User", passwd="password", buffered=True)  # submission spec
else:
    mydb = sql.connect(host="localhost", user="root", passwd="", buffered=True)  # unit test spec

mycursor = mydb.cursor()

# create database schema and table
mycursor.execute("create schema nj_state_teachers_salaries;")
mycursor.execute("use nj_state_teachers_salaries;")
tbCreate = "create table nj_state_teachers_salaries (last_name VARCHAR(45) NOT NULL, first_name VARCHAR(45) NOT NULL,	county VARCHAR(45) NOT NULL,	district VARCHAR(100) NOT NULL,	school VARCHAR(100) NOT NULL,	primary_job TEXT NOT NULL,	fte FLOAT NOT NULL,	salary INT NOT NULL,	certificate	VARCHAR(45) NOT NULL, subcategory VARCHAR(32) NOT NULL,	teaching_route  VARCHAR(32) NOT NULL,	highly_qualified VARCHAR(100) NOT NULL,	experience_district INT NOT NULL,	experience_nj INT NOT NULL,	experience_total INT NOT NULL);"

mycursor.execute(tbCreate)

# load data from csv file into database table
if submission: 
    loadData = "LOAD DATA INFILE '/autograder/nj_state_teachers_salaries.csv' INTO TABLE nj_state_teachers_salaries FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;"  # submission spec
else:
    loadData = "LOAD DATA INFILE '/var/lib/mysql-files/nj_state_teachers_salaries_cleaned.csv' INTO TABLE nj_state_teachers_salaries FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;"  # unit test spec

mycursor.execute(loadData)

# Commit DB transactions
mydb.commit()

# Verify the # of records loaded into SQL DB table
mycursor.execute("select count(*) from nj_state_teachers_salaries;")

if not submission:
        print(f"Loaded {mycursor[0]} records into 'nj_teachers_salaries' table")

# Conclude DB transaction
mydb.close()


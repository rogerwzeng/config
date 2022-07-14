'''
CSCI-101 Foundations of Data Science and Engineering
Term: 2022 Summer
PSET #3: Managin Data - Load Salary Data
Name: Roger W Zeng
'''

import mysql.connector as sq

# open connection to mySQL
mydb = sq.connect(host="localhost", user="root", passwd="", buffered=True)  # unit test spec
#mydb = sq.connect(host="localhost", user="User", passwd="password", buffered=True)  # submission spec

mycursor = mydb.cursor()

# create database schema and table
mycursor.execute("create schema nj_state_teachers_salaries_cls;")
mycursor.execute("use nj_state_teachers_salaries_cls;")
tbCreate = "create table nj_state_teachers_salaries (last_name VARCHAR(45) NOT NULL, first_name VARCHAR(45) NOT NULL,	county VARCHAR(45) NOT NULL,	district VARCHAR(100) NOT NULL,	school VARCHAR(100) NOT NULL,	primary_job TEXT NOT NULL,	fte FLOAT NOT NULL,	salary INT NOT NULL,	certificate	VARCHAR(45) NOT NULL, subcategory VARCHAR(32) NOT NULL,	teaching_route  VARCHAR(32) NOT NULL,	highly_qualified VARCHAR(100) NOT NULL,	experience_district INT NOT NULL,	experience_nj INT NOT NULL,	experience_total INT NOT NULL);"

mycursor.execute(tbCreate)

# load data from csv file into database table
loadData = "LOAD DATA INFILE '/var/lib/mysql-files/nj_teachers_salaries_cls.csv' INTO TABLE nj_state_teachers_salaries FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;"  # unit test spec
#loadData = "LOAD DATA INFILE '/autograder/nj_teachers_salaries_cls.csv' INTO TABLE nj_state_teachers_salaries FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;"  # submission spec

mycursor.execute(loadData)

# Commit DB transactions
mydb.commit()

# Verify the # of records loaded into SQL DB table
mycursor.execute("select count(*) from nj_state_teachers_salaries;")

# Unit test spec
for i in mycursor:
    print(f"Loaded {i[0]} records into 'nj_teachers_salaries' table")

# Conclude DB transaction
mydb.close()

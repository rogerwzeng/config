'''
HarvardX Summer 2022
CSCI-101: Foundations of Data Science and Engineering
Module 4 Python Managing Data Practice Worksheet
Name: Roger Zeng
'''

import pandas as pd
import QCTestString as qt

df = pd.read_excel('QCTest.xlsx', sheet_name="Sheet1", index_col=None,na_values="NA", header=0)

# Add the validity of the QC test string for each plant
df['isValid'] = df['TestResults'].apply(lambda x: 'yes' if qt.isValidString(str(x)) == True else 'no')

print(df.loc[df['isValid'] == 'no'])

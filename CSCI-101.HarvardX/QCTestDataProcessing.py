'''
HarvardX Summer 2022
CSCI-101: Foundations of Data Science and Engineering
Module 4 Python Managing Data Practice Worksheet
Name: Roger Zeng
'''

import pandas as pd
import QCTestString as qt

df = pd.read_excel('QCTest.xlsx', sheet_name="Sheet1", index_col=None,na_values="NA", header=0)

# Validate the QC test string for each plant and add stats cols
ds = df['TestResults'].apply(lambda x: qt.isValidString(str(x))).to_frame()
# df[['isValid', 'TotalTests', 'Pass', 'Defect']] = df['TestResults'].apply(lambda x: qt.isValidString(str(x))).to_frame()

# Convert to Dataframe
dfa = pd.DataFrame(ds['TestResults'].tolist(), columns=['isValid', 'TotalTests', 'Pass','Defect'])

# Adjust status col
dfa['isValid'] = dfa['isValid'].apply(lambda x: 'yes' if x else 'no')

# Done
df = df.join(dfa)

print(df.head())
print(df.loc[df['isValid'] == 'no'])

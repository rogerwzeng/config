'''
HarvardX Summer 2022
CSCI-101: Foundations of Data Science and Engineering
Module 4 Python Managing Data Practice Worksheet
Name: Roger Zeng
'''

import pandas as pd
import QCTestString as qt

df = pd.read_excel('QCTest.xlsx', index_col=None, na_values="NA", header=0)

# Validate the QC test string for each plant and add stats cols
ds = df['TestResults'].apply(lambda x: qt.isValidString(str(x)))

# Convert Series to Dataframe
dfa = pd.DataFrame(ds.tolist(), columns=['isValid', 'TotalTests', 'Pass', 'Defect'])

# Adjust status col
dfa['isValid'] = dfa['isValid'].apply(lambda x: 'yes' if x else 'no')

# Merge with original table 
df = df.join(dfa)

# print(df.head())
# print(df.loc[df['isValid'] == 'no'])

# Save results to file and Done!
df.to_excel('QCTestResults.xlsx', index=False)

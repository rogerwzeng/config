'''
I-101 Foundations of Data Science and Engineering
Term: 2022 Summer
PSET #5: Exploratory Data Analysis
Name: Roger W Zeng
'''

import pandas as pd


def CleanColumnHeading(dfx):
    '''
    function to:
        1. convert all column heading to lower case
        2. convert all space in column names to '_'
    '''
    cols_from = dfx.columns
    cols_to = [x.strip().lower().replace(' ', '_') for x in cols_from]
    
    cols_dict = dict(zip(cols_from, cols_to))

    dfx.rename(columns=cols_dict)
    
    return dfx


def StandardizeColNames(df):
    '''
    function to:
        1. columns contain zipcodes are named 'zip'
        2. colunms contain city names are named 'city'
        3. columns contain states are named 'state'
    '''
    cols = df.columns
    for i in cols:
        if i.find('zip') >= 0:
            df.rename(columns={i:'zip'})
        if i.find('city') >= 0:
            df.rename(columns={i:'city'})
        if i.find('state') >= 0:
            df.rename(columns={i:'state'})

    return df


def CleanQCTest(df_test):
    # Validate the QC test string for each plant and add stats cols
    ds = df_test['TestResults'].apply(lambda x: isValidString(str(x)))

    # Convert Series to Dataframe
    dfa = pd.DataFrame(ds.tolist(), columns=['isValid', 'TotalTests', 'Pass', 'Defect'])

    # Adjust status col
    dfa['isValid'] = dfa['isValid'].apply(lambda x: 'yes' if x else 'no')

    # Merge with original table 
    df = df_test.join(dfa)

    return df


def isValidString(s):
    '''
    Function to verify the validity of the test result string
    '''

    isValid = True
    total_p = 0
    total_d = 0

    # Some initial sanity checks
    if not s.startswith('Q'):
        isValid = False
        return [isValid, (total_p + total_d), total_p, total_d]

    # Parse all QC batches in a single line record
    tests = s.split("Q")

    # The first one is alway null, remove
    tests.remove('')

    # Loop through all QC batches
    for i in tests:
        #Validate in text form first
        txtValid, Q, p, d = parseNumsTxt(i)
        if not txtValid:
            isValid = False
            return [isValid, (total_p + total_d), total_p, total_d]

        #Now validate the numbers
        numValid, inc_p, inc_d = numsValid(Q, p, d)  
        if not numValid:
            isValid = False
            return [isValid, (total_p + total_d), total_p, total_d]
        else:
            total_p += inc_p
            total_d += inc_d
            
    return [isValid, (total_p + total_d), total_p, total_d]

# function call by isValidString() to parse Q p d as strings
# includes string level validity checks 
def parseNumsTxt(case):

    # Check that both p and d are present
    if 'p' not in case or 'd' not in case:
        return False, -1, -1, -1

    # get position of p and d
    idx_p = case.find('p')
    idx_d = case.find('d')

    # Parse the number of Q, pass and defective cases
    if idx_p > idx_d:  # d appears first after Q
        txt_Q = case[0:idx_d]
        txt_d = case[(idx_d+1):idx_p]
        txt_p = case[(idx_p+1):].strip('\n')
    else:  # p appears first after Q
        txt_Q = case[0:idx_p]
        txt_d = case[(idx_d+1):].strip('\n')
        txt_p = case[(idx_p+1):idx_d]

    # string parsing successful, return values
    return True, txt_Q, txt_p, txt_d

# function to verify the validity of p d and Q as numbers
# includes numeric validity checks
def numsValid(txt_Q, txt_p, txt_d):


    for i in [txt_Q, txt_p, txt_d]:
        # See if all of the numbers are numeri
        if i.isdecimal() is False:
            return [False, 0, 0]
        # See if there is any leading zero
        if i[0] == '0' and len(i.strip()) > 1:
            return [False, 0, 0]

    # Passes all tests, convert to numbers
    Q = int(txt_Q.strip())
    p = int(txt_p.strip())
    d = int(txt_d.strip())

    # See if it's a empty batch
    if Q == 0:
        return [False, 0, 0]
    # See if the total adds up
    if Q != p + d:
        return [False, 0, 0]
    
    # All tests passed, this QA batch is valid
    return [True, p, d]


# main function of bigtest
def main():
    # submssion flag, set to False in dev and unit test
    submission = False

    if submission:
        subdir = '/autograder/source/'
    else:
        subdir = ''

    # load QC results data
    df_test = pd.read_csv(subdir + 'QCTest.csv', on_bad_lines='skip', \
            index_col=None, header=0, skipinitialspace=True)

    # load zip data
    load_cols = ['Zip Code', 'Primary City', 'STATE', 'IRS Estimated population']
    df_zip = pd.read_csv(subdir + 'zip_code_database.csv',
            on_bad_lines='skip', usecols = load_cols,
            index_col=None, header=0, skipinitialspace=True)

    # load defects by state data
    df_defects = pd.read_csv(subdir + 'defect_returns_by_state.csv',
            on_bad_lines='skip', index_col=None, header=0,
            skipinitialspace=True) 

    # clean and standardize column headings
    for df in [df_test, df_zip, df_defects]:
        df = CleanColumnHeading(df)
        df = StandardizeColNames(df)

    # clean up QC test results
    df_test = CleanQCTest(df_test)


    # merge into final data frame
    df_new = df_test.merge(df_zip)
    df_new = df.new.merge(df_defects)

    # result output variables
    defect_result = df_new[df['defects'] > 8000]['state']
    pass_result = df_new[df['pass'] > 10]['city']
    pop_result = df_new[(df['pass'] > 10) & ( df['defects'] > 10000) & \
            (df['irs_estimated_population'] > 30000)]['plant']

    if not submission:
        print(f"defect result: {defect_result}")
        print(f"pass result: {pass_result}")
        print(f"pop result: {pop_result}")


if __name__ == '__main__':
    main()

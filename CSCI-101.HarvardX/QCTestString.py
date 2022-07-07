'''
CSCI-101 Foundations of Data Science and Engineering
Term: 2022 Summer
PSET #2: String Data Manipulation
Name: Roger W Zeng
'''

# main function called 
def isValidString(s):

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

# main program used to call isValidString()
if __name__ == "__main__":

    ## read in string test cases
    f=open('testcases.txt', 'r')
    for x in f:
        print(f"{isValidString(x)} QC case |{x[:-1]}|")


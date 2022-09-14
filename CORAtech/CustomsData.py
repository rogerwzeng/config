# 利用 ASN 文件内容，获得本批货品的产品资料，然后翻译成中文
#
import subprocess
import pandas as pd
from python_translator import Translator

import vars

# START JOB #
# import product meta data 
# 
# Product info for Customs declaration purposes
df_mat = pd.read_excel(vars.meta_dir+vars.season_dir+'F22materialsENG.xlsx', 
                       header=0, index_col=0, usecols="A,C,D,L,S")
# Product care information
df_care = pd.read_excel(vars.meta_dir+vars.season_dir+'F22materialsENG.xlsx',
        sheet_name=2, index_col=0, header=0, usecols="A,B,D,G:R")

df_mat = df_mat.merge(df_care.drop('Product Name', axis=1), 
        how='left', on='Style Number')

# short column names
df_mat.columns = vars.col_names

if vars.debug:
    print(df_mat.columns, df_mat.nunique())

# standard ASN columns, used for checking conformity of incoming files
asn_std_cols = ['Date Shipped From our DC', 'Our Order Number', 'Our Pick Number',
       'Style Number', 'Shipped Color', 'Qty Shipped', 'Shipped Size Desc',
       'SKU Reference', 'Our UPC Code']

# Load all ASN files in the asn directory
files = subprocess.run(['ls', vars.asn_dir+vars.season_dir], 
                           stdout=subprocess.PIPE, 
                           stderr=subprocess.PIPE, 
                           universal_newlines=True)

filelist = files.stdout.split('\n')
filelist.pop()  # delete last empty item

# Load all ASN files into one data frame
df_asn = pd.DataFrame()
for i in filelist:
    dft = pd.read_excel(vars.asn_dir+vars.season_dir+i, header=0, parse_dates=True)
    try:
        assert(list(dft.columns) == asn_std_cols)
    except AssertionError:
        print(f"ERROR: Invlid input file format {asn_dir+i}")
    df_asn = pd.concat([df_asn, dft], axis=0, ignore_index=True)

if vars.debug:
    print(f"ASN data size = {df_asn.shape}")
    print(f"Total shipped = {df_asn['Qty Shipped'].sum()}")

# Simplify column names
df_asn.columns = ['ShipDate', 'Order#', 'Pick#', 'Style', 'Color', 
        'QTY', 'Size', 'Product', 'UPC']

df_asn.drop(['ShipDate', 'Order#', 'Pick#'], axis=1, inplace=True)

# dumb way to convert Style data type to string
df_asn['存货编码'] = df_asn['Style'].apply(lambda x: str(x))  
df_asn['存货编码'] += df_asn['Color'] + df_asn['Size']

# merged with product meta data
df = df_asn.merge(df_mat.drop('Product', axis=1), how='left', on='Style')

# Call Google translate API
translator = Translator() 

# translate the above fields
for label in vars.to_trans:
    if vars.debug:
        print(f"Translating {label}...")

    uniques = list(df[label].unique())
    uniques_denan = [i for i in uniques if not(pd.isnull(i))]

    if uniques_denan != []:
        trans = [translator.translate(x, "chinese") for x in uniques_denan]
        for value in trans:
            df.loc[df[label] == value.original_text, label+'中文'] = value.new_text


if vars.debug:
    print(df.nunique())
    print(f"Print output to file {vars.out_dir+vars.season_dir+vars.merged_file_name}")

# write intermediate step with rough machine translation
with pd.ExcelWriter(vars.out_dir+vars.season_dir+vars.merged_file_name) as writer:
    df.to_excel(writer, index=False, engine='openpyxl')


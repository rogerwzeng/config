
### some preliminaries

# dev switch, turn off in production
debug = True

# file structure for various data files
batch_code  = 'F22-2'
season_dir = ''   # define as needed
meta_dir = '/mnt/d/CORAtech/meta/'  # persistent product data
asn_dir = '/mnt/d/CORAtech/'+ batch_code +'asn/'  # shipment specific data
out_dir = '/mnt/d/CORAtech/out/'  # output files
 
# meta files
materials = 'F22materialsENG.xlsx'
lookup_table1 = 'lookuptb1.xlsx'

# Change the columns to be easier to handle
col_names = ['Style', 'Product', 'COO', 'Material', 'Loc1', 'Lab1',
        'Loc2', 'Lab2', 'Loc3', 'Lab3',
        'Loc4', 'Lab4', 'Loc5', 'Lab5', 'Loc6', 'Lab6']

# fields to translate
to_trans = ['COO', 'Material', 'Loc1', 'Lab1',
        'Loc2', 'Lab2', 'Loc3', 'Lab3',
        'Loc4', 'Lab4', 'Loc5', 'Lab5', 'Loc6', 'Lab6']

# Output Custom declaration data file
merged_file_name = 'MergedCustomsData.xlsx'
final_file_name = batch_code + 'ASN翻译中文资料.xlsx'


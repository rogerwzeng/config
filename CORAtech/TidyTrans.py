# Clean up translation

import pandas as pd
import re

import vars


# import the save intermeidate file, and the lookup table
df_trans = pd.read_excel(vars.out_dir+vars.season_dir+vars.merged_file_name, header=0)
df_lookup1 = pd.read_excel(vars.meta_dir+vars.season_dir+vars.lookup_table1, header=0)

# find which Chinese headers are present
sel = ['中文' in x for x in list(df_trans.columns)]

if vars.debug:
    print(f"Customs Data Table Size: {df_trans.shape}")
    print(f"中文翻译的字段：{df_trans.columns[sel]}")

for i, row in df_lookup1.iterrows():
    if row['Trans1'] == '':
        continue
    else:
        for i in df_trans.columns[sel]:
            df_trans[i] = df_trans[i].apply(lambda x: re.sub(str(row['Trans1']), str(row['Correct']), str(x)))

if vars.debug:
    print(f"Print output to file {vars.out_dir+vars.season_dir+vars.final_file_name}")

with pd.ExcelWriter(vars.out_dir+vars.season_dir+vars.final_file_name) as writer:
    df_trans.to_excel(writer, index=False, engine='openpyxl')

import os
import pandas as pd
import itertools
import locale


#SETUP
cd = os.path.join(os.path.expanduser("~"),r'Documents',r'projects',r'origin_destination')
cd_dotdot = os.path.join(os.path.expanduser("~"),r'Documents',r'projects')
locale.setlocale(locale.LC_NUMERIC, '')

#LOAD
raw_data_filepath = os.path.join(cd,r'origin_destination_files',r'Copy of O-D Geography by Mode_final version as of 10_14_11.xlsx')
raw_data = pd.read_excel(raw_data_filepath,skiprows=[0])
raw_data = raw_data.head(-1)
#millions of $ for value,1000s for tons, millions for ton-miles
raw_data.columns = ['orig_state','orig_cfs','dest_state','dest_cfs', \
                    'mode','value','tons','ton_miles','value_cv', \
                    'tons_cv','ton_miles_cv','NA']
raw_data = raw_data[['orig_state','orig_cfs','dest_state','dest_cfs', \
                    'mode','value']]
#drop Alaska and Hawaii
raw_data = raw_data[~(raw_data['orig_state'] == 'AK') & \
                    ~(raw_data['orig_state'] == 'HI') & \
                    ~(raw_data['dest_state'] == 'AK') & \
                    ~(raw_data['dest_state'] == 'HI') & \
                    ~(raw_data['dest_state'] == '-')]
#drop non-CFS areas
raw_data['first_nine_orig'] = raw_data['orig_cfs'].str[:9]
raw_data['last_five_orig'] = raw_data['orig_cfs'].str[-5:]
raw_data = raw_data[(raw_data['first_nine_orig'] == 'Remainder') | \
                    (raw_data['last_five_orig'] == ' Area') | \
                    (raw_data['last_five_orig'] == 'part)') | \
                    (raw_data['orig_cfs'] == 'Arkansas') | \
                    (raw_data['orig_cfs'] == 'Delaware') | \
                    (raw_data['orig_cfs'] == 'Idaho') | \
                    (raw_data['orig_cfs'] == 'Iowa') | \
                    (raw_data['orig_cfs'] == 'Maine') | \
                    (raw_data['orig_cfs'] == 'Mississippi') | \
                    (raw_data['orig_cfs'] == 'Montana') | \
                    (raw_data['orig_cfs'] == 'Nebraska') | \
                    (raw_data['orig_cfs'] == 'New Hampshire') | \
                    (raw_data['orig_cfs'] == 'New Mexico') | \
                    (raw_data['orig_cfs'] == 'North Dakota') | \
                    (raw_data['orig_cfs'] == 'South Dakota') | \
                    (raw_data['orig_cfs'] == 'Vermont') | \
                    (raw_data['orig_cfs'] == 'West Virginia') | \
                    (raw_data['orig_cfs'] == 'Wyoming')]
del raw_data['first_nine_orig']
del raw_data['last_five_orig']
raw_data['first_nine_dest'] = raw_data['dest_cfs'].str[:9]
raw_data['last_five_dest'] = raw_data['dest_cfs'].str[-5:]
raw_data = raw_data[(raw_data['first_nine_dest'] == 'Remainder') | \
                    (raw_data['last_five_dest'] == ' Area') | \
                    (raw_data['last_five_dest'] == 'Area ') | \
                    (raw_data['last_five_dest'] == 'Part)') | \
                    (raw_data['dest_cfs'] == 'Arkansas') | \
                    (raw_data['dest_cfs'] == 'Delaware') | \
                    (raw_data['dest_cfs'] == 'Idaho') | \
                    (raw_data['dest_cfs'] == 'Iowa') | \
                    (raw_data['dest_cfs'] == 'Maine') | \
                    (raw_data['dest_cfs'] == 'Mississippi') | \
                    (raw_data['dest_cfs'] == 'Montana') | \
                    (raw_data['dest_cfs'] == 'Nebraska') | \
                    (raw_data['dest_cfs'] == 'New Hampshire') | \
                    (raw_data['dest_cfs'] == 'New Mexico') | \
                    (raw_data['dest_cfs'] == 'North Dakota') | \
                    (raw_data['dest_cfs'] == 'South Dakota') | \
                    (raw_data['dest_cfs'] == 'Vermont') | \
                    (raw_data['dest_cfs'] == 'West Virginia') | \
                    (raw_data['dest_cfs'] == 'Wyoming')]
del raw_data['first_nine_dest']
del raw_data['last_five_dest']
raw_data.loc[(raw_data['value'] == 'S'), 'value'] = 0
raw_data.loc[(raw_data['value'] == 'Z'), 'value'] = 0

#list of unique cfs areas
unique_orig = raw_data[['orig_state','orig_cfs']]
unique_orig = unique_orig.drop_duplicates(subset=['orig_state','orig_cfs'])
unique_dest = raw_data[['dest_state','dest_cfs']]
unique_dest = unique_dest.drop_duplicates(subset=['dest_state','dest_cfs'])
unique_dest.columns = ['orig_state','orig_cfs']
unique = unique_orig.append(unique_dest)
unique.columns = ['state','cfs']
unique = unique.drop_duplicates(subset=(['state','cfs']))
unique.to_csv('unique_cfs.csv',index=False)

#import cfs with codes
cfs_code_map = pd.read_csv('unique_cfs_mapped.csv')
cfs_code_map['cfs_code'] = cfs_code_map['cfs_code'].apply(str)
states_w_leading_zero = ['AL','AZ','AR','CA','CO','CT']
for st in states_w_leading_zero:
    cfs_code_map.loc[(cfs_code_map['state'] == st), 'cfs_code'] = '0' + cfs_code_map['cfs_code']
#all combinations
code_list = cfs_code_map['cfs_code'].unique().tolist()
all_comb = []
for code1 in code_list:
    for code2 in code_list:
        all_comb.append((code1,code2))
comb_df = pd.DataFrame(all_comb)
comb_df.columns = ['orig_cfs_code','dest_cfs_code']
comb_df = comb_df[~(comb_df['orig_cfs_code'] == comb_df['dest_cfs_code'])]

#fill in all pairs of trade values
#bring in codes
raw_data = raw_data.rename(columns={'orig_state':'state','orig_cfs':'cfs'})
raw_data = pd.merge(raw_data,cfs_code_map,on=['state','cfs'],how='inner')
raw_data = raw_data[['state','cfs','cfs_code','dest_state','dest_cfs','mode','value']]
raw_data = raw_data.rename(columns={'state':'orig_state','cfs':'orig_cfs','cfs_code':'orig_cfs_code'})
raw_data = raw_data.rename(columns={'dest_state':'state','dest_cfs':'cfs'})
raw_data = pd.merge(raw_data,cfs_code_map,on=['state','cfs'],how='inner')
raw_data = raw_data[['orig_state','orig_cfs','orig_cfs_code','state','cfs','cfs_code','mode','value']]
raw_data = raw_data.rename(columns={'state':'dest_state','cfs':'dest_cfs','cfs_code':'dest_cfs_code'})
clean_data = raw_data[['orig_cfs_code','dest_cfs_code','mode','value']].copy()
clean_data = clean_data.pivot(index=['orig_cfs_code','dest_cfs_code'],columns='mode',values='value')
clean_data.reset_index(inplace=True)
clean_data = clean_data.fillna(0)
clean_data['truck'] = clean_data['Truck (3)']
clean_data['rail'] = clean_data['Rail'] + clean_data['Truck and rail'] + (clean_data['Rail and water']/2)
clean_data['water'] = clean_data['Water'] + clean_data['Truck and water'] + (clean_data['Rail and water']/2)
clean_data['air'] = clean_data['Air (includes truck and air)']
clean_data = clean_data[['orig_cfs_code','dest_cfs_code','truck','rail','water','air']]
clean_data = clean_data[~(clean_data['orig_cfs_code'] == clean_data['dest_cfs_code'])]

#combine with total
comb_data = pd.merge(comb_df,clean_data,on=['orig_cfs_code','dest_cfs_code'],how='left')
comb_data = comb_data.fillna(0)
comb_data.to_csv('trade_data.csv',index=False)






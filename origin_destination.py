import os
import pandas as pd

#SETUP
cd = os.path.join(os.path.expanduser("~"),r'Documents',r'projects',r'origin_destination')
cd_dotdot = os.path.join(os.path.expanduser("~"),r'Documents',r'projects')

#LOAD
raw_data_filepath = os.path.join(cd,r'origin_destination_files',r'Copy of O-D Geography by Mode_final version as of 10_14_11.xlsx')
raw_data = pd.read_excel(raw_data_filepath,skiprows=[0])
raw_data = raw_data.head(-1)
#millions of $ for value,1000s for tons, millions for ton-miles
raw_data.columns = ['orig_state','orig_cfs','dest_state','dest_cfs', \
                    'mode','value','tons','ton_miles','value_cv', \
                    'tons_cv','ton_miles_cv','NA']
raw_data = raw_data[['orig_state','orig_cfs','dest_state','dest_cfs', \
                    'mode','value','tons']]
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
                    (raw_data['last_five_orig'] == 'part)')]
del raw_data['first_nine_orig']
del raw_data['last_five_orig']
raw_data['first_nine_dest'] = raw_data['dest_cfs'].str[:9]
raw_data['last_five_dest'] = raw_data['dest_cfs'].str[-5:]
raw_data = raw_data[(raw_data['first_nine_dest'] == 'Remainder') | \
                    (raw_data['last_five_dest'] == ' Area') | \
                    (raw_data['last_five_dest'] == 'part)')]
del raw_data['first_nine_dest']
del raw_data['last_five_dest']
raw_data = raw_data[(raw_data['mode'] == 'Truck (3)') | \
                    (raw_data['mode'] == 'Rail') | \
                    (raw_data['mode'] == 'Air (includes truck and air)') | \
                    (raw_data['mode'] == 'Water')]


#how many non zeros in AA14's data?


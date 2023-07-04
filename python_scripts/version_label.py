
import pandas as pd
import numpy as np
import re
from packaging.version import Version, parse
from packaging.version import parse, Version
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)


df=pd.read_csv('imptemp.csv',encoding='utf-8')
df = df.sort_values(by=['api_spec_id','commit_date'], ascending=True)
df.dropna(inplace=True)

version_pattern = r'^([1-9][0-9]*!)?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))*((a|b|rc)(0|[1-9][0-9]*))?(\.post(0|[1-9][0-9]*))?(\.dev(0|[1-9][0-9]*))?$'

# Group the data by "api_spec_id"
groups = df.groupby('api_spec_id')

valid_rows = []
invalid_rows = []

# Iterate over the groups
for group_id, group_data in groups:
    # Apply the version pattern to the "info_version" column of the group
    valid_rows_group = group_data['info_version'].str.contains(version_pattern)
    
    # If all the "info_version" fields match the pattern, add the group to the valid_rows list
    if valid_rows_group.all():
        valid_rows.append(group_data)
    else:
        # Otherwise, add the group to the invalid_rows list
        invalid_rows.append(group_data)

# Concatenate the valid and invalid rows for all groups into a single DataFrame
valid_df = pd.concat(valid_rows)
invalid_df = pd.concat(invalid_rows)


# Define the regular expression pattern
pat = r'(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)(?:\.(?P<micro>\d+))?'

sem = valid_df['info_version'].str.extract(pat).fillna(0).astype(int)
diff = sem.groupby(valid_df['api_spec_id']).diff().fillna(0).ne(0)
 
# Assign the labels to each row based on the diff values
valid_df['label'] = diff.dot(sem.columns + '.').str.rstrip('.')


attrs = ['major', 'minor', 'micro', 'pre', 'post', 'dev', 'local']
def extract_version(ver):
    ver = Version(ver)  
    return pd.Series({attr: getattr(ver, attr) for attr in attrs}, dtype=str)


sem = valid_df['info_version'].agg(extract_version).fillna('').rename(columns={'micro': 'patch'})
diff = (sem.groupby(valid_df['api_spec_id'], group_keys=False)
           .apply(lambda x: x.ne(x.shift().fillna(x.iloc[0]))))

valid_df['label'] = diff.dot(sem.columns + '.').str.rstrip('.')


# Split invalid versions dataframe
unparsed = pd.DataFrame(columns=invalid_df.columns)

# iterate over rows and parse versions
for index, row in invalid_df.iterrows():
    try:
        # parse version
        version = parse(row['info_version'])
        # add parsed version to dataframe
        unparsed = unparsed.append(row)
    except:
        # ignore unparsable versions
        pass


pat = r'(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)(?:\.(?P<micro>\d+))?'

sem = unparsed['info_version'].str.extract(pat).fillna(0).astype(int)
diff = sem.groupby(unparsed['api_spec_id']).diff().fillna(0).ne(0)

unparsed['label'] = diff.dot(sem.columns + '.').str.rstrip('.')

attrs = ['major', 'minor', 'micro', 'pre', 'post', 'dev', 'local']
def extract_version(ver):
    ver = Version(ver)  
    return pd.Series({attr: getattr(ver, attr) for attr in attrs}, dtype=str)


sem = unparsed['info_version'].agg(extract_version).fillna('').rename(columns={'micro': 'patch'})
diff = (sem.groupby(unparsed['api_spec_id'], group_keys=False)
           .apply(lambda x: x.ne(x.shift().fillna(x.iloc[0]))))

unparsed['label'] = diff.dot(sem.columns + '.').str.rstrip('.')

# Define dataframe for unparsable versions
remain= invalid_df[~invalid_df.isin(unparsed)].dropna(how = 'all')

regex='^(?:v)?(?P<major>\d+)(?P<pre>[a-zA-Z]+\d+)?(?:\.(?P<minor>\d+))?(?:\.(?P<patch>\d+))?(?:-(?P<suffix>SNAPSHOT))?$'
sem = remain['info_version'].str.extract(regex).fillna(0).apply(pd.to_numeric, errors='coerce')
diff = sem.groupby(remain['api_spec_id']).diff().fillna(0).ne(0)
remain['label'] = diff.dot(sem.columns + '.').str.rstrip('.')

# Concatenation of all the dataframes
final_api = pd.concat([valid_df, unparsed, remain], axis=0)



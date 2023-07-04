import pandas as pd
from pymongo import MongoClient
import numpy as np
import ast
import re

mongo_client = MongoClient('localhost', 27017)
db=mongo_client['api_ace_db_dev']
col=db['versioned-collection']
cursor=col.find( )

df=pd.DataFrame(list(cursor))

df.drop(['_id','api_spec','api_title','bundled_at','oas_version','bump_diff','file_present','oas_version','processed_at','version_location','sha','valid','version_formats_classification','version_catergory','version_path' ], axis=1, inplace=True)

extract_info_version = lambda row: row['extracted_versions']['info_version']

# Apply the lambda functions to create new columns in the dataframe
df['info_version'] = df.apply(extract_info_version, axis=1)

df['diff'] = df['diff'].astype(str)
df['diff'] = df['diff'].apply(lambda x: ast.literal_eval(x))

def try_get(obj, *keys, defaultVal=None):
    try:
        for k in keys: obj = obj[k]
        return obj
    except: return defaultVal

kSep = '.' 
extractKeys = [ ('info', 'version'),
                ('info', 'title'),
                ('info', 'description'),
                ('info', 'contact', 'name'),
                ('info', 'contact', 'url'),
                ('info', 'contact', 'email'),
                ('info', 'license', 'name'),
                ('info', 'license', 'url'),
                ('info', 'termsOfService'),

                ('servers','added'),
                ('servers', 'deleted'),
                ('servers', 'modified'),

                ('paths', 'modified'), 
                ('paths', 'added'),
                ('paths', 'deleted'),         

                ('endpoints', 'added'),
                ('endpoints', 'deleted'),
                ('endpoints', 'modified'),
                
                ('components', 'securitySchemes', 'added'),
                ('components', 'securitySchemes', 'deleted'),
                ('components', 'securitySchemes', 'modified'),
                ('components', 'securitySchemes', 'removed'),
                ('components', 'headers', 'added'),
                ('components', 'headers', 'deleted'),
                ('components', 'links', 'added'),
                ('components', 'links', 'deleted'),
                ('components', 'parameters', 'added'),
                ('components', 'parameters', 'deleted'),
                ('components', 'responses', 'added'),
                ('components', 'responses', 'deleted'),
                ('components', 'schemas', 'added'), 
                ('components', 'schemas', 'deleted'),
                ('components', 'requestBodies', 'added'),
                ('components', 'requestBodies', 'deleted'),

                ('tags', 'added'),
                ('tags', 'deleted'),
                ('tags', 'modified'),

                ('security', 'added'),
                ('security', 'deleted'),
                ('security', 'modified'),

                ('externalDocs', 'added'),
                ('externalDocs', 'deleted')
                

                 ]
for kl in extractKeys:
    df[kSep.join(kl)] = df['diff'].map(lambda d: try_get(d, *kl))

# for column Info Contact Name changes
def count_changes(x):
    if x is None:
        return 0
    else:
        return 1     

# apply the custom function to the 'info.contact.name' column and create a new 'changes' column
df['Info_contact_name_changes'] = df['info.contact.name'].apply(count_changes)

# for column server modified
urls_column = df['servers.modified']

# loop through each row in the column
for i, url_dict in enumerate(urls_column):
    # initialize a count variable for this row
    count = 0
    # check if the dictionary is not None
    if url_dict is not None:
        for url in url_dict.keys():
            # find all occurrences of URLs using a regular expression pattern
            pattern = r'(https?://[^\s]+)'
            urls = re.findall(pattern, url)
            # add the number of URLs found to the count for this row
            count += len(urls)
    # add the count for this row to the Servers.modified column
    df.loc[i, 'Servers_modified'] = count

# for column endpoints.added
df['endpoints.added'].fillna(value='', inplace=True)
endpoints_column = df['endpoints.added']

pattern = r"'method':\s+'(\w+)'"

count_matches = lambda lst: sum([bool(re.search(pattern, str(d))) for d in lst])
count_list = [count_matches(lst) for lst in endpoints_column]

df['Endpoints_added'] = count_list

# for endpoints.deleted
df['endpoints.deleted'].fillna(value='', inplace=True)
endpoints_column = df['endpoints.deleted']

pattern = r"'method':\s+'(\w+)'"

count_matches = lambda lst: sum([bool(re.search(pattern, str(d))) for d in lst])
count_list = [count_matches(lst) for lst in endpoints_column]

df['Endpoints_deleted'] = count_list

# for column components.parameters.added
def count_changes(row):
    if row is None:
        return 0
    else:
        return sum([len(row[key]) for key in row.keys()])

df['components.parameters.added'] = df['components.parameters.added'].astype(str)
df['Components_parameters_added'] = df['components.parameters.added'].apply(lambda x: count_changes(eval(x)) if x not in ('', None) else 0)

df['servers.added'] = df['servers.added'].astype(str) 
df['Servers_added'] = (df['servers.added'].str.extract(r'\[([^\]]*)', expand=False)
                    .str.split(',').str.len().fillna(0).astype(int))

df['servers.deleted'] = df['servers.deleted'].astype(str) 
df['Servers_deleted'] = (df['servers.deleted'].str.extract(r'\[([^\]]*)', expand=False)
                    .str.split(',').str.len().fillna(0).astype(int))

df['paths.added'] = df['paths.added'].astype(str) 
df['Paths_added'] = (df['paths.added'].str.extract(r'\[([^\]]*)', expand=False)
                    .str.split(',').str.len().fillna(0).astype(int))

df['paths.deleted'] = df['paths.deleted'].astype(str) 
df['Paths_deleted'] = (df['paths.deleted'].str.extract(r'\[([^\]]*)', expand=False)
                    .str.split(',').str.len().fillna(0).astype(int))

df['components.securitySchemes.added'] = df['components.securitySchemes.added'].astype(str) 
df['Components_Security_Schemes_added'] = (df['components.securitySchemes.added'].str.extract(r'\[([^\]]*)', expand=False)
                    .str.split(',').str.len().fillna(0).astype(int))
df['components.securitySchemes.deleted'] = df['components.securitySchemes.deleted'].astype(str) 
df['Components_Security_Schemes_deleted'] = (df['components.securitySchemes.deleted'].str.extract(r'\[([^\]]*)', expand=False)
                    .str.split(',').str.len().fillna(0).astype(int))

# for column components.parameters.deleted
def count_changes(row):
    if row is None:
        return 0
    else:
        return sum([len(row[key]) for key in row.keys()])

df['components.parameters.deleted'] = df['components.parameters.deleted'].astype(str)
df['Components_parameters_deleted'] = df['components.parameters.deleted'].apply(lambda x: count_changes(eval(x)) if x not in ('', None) else 0)

df.loc[:, 'Info_title_changes'] = df['info.title'].astype(str).astype(str).apply(lambda x: len(x.split(',')) if x.strip() else 0)
df.loc[:, 'Info_description_changes'] = df['info.description'].astype(str).apply(lambda x: len(x.split(',')) if x.strip() else 0)
df.loc[:, 'Info_contact_url_changes'] = df['info.contact.url'].astype(str).apply(lambda x: len(x.split(',')) if x.strip() else 0)
df.loc[:, 'Info_contact_email_changes'] = df['info.contact.email'].astype(str).apply(lambda x: len(x.split(',')) if x.strip() else 0)
df.loc[:, 'Info_license_name_changes'] = df['info.license.name']. astype(str).apply(lambda x: len(x.split(',')) if x.strip() else 0)
df.loc[:, 'Info_license_url_changes'] = df['info.license.url'].astype(str).apply(lambda x: len(x.split(',')) if x.strip() else 0)
df.loc[:, 'Info_termsOfService_changes'] = df['info.termsOfService'].astype(str).apply(lambda x: len(x.split(',')) if x.strip() else 0)

df['tags.added'] = df['tags.added'].astype(str) 
df['Tags_added'] = (df['tags.added'].str.extract(r'\[([^\]]*)', expand=False)
                    .str.split(',').str.len().fillna(0).astype(int))
                    
df['tags.deleted'] = df['tags.deleted'].astype(str) 
df['Tags_deleted'] = (df['tags.deleted'].str.extract(r'\[([^\]]*)', expand=False)
                    .str.split(',').str.len().fillna(0).astype(int))
df['components.headers.added'] = df['components.headers.added'].astype(str) 
df['Components_Headers_Added'] = (df['components.headers.added'].str.extract(r'\[([^\]]*)', expand=False)
                    .str.split(',').str.len().fillna(0).astype(int))
df['components.headers.deleted'] = df['components.headers.deleted'].astype(str) 
df['Components_Headers_Deleted'] = (df['components.headers.deleted'].str.extract(r'\[([^\]]*)', expand=False)
                    .str.split(',').str.len().fillna(0).astype(int))
df['components.requestBodies.added'] = df['components.requestBodies.added'].astype(str) 
df['Components_Request_Bodies_Added'] = (df['components.requestBodies.added'].str.extract(r'\[([^\]]*)', expand=False)
                    .str.split(',').str.len().fillna(0).astype(int))

df['components.requestBodies.deleted'] = df['components.requestBodies.deleted'].astype(str) 
df['Components_Request_Bodies_Deleted'] = (df['components.requestBodies.deleted'].str.extract(r'\[([^\]]*)', expand=False)
                    .str.split(',').str.len().fillna(0).astype(int))

df['components.responses.added'] = df['components.responses.added'].astype(str) 
df['Components_Responses_Added'] = (df['components.responses.added'].str.extract(r'\[([^\]]*)', expand=False)
                    .str.split(',').str.len().fillna(0).astype(int))

df['components.responses.deleted'] = df['components.responses.deleted'].astype(str) 
df['Components_Responses_Deleted'] = (df['components.responses.deleted'].str.extract(r'\[([^\]]*)', expand=False)
                    .str.split(',').str.len().fillna(0).astype(int))

df['components.schemas.added'] = df['components.schemas.added'].astype(str) 
df['Components_Schemas_Added'] = (df['components.schemas.added'].str.extract(r'\[([^\]]*)', expand=False)
                    .str.split(',').str.len().fillna(0).astype(int))

df['components.schemas.deleted'] = df['components.schemas.deleted'].astype(str) 
df['Components_Schemas_Deleted'] = (df['components.schemas.deleted'].str.extract(r'\[([^\]]*)', expand=False)
                    .str.split(',').str.len().fillna(0).astype(int))

df['components.links.added'] = df['components.links.added'].astype(str) 
df['Components_Links_Added'] = (df['components.links.added'].str.extract(r'\[([^\]]*)', expand=False)
                    .str.split(',').str.len().fillna(0).astype(int))

df['components.links.deleted'] = df['components.links.deleted'].astype(str) 
df['Components_Links_Deleted'] = (df['components.links.deleted'].str.extract(r'\[([^\]]*)', expand=False)
                    .str.split(',').str.len().fillna(0).astype(int))


df['components.securitySchemes.modified'] = df['components.securitySchemes.modified'].astype(str)
df['Components_Security_Schemes_modified'] = (df['components.securitySchemes.modified'].replace(np.nan, '{}')
                  .apply(ast.literal_eval).str.len())

df['tags.modified'] = df['tags.modified'].astype(str)
df['Tags_modified'] = (df['tags.modified'].replace(np.nan, '{}')
                  .apply(ast.literal_eval).str.len())

df['paths.modified'] = df['paths.modified'].astype(str)
df['Paths_modified'] = (df['paths.modified'].replace(np.nan, '{}')
                  .apply(ast.literal_eval).str.len())

df['security.modified'] = df['security.modified'].astype(str)
df['Security_modified'] = (df['security.modified'].replace(np.nan, '{}')
                  .apply(ast.literal_eval).str.len())

df['security.added'] = df['security.added'].astype(str) 
df['Security_added'] = (df['security.added'].str.extract(r'\[([^\]]*)', expand=False)
                    .str.split(',').str.len().fillna(0).astype(int))
df['security.deleted'] = df['security.deleted'].astype(str) 

df['Security_deleted'] = (df['security.deleted'].str.extract(r'\[([^\]]*)', expand=False)
                    .str.split(',').str.len().fillna(0).astype(int))
df['endpoints.modified'] = df['endpoints.modified'].astype(str)
df['Endpoints_modified'] = (df['endpoints.modified'].replace(np.nan, '{}')
                  .apply(ast.literal_eval).str.len())

df.to_csv('imptemp.csv')



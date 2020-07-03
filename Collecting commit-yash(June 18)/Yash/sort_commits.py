import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz
import json

df=pd.read_csv("vue.csv")

for id in df:
    df1=df[["commit.tree.url","commit.message","node_id","sha","commit.committer.date","committer.type"]]
c=0
df1.to_csv("nvue.csv")
sub="fix"
df2 = df1[df1['commit.message'].str.contains("fix")]
df2=df2[["commit.message"]]
df3 = df1[df1['commit.message'].str.contains("bug")] 
df3=df3[["commit.message"]]
df4 = df1[df1['commit.message'].str.contains("vulnerability")] 
df4=df4[["commit.message"]]
df3
frames = [df2, df3, df4]
result = pd.concat(frames)
result.to_csv("final.csv")
# for id in df1:
#     if (df1[df1['commit.message'].str.contains("fix")]==True ):
#         print("t")
   
result.rename(columns={'commit.message': 'commit_message'},inplace=True)
result
#open NVD file downloaded which has CVE number
file_path = '/Users/pandit_ji/Desktop/MS/ra/Collecting commit-yash(June 18)/Data/'
nvd_file = 'nvdcve-1.1-modified.json'
with open(file_path + nvd_file) as json_file:
    data = json.load(json_file)
 
cves = data['CVE_Items']
cves[0]


#Clean The file and create a dataframe


cve_number_list = [ sub['cve']['CVE_data_meta']['ID'] for sub in cves ] 
dfcve = pd.DataFrame(cves,index=cve_number_list)
# we would like a column that is CVE numbers rather than an index
dfcve = dfcve.rename_axis('cve_number').reset_index()
dfcve1=dfcve[["cve_number"]]
dfcve1


#Check for CVE number in commit messages
dfcve_final=dfcve1.cve_number.isin(result.commit_message).astype(int)
dfcve_final
#Open CWE file downloaded which has CWE info
cwed=pd.read_csv("699.csv")
#Create a new DF with only CWE ID
cwedf=cwed[["CWE-ID"]]
cwedf
cwedf.rename(columns={'CWE-ID': 'cwe_id'},inplace=True)
#Check for CWE in commit messages
cwedf_final=cwedf.cwe_id.isin(result.commit_message).astype(int)
cwedf_final

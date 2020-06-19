## import requests
import os
import json
from pprint import pprint
import csv
from github import Github
from pandas.io.json import json_normalize

##GIVE ACCESS PARAMETERS

ACCESS_TOKEN = '******'
username = '*****'

#REQUEST SESSION

github_api = "https://api.github.com"
gh_session = requests.Session()
gh_session.auth = (username, ACCESS_TOKEN)

#CHECK REQUEST RATE REMAINING
rate_l=gh_session.get("https://api.github.com/rate_limit")
pprint(rate_l.json())



#OPEN THE REPO_LIST.CSV PROVIDED AND CHECK EVERY LINK
with open('/Users/pandit_ji/Desktop/MS/ra/Repository_List.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            #READ AND BREAK URL AND PASS IT TO GET COMMIT DATA
             url=row[8]
             print(url.replace('https://',''))
             f=url.replace('https://','').split('/')
             commits = create_commits_df(f[3], f[2], github_api)
             print(commits)
                  
            #SAVE DATAFRAME TO CSV
                  
             commits.to_csv('/Users/pandit_ji/Desktop/commits1.csv')
             print(f[2],f[3])



#FUNCTION TO GET COMMIT DATA AND CREATE A DATA FRAME

def commits_of_repo_github(repo, owner, api):
    commits = []
    next = True
    i = 1
    while next == True:
        url = api + '/repos/{}/{}/commits?page={}&per_page=100'.format(owner, repo, i)
        print(url)
        commit_pg = gh_session.get(url = url)
        commit_pg_list = [dict(item, **{'repo_name':'{}'.format(repo)}) for item in commit_pg.json()]
        commit_pg_list = [dict(item, **{'owner':'{}'.format(owner)}) for item in commit_pg_list]
        commits = commits + commit_pg_list
        if 'Link' in commit_pg.headers:
            if 'rel="next"' not in commit_pg.headers['Link']:
                next = False
        i = i + 1
    return commits

#FUNCTION TO NORMALIZE COMMIT LIST OBTAINED FROM "commits_of_repo_github"
def create_commits_df(repo, owner, api):
    commits_list = commits_of_repo_github(repo, owner, api)
    return json_normalize(commits_list)


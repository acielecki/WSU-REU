import pandas as pd
import requests
import os
import json

class RetrvCommits():

    def __init__(self, repo_url):    
        self.repo_url = repo_url
        self.username = "acielecki"
        self.token = "369e1093422f763f2745348139a4762218f62848"
        self.list_of_commits = []

    def http_get_call(self, url):
        result = requests.get(url,
                              auth=(self.username, self.token),
                              headers={"Accept": "application/vnd.github.mercy-preview+json"})
        
        return result.json()

    def collect_commits(self):
        print("Retrieve commits -> %s"  %(self.repo_url))
        
        page_num = 1

        #Will visit each page and add results to self.list_of_commits
        while True:
            #Use below command to get commit stats instead
            #commits_url = self.repo_url + "/stats/contributors?" + "per_page=100" + "&page=" + str(page_num)
            
            commits_url = self.repo_url + "/commits?" + "per_page=100" + "&page=" + str(page_num)   
            results = self.http_get_call (commits_url)
            print ("[%d]Get Commits Num = %d"  %(page_num, len (results)))          
            self.list_of_commits += results
            #stop at last page
            if (len (results) < 100):
                break
            page_num += 1

#Retrieve commits data for each project in Repository_List
#and save the results to a file under the project's name
#Ex. https://api.github.com/repos/airbnb/javascript/ --> airbnb_javascript
df = pd.read_csv('Repository_List.csv')
repo_urls = df['url']

for api_url in repo_urls:
        RC = RetrvCommits(api_url)
        RC.collect_commits ()
        #Use below command to save stats to a separate file if applicable
        #filename = api_url[29:].replace('/', '_') + '_stats'
        
        filename = api_url[29:].replace('/', '_')
        with open(filename, 'w') as outfile:
            json.dump(RC.list_of_commits, outfile)

import requests
import os
import csv
import pandas as pd
import json

class RetrvCommitStats():

    def __init__(self, repo_id, repo_url):
            self.repo_id = repo_id
            self.repo_url = repo_url

            self.username = "*******"
            self.token = "****************************"

            self.commit_stats = []

    def http_get_call(self, url):
        result = requests.get(url,
                              auth=(self.username, self.token),
                              headers={"Accept": "application/vnd.github.mercy-preview+json"})
        
        return result.json()
    
    def write_csv(self):
        file = str(self.repo_id) + '_stats' +'.csv'

        with open(file, 'w', encoding='utf-8', newline='') as csv_file:
        
            writer = csv.writer(csv_file)

            header = list(self.commit_stats[0].keys()) 
            writer.writerow(header)
            
            for stats in self.commit_stats:
                if stats != None:
                    row = list(stats.values())
                    writer.writerow(row)
        csv_file.close()
        
    #Collect statistics for all files changed in given commit
    def parse_stats(self, commit_url):
        print("Retrieving commit stats for %s"  %(commit_url))
        result = self.http_get_call(commit_url)
        files = result['files']
        for file in files:
            stats = {}
            stats['filename'] = file['filename']
            stats['status'] = file['status']
            stats['additions'] = file['additions']
            stats['deletions'] = file['deletions']
            stats['changes'] = file['changes']
            if('patch' in file.keys()):
                stats['patch'] = file['patch']
            else:
                stats['patch'] = ""
            stats['contents_url'] = file['contents_url']
            
            self.commit_stats.append(stats)
            
    #Iterate over all the commits in the repository and
    #collect commit statistics by constructing the url
    #which compares commits with their parent(s)
    def collect_commit_stats(self):
        commitsfile = str(self.repo_id) + "_commits.csv"
        cdf = pd.read_csv(commitsfile)
        for index, row in cdf.iterrows():
            #if the commit is a merge with two parents
            if(',' in str(row['parents'])):
                parent1 = row['parents'].split(',')[0]
                parent2 = row['parents'].split(' ')[1]
                stats_url1 = self.repo_url + "/compare/" + parent1 + "..." + row['sha']
                stats_url2 = self.repo_url + "/compare/" + parent2 + "..." + row['sha']
                self.parse_stats(stats_url1)
                self.parse_stats(stats_url2)
            #only one parent
            else:
                stats_url = self.repo_url + "/compare/" + str(row['parents']) + "..." + row['sha']
                #make sure we have not reached the last commit
                if ("nan" not in stats_url):
                    self.parse_stats(stats_url)
        if(self.commit_stats != []):
            self.write_csv()
            
#Automation over all repositories

#df = pd.read_csv('Repository_List.csv')

#for index, row in df.iterrows():
    #RCS = RetrvCommitStats(row['id'], row['url'] )     
    #RCS.collect_commit_stats()
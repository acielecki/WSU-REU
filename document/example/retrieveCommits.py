#!/usr/bin/python

import requests
import os
import csv 

class RetrvCommits():

    def __init__(self, repo_id, repo_url):    
        self.repo_id  = repo_id
        self.repo_url = repo_url
        
        self.username = ""
        self.password = ""
        
        self.list_of_commits = []
        
    def get_basic_auth(self):
        if (os.getenv("GIT_NAME", "None") != "None" and os.getenv("GIT_PWD", "None") != "None"):
            print("Github Username:****** \r\n", end="")
            self.username = os.environ["GIT_NAME"]
            print("Github Password:****** \r\n", end="")
            self.password = os.environ["GIT_PWD"] 
        else:        
            print("Github Username: ", end="")
            self.username = str(input())
            print("Github Password: ", end="")
            self.password = str(input())

    def http_get_call(self, url):
        result = requests.get(url,
                              auth=(self.username, self.password),
                              headers={"Accept": "application/vnd.github.mercy-preview+json"})
        
        return result.json()
        
    def write_csv(self):
        file = str(self.repo_id) + '.csv'

        with open(file, 'w') as csv_file:
        
            writer = csv.writer(csv_file)

            header = list(self.list_of_commits[0].keys()) 
            writer.writerow(header)
            
            for commit in self.list_of_commits:
                row = list(commit.values())
                writer.writerow(row)
        csv_file.close()
        
    def filter_commits(self, commits):
        commit_list = []
        
        for item in commits:
            commit_dict = {}
            
            commit_dict["sha"]     = item["sha"]
            commit_dict["author"]  = item["commit"]["author"]["name"]
            commit_dict["date"]    = item["commit"]["author"]["date"]
            commit_dict["message"] = item["commit"]["message"]
            commit_dict["commits"] = item["commit"]["tree"]["url"]
            #print (commit_dict)
            commit_list.append (commit_dict)
            
        return commit_list

    def collect_commits(self):
    
        self.get_basic_auth ()
        print("Retrieve commits -> %s"  %(self.repo_url))
        
        page_num = 1
        while True:

            commits_url = self.repo_url + "/commits?" + "per_page=100" + "&page=" + str(page_num)
            
            commits = self.http_get_call (commits_url)
            commit_num = len (commits)
  
            print ("[%d]Get Commits Num = %d"  %(page_num, commit_num))
            
            self.list_of_commits += self.filter_commits (commits)            
            
            page_num += 1
            if (commit_num < 100):
                break
       
        self.write_csv ()
        
        
RC = RetrvCommits(123, "https://api.github.com/repos/vuejs/vue")
RC.collect_commits ()
    

    
#!/usr/bin/python

import requests
import os

class RetrvCommits():

    def __init__(self, repo_url):    
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

    def collect_commits(self):
    
        self.get_basic_auth ()
        print("Retrieve commits -> %s"  %(self.repo_url))
        
        page_num = 1
        while True:

            commits_url = self.repo_url + "/commits?" + "per_page=100" + "&page=" + str(page_num)   
            results = self.http_get_call (commits_url)
            if (len (results) < 100):
                print (results)
            
            print ("[%d]Get Commits Num = %d"  %(page_num, len (results)))          
            self.list_of_commits += results
            
            page_num += 1
        
        
RC = RetrvCommits("https://api.github.com/repos/vuejs/vue")
RC.collect_commits ()
    

    
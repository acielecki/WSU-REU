import requests
import os
import csv
import pandas as pd
import json
import mysql.connector

class RetrvCommits():

    def __init__(self, repo_id, repo_url, account):    
        self.repo_id  = repo_id
        self.repo_url = repo_url
        
        self.username = account['username']
        self.token = account['token']
        
        self.list_of_commits = []
        
    def http_get_call(self, url):
        result = requests.get(url,
                              auth=(self.username, self.token),
                              headers={"Accept": "application/vnd.github.mercy-preview+json"})
        
        return result.json()
        
    def write_csv(self):
        file = str(self.repo_id) + '_commits.csv'

        with open(file, 'w', encoding="utf-8", newline='') as csv_file:
        
            writer = csv.writer(csv_file)

            header = list(self.list_of_commits[0].keys()) 
            writer.writerow(header)
            
            for commit in self.list_of_commits:
                row = list(commit.values())
                writer.writerow(row)
        csv_file.close()

    def connect_to_db(self):
        self.mydb = mysql.connector.connect(
          host="localhost",
          user="root",
          password="************",
          database="test1"
        )
        
    def write_to_db(self):
        header = str(list(self.list_of_commits[0].keys()))
        remove_chars = ['[', ']', '\'']
        for char in remove_chars:
            header = header.replace(char, '')
            
        columns = "sha VARCHAR(255), author VARCHAR(255), date VARCHAR(255), message TEXT, commits VARCHAR(255), parents VARCHAR(255)"
        table_stmnt = "CREATE TABLE IF NOT EXISTS %s (%s);" %('commits_' + str(self.repo_id), columns)
        cursor = self.mydb.cursor()
        cursor.execute(table_stmnt)
        
        for commit in self.list_of_commits:
            row = list(commit.values())
            sha = row[0]
            author = str(row[1]).replace('\'', '')
            date = row[2]
            message = str(row[3]).replace('\'', '')
            message = message.replace('\\', 'forwardslash')
            commits = row[4]
            parents = row[5]
            insert_stmnt = "INSERT INTO %s (%s) VALUES ('%s', '%s', '%s', '%s', '%s', '%s');" % ('commits_' + str(self.repo_id), header, sha, author, date, message, commits, parents)
            #print(insert_stmnt)
            cursor.execute(insert_stmnt)
            self.mydb.commit()
            
    #collect commit information displayed on given page
    #and add it to out list of commits for the given project
    def filter_commits(self, commits):
        commit_list = []
        
        for item in commits:
            commit_dict = {}
            
            commit_dict["sha"]     = item["sha"]
            commit_dict["author"]  = item["commit"]["author"]["name"]
            commit_dict["date"]    = item["commit"]["author"]["date"]
            commit_dict["message"] = item["commit"]["message"]
            commit_dict["commits"] = item["commit"]["tree"]["url"]
            #if no parents exist, set value to none
            if (len(item["parents"]) < 1):
               commit_dict["parents"] = "None"
            #if 1 parent exists, record sha
            elif (len(item["parents"]) == 1):
                commit_dict["parents"] = item["parents"][0]["sha"]
            #if 2 parents exist, records both shas separated by a dash
            else:
                commit_dict["parents"] = item["parents"][0]["sha"] + "-" + item["parents"][1]["sha"]
            #print (commit_dict)
            commit_list.append(commit_dict)
            
        return commit_list
    
    #Iterate over all pages of commit info to collect commits
    def collect_commits(self):
    
        print("Retrieve commits -> %s"  %(self.repo_url))
        
        page_num = 1
        while True:

            commits_url = self.repo_url + "/commits?" + "per_page=100" + "&page=" + str(page_num)
            
            commits = self.http_get_call(commits_url)
            commit_num = len(commits)
  
            print ("[%d]Get Commits Num = %d"  %(page_num, commit_num))
            
            self.list_of_commits += self.filter_commits (commits)            
            
            page_num += 1
            if (commit_num < 100):
                break
            
        self.write_to_db()
        
        
#Retrieve commits data for each project in Repository_List
#and save the results to a table named commits_repo_id
        
#df = pd.read_csv('Repository_List.csv')
#account = {'username': 'acielecki', 'token': '****************************'}
#for index, row in df.iterrows():
    #RC = RetrvCommits(row['id'], row['url'], account)
    #RC.connect_to_db()
    #RC.collect_commits()



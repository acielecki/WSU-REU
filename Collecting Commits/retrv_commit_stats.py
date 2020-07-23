import requests
import os
import csv
import pandas as pd
import json
import mysql.connector

class RetrvCommitStats():

    def __init__(self, repo_id, repo_url, account):
            self.repo_id = repo_id
            self.repo_url = repo_url

            self.username = account['username']
            self.token = account['token']

            self.commit_stats = []

    def http_get_call(self, url):
        result = requests.get(url,
                              auth=(self.username, self.token),
                              headers={"Accept": "application/vnd.github.mercy-preview+json"})
        
        return result.json()
    
    def connect_to_db(self):
        self.mydb = mysql.connector.connect(
          host="localhost",
          user="root",
          password="************",
          database="test1"
        )
    def write_to_db(self):
        header = str(list(self.commit_stats[0].keys()))
        remove_chars = ['[', ']', '\'']
        for char in remove_chars:
            header = header.replace(char, '')
            
        columns = "filename VARCHAR(255), status VARCHAR(255), additions INT, deletions INT, changes INT, patch TEXT, contents_url VARCHAR(255)"
        table_stmnt = "CREATE TABLE IF NOT EXISTS %s (%s);" %('stats_' + str(self.repo_id), columns)
        cursor = self.mydb.cursor()
        cursor.execute(table_stmnt)
        
        for commit in self.commit_stats:
            row = list(commit.values())
            insert_stmnt = "INSERT INTO %s (%s) VALUES ('%s', '%s', '%d', '%d', '%d', '%s', '%s');" % ('stats_' + str(self.repo_id), header, row[0], row[1], row[2], row[3], row[4], str(row[5]).replace('\'', ''), row[6])
            #print(insert_stmnt)
            cursor.execute(insert_stmnt)
            self.mydb.commit()
            
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
        
        cursor = self.mydb.cursor()
        select_stmnt = "SELECT parents, sha FROM %s" % ('commits_' + str(self.repo_id))
        cursor.execute(select_stmnt)
        result = cursor.fetchall()
        for row in result:
            #if the commit is a merge with two parents
            if('-' in str(row[0])):
                parent1 = row[0].split('-')[0]
                parent2 = row[0].split('-')[1]
                stats_url1 = self.repo_url + "/compare/" + parent1 + "..." + row[1]
                stats_url2 = self.repo_url + "/compare/" + parent2 + "..." + row[1]
                self.parse_stats(stats_url1)
                self.parse_stats(stats_url2)
            #only one parent
            else:
                stats_url = self.repo_url + "/compare/" + str(row[0]) + "..." + row[1]
                #make sure we have not reached the last commit
                if ("None" not in stats_url):
                    self.parse_stats(stats_url)
        if(self.commit_stats != []):
            self.write_to_db()


#Automate over all Repositories in Repository_List

#df = pd.read_csv('Repository_List.csv')
#account = {'username': 'acielecki', 'token': '************************'}
#for index, row in df.iterrows():
    #RCS = RetrvCommitStats(row['id'], row['url'], account)
    #RCS.connect_to_db()
    #RCS.collect_commit_stats()


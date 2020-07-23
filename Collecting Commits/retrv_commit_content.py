import requests
import os
import csv
import pandas as pd
import json
import base64
import mysql.connector

class RetrvCommitContent():
    def __init__(self, repo_id, account):    
        self.repo_id  = repo_id 
        
        self.username = account['username']
        self.token = account['token']
        
        self.commit_content = []
        
    def http_get_call(self, url):
        result = requests.get(url,
                              auth=(self.username, self.token),
                              headers={"Accept": "application/vnd.github.mercy-preview+json"})
        
        return result.json()
    
    def connect_to_db(self):
        self.mydb = mysql.connector.connect(
          host="localhost",
          user="root",
          password="***********",
          database="test1"
        )
        
    def write_to_db(self):
        if not self.commit_content:
            self.collect_commit_content()
        else:
            header = str(list(self.commit_content[0].keys()))
            remove_chars = ['[', ']', '\'']
            for char in remove_chars:
                header = header.replace(char, '')
                
            columns = "sha VARCHAR (255), path VARCHAR(255), type VARCHAR(255), content TEXT"
            table_stmnt = "CREATE TABLE IF NOT EXISTS %s (%s);" %('content_' + str(self.repo_id), columns)
            cursor = self.mydb.cursor()
            cursor.execute(table_stmnt)
            
            for commit in self.commit_content:
                row = list(commit.values())
                insert_stmnt = "INSERT INTO %s (%s) VALUES ('%s', '%s', '%s', '%s');" % ('content_' + str(self.repo_id), header, row[0], row[1], row[2], str(row[3]).replace('\'', ''))
                cursor.execute(insert_stmnt)
                self.mydb.commit()
            
    def parse_commits(self, commit_url):
        print("Retrieving commit content for %s"  %(commit_url))
        result = self.http_get_call(commit_url)

        if 'tree' in result:
            allitems = result['tree']
        else:
            allitems = {}
            
        for item in allitems:
            if item['type'] == 'tree':
                self.parse_commits(item['url'])
            else:                             
                result2 = self.http_get_call(item['url'])
                if 'content' in result2:
                    content = result2['content']
                    content = base64.b64decode(content)

                    record = {}
                    record['sha'] = item['sha']
                    record['path'] = item['path']
                    record['type'] = item['type']
                    record['content'] = content
                
                    self.commit_content.append(record)
            
    def collect_commit_content(self):
        cursor = self.mydb.cursor()
        select_stmnt = "SELECT commits FROM %s" % ('commits_' + str(self.repo_id))
        cursor.execute(select_stmnt)
        result = cursor.fetchall()
        for commit_url in result:
            self.parse_commits(commit_url[0])
        self.write_to_db()

#Test for a single file            
#RCC = RetrvCommitContent('18047027')
#RCC.collect_commit_content()

#Automate for each repository
#df = pd.read_csv('Repository_List.csv')
#account = {'username': 'acielecki', 'token': '***********************'}

#for repo_id in df['id']:
    #RCC = RetrvCommitContent(str(repo_id), account)
    #RCC.connect_to_db()
    #RCC.collect_commit_content()

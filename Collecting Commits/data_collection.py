import csv
import pandas as pd
import mysql.connector
import retrv_commits as RetrvCommits
import retrv_commit_content as RetrvCommitContent
import retrv_commit_stats as RetrvCommitStats

class DataCollection():
    
    def __init__(self):
        self.repo_list = pd.read_csv('Repository_List.csv')
        
    def populate_commits(self):
        for index, row in self.repo_list.iterrows():
            RC = RetrvCommits(row['id'], row['url']
            RC.connect_to_db()
            RC.collect_commits()
                    
    def populate_stats(self):
        for index, row in self.repo_list.iterrows():
            RCS = RetrvCommitStats(row['id'], row['url']
            RCS.connect_to_db()
            RCS.collect_commits()

    def populate_content(self):
        for repo_id in self.repo_list['id']:
            RCC = RetrvCommitContent(str(repo_id))
            RCC.connect_to_db()
            RCC.collect_commit_content()
            
#Access database to retrieve the commit log/message 
#and code changes if applicable
class DataRetrieval():

    def connect_to_db(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="txbTMstvwkKWfOBP",
            database="test"
        )
                                   
    def retrv_commit_messages(self, repo_id):
        self.connect_to_db()
        cursor = self.mydb.cursor()
        select_stmnt = "SELECT sha, message FROM %s" % ('commits_' + str(repo_id))
        cursor.execute(select_stmnt)
        result = cursor.fetchall()

        return result

    def retrv_code_changes(self, repo_id, sha):
        self.connect_to_db()
        select_stmnt = "SELECT content FROM %s WHERE sha='%s'" % ('content_' + str(repo_id), sha)
        cursor.execute(select_stmnt)
        result = cursor.fetchall()

        return result

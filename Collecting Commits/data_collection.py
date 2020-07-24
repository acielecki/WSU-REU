import csv
import pandas as pd
import mysql.connector
from retrv_commits import RetrvCommits
from retrv_commit_content import RetrvCommitContent
from retrv_commit_stats import RetrvCommitStats

class DataCollection():
    
    def __init__(self, repo_list, account):
        self.repo_list = repo_list
        self.account = account
        
    def collection(self):
        self.populate_commits()
        self.populate_stats()
        self.populate_content()
        
    def populate_commits(self):
        for index, row in self.repo_list.iterrows():
            RC = RetrvCommits(row['id'], row['url'], self.account)
            RC.connect_to_db()
            RC.collect_commits()
                    
    def populate_stats(self):
        for index, row in self.repo_list.iterrows():
            RCS = RetrvCommitStats(row['id'], row['url'], self.account)
            RCS.connect_to_db()
            RCS.collect_commit_stats()

    def populate_content(self):
        for repo_id in self.repo_list['id']:
            RCC = RetrvCommitContent(str(repo_id), self.account)
            RCC.connect_to_db()
            RCC.collect_commit_content()
                                   
class DataRetrieval():

    def connect_to_db(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="*****************",
            database="test1"
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


#Data collection example:
#repo_list1 = pd.read_csv('test_list.csv')
#account1 = {'username': 'acielecki', 'token': '******************************'}
#DC1 = DataCollection(repo_list1, account1)
#DC1.collection()


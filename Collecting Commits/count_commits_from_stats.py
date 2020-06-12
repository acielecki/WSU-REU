#Counts the number of commits for a project from the statistics
#Work in progress, currently does not produce correct numbers
import pandas as pd

df = pd.read_csv('Repository_List.csv')
repo_urls = df['url']

for api_url in repo_urls:
    filename = api_url[29:].replace('/', '_') + "2"
    
    f = open(filename, "r")
    
    data = f.read()
    data_list = data.split()
    total_commits = 0
    
    for index, word in enumerate(data_list):
        if word == "{\"total\":":
            total_commits += int(data_list[index + 1].replace(',', ''))
            print(data_list[index + 1].replace(',', ''))
    print(total_commits)
    f.close()

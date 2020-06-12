#Similar to count_commits_for_one but will count the
#total commits for each project in Repository_List given
#the filename which contains the commit information.
#Similarly inaccurate.
import pandas as pd

df = pd.read_csv('Repository_List.csv')
repo_urls = df['url']

for api_url in repo_urls:
    filename = api_url[29:].replace('/', '_')
    f = open(filename, "r")
    data = f.read()
    total_commits = data.count("\"commit\"")
    print(total_commits)
    f.close()

import pandas as pd

df = pd.read_csv('FILENAME.csv')
repo_urls = df['urls']
w = open('NEWFILENAME.csv', 'w')
w.write('urls\n');

for row in repo_urls:
        new_url = 'https://github.com/' + row[29:] 
        w.write(new_url + '\n')
w.close

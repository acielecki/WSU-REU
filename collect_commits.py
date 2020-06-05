import pandas as pd
import requests
import subprocess
import shutil
import stat
import os
import ast

def handleError(func, path, exc_info):
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise

#file to read from
df = pd.read_csv('urls.csv') 

#file to write to
w = open('commits.csv', 'w') 
w.write('url,commits\n')

url_list = df['urls']

for url in url_list:
	url_dir = url.rsplit('/', 1)[1]
	clone_cmd = 'git clone ' + url

	#clone the repository
	pipe1 = subprocess.Popen(clone_cmd, shell=True)
	pipe1.wait()

	#change directory into repository
	os.chdir(url_dir)

	#get total # of commits for this repository
	output = subprocess.check_output('git rev-list --count HEAD', shell=True)
	commits = ast.literal_eval(output.decode("ascii"))
	
	#change directory back to main folder
	os.chdir('..')
	w.write(url + ',' + str(commits) + '\n')

	#delete repository
	if url_dir is not None: 
		shutil.rmtree(url_dir, onerror=handleError)

	
	



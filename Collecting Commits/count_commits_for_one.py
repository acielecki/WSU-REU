#Counts the number of commits for a project from the 
#file containing all commit info Ex. "airbnb_javascript"
#Results do not always match up with what appears on the
#project site. Ex. https://github.com/airbnb/javascript says 1822
#but this code returns 1817
f = open(filename, "r")
    
data = f.read()

total_commits = data.count("\"commit\"")
    
print(total_commits)

f.close()

url = 'https://github.com/Kur12120/soc-management-app.git'
config = '''[core]
repositoryformatversion = 0
filemode = false
bare = false
logallrefupdates = true
symlinks = false
ignorecase = true
[remote "origin"]
url = ''' + url + '''
fetch = +refs/heads/*:refs/remotes/origin/*
[branch "main"]
remote = origin
merge = refs/heads/main
'''
with open('.git/config', 'w') as f:
    f.write(config)
print('Git config written with URL: ' + url)
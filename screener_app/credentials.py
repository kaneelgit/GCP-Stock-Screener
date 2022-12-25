#credentials file location
reddit_cred_dir = '/mnt/c/Users/kanee/Desktop/git/credentials/reddit_creds.txt'

#open file
with open(reddit_cred_dir) as f:
    lines = f.readlines()

#get credentials reddit
client_id = lines[0].split()[0]
secret = lines[1].split()[0]
user_id = lines[2].split()[0] 

#credentials for TD app

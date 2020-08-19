# Importing required libraries
import os
import sys
# sys.path.insert(1, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..\\..\\'))
from k3y5 import DEV_GIT_KEY
import requests
import json
import itertools  
import collections 
import numpy as np

# Function to get information output in JSON format
def apiToJson(url):
    payload = ''
    headers = {
        'Authorization': 'Bearer ' + DEV_GIT_KEY,
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers, data = payload)
    v = json.loads(response.text)
    
    return (json.loads(response.text), response.headers)

# Function used to get Github data of the user
def getUserGitData(user):
    try:
        repoList = apiToJson("https://api.github.com/users/" + user + "/repos")[0]
        repoLangData = []
        repoContriData = []
        for i in range (len(repoList)):
            repoLangData.append (apiToJson(repoList[i]['languages_url'])[0])
            repoContriData.append (apiToJson(repoList[i]["contributors_url"])[0])
        thisUserResponse = apiToJson("https://api.github.com/users/"+user+"/events")
        thisUser = thisUserResponse[0]
        thisUserHeader = thisUserResponse[1]
        if not (len(thisUser)>0):
            print("Invalid Username")
            return None
        else:
            last_event_url = thisUserHeader['Link'].split(', ')[1].split('>')[0][1:]
            last_page_num = int(last_event_url.split('=')[-1])
            lastPageActivity = apiToJson(last_event_url)[0]
            thisUserContri = len(lastPageActivity) + (30 * (last_page_num - 1))
            
    except:
        print("ERR Fetching GitHub API Data")
        return None
    try:
        sumThisUserCommits = 0
        sumCommitPercent = 0
        allLangList = []
        for i in range(len(repoList)):
            
            languageDict = repoLangData[i]
            langList = list(languageDict.keys())
            for lang in langList:
                allLangList.append(lang)
            allLangList = list(set(allLangList))

            this_contri = repoContriData[i]
            allCommits = 0 
            this_userCommits=0
            for j in range(len(this_contri)):
                allCommits = allCommits + this_contri[j]["contributions"]
                if this_contri[j]["login"] == user:
                    this_userCommits = this_contri[j]["contributions"]
                    sumThisUserCommits = sumThisUserCommits + this_contri[j]["contributions"] 
                
            commit_percent = (this_userCommits / allCommits) * 100
            sumCommitPercent = sumCommitPercent + commit_percent

        gitStats = {
            'avgContri': (sumCommitPercent / len(repoList)),
            'langList': allLangList,
            'recentContri': thisUserContri
        }

        return gitStats
    
    except:
        print("Invalid Username")
        return None

# Function used to calculate the difference between two users regarding their average and recent contribution  
def gitDistance(user1, user2):
    try:
        stat1 = getUserGitData(user1)
        stat2 = getUserGitData(user2)

        score = {
            "avgContri": abs(stat1['avgContri'] - stat2['avgContri']),
            "recentContri": abs(stat1['recentContri'] - stat2['recentContri'])
        }
        return (score['avgContri']/10 + score['recentContri']/100)/2
    except:
        return 0



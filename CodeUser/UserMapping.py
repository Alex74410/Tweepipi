import tweepy as tw
import time
from collections import Counter
import re
import csv

import shutil
import operator

consumer_key= 'E2v8hoHS6iAlTb0dU5fmCTwno'
consumer_secret= '5VfhIJAldDZbbmDjzxu0X7y0RK6BR1zTGtEKCQGtuQChjI8Nw9'
access_token= '1000532954416926720-sbQWtdJtZk9rcAsMLPAjUZvWNVBlWe'
access_token_secret= 'm5Z44oOlTut6bDJOPMvRpDJnFOhsI8hGHuBaVbbupsR0X'



auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

stopWords = ['co','https','i', 'me','says','amp','said', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren', 'won', 'wouldn']

#Fonctions
#########################################################################

#followers_count ->est suivi
#friends_count ->suit

def searchTw(srch,date,nb):
    
    tweets = tw.Cursor(api.search,
              q=srch,
              lang="en",
              since=date,
              tweet_mode="extended").items(nb)
    return tweets


def UserTxt(tweets):
    txt = []
    for tweet in tweets:
        txt.append(tweet.user)  
    return txt




def get_follows(user_name):
    followers = []
    for page in tw.Cursor(api.friends, screen_name=user_name, wait_on_rate_limit=True,count=200).pages():
        followers.extend(page)
    return followers



def clean(txt):
    new = {}
    for i in txt:
        if i.lower() not in stopWords:
            new[i.lower()] = txt[i]
    return new

def get100TweetC(user):
    allTweet = ""
    tweets = api.user_timeline(screen_name=user, 
                               count=100,
                               include_rts = False,
                               tweet_mode = 'extended'
                               )
    for tweet in tweets:
        allTweet += tweet.full_text
    listW = re.findall(r'\w+', allTweet)
    c = Counter(listW)
    d = clean(c)
    return {k: v for k, v in sorted(d.items(), key=lambda item: item[1], reverse = True)}
    


def createCSVKey(name):
    with open(name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["test",1])
           
        
def createCSVUser(name):
    with open(name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["user"])

def createCSVUserInt(name):
    with open(name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["user",1])
    
def createCSVUserF(name):
    with open(name, 'w', newline='') as file:
        writer = csv.writer(file)
              
        
        

def writeCSV(twcount,name):
    r = csv.reader(open(name)) # Here your csv file
    lines = list(r)
    for x in twcount:
        s = 0
        for row in lines:
            if str(row[0]) == str(x):
                
                b = row[1]
                c = twcount[x]
                row[1] = int(int(b) + int(c))
                s = 1
        if s == 0:
            lines.append([x,int(twcount[x])])
    
    sorted_by_second = sorted(lines, key=lambda tup: int(float(tup[1])),reverse = True)
    writer = csv.writer(open(name, 'w'))
    writer.writerows(sorted_by_second)
    
    
    
                
def getMaxPoint(fileint):
    r = csv.reader(open(fileint)) # Here your csv file
    lines = list(r)
    return lines[0][1]
    
def getPoint(user,fileint):
    r = csv.reader(open(fileint)) # Here your csv file
    lines = list(r)
    score=0
    for row in lines:
        if row[0] == user:
            score = row[1]
    return score


        
def evaluateJourna(name,file,add):
    try:
        tweets = api.user_timeline(screen_name=name, 
                                   count=100,
                                   include_rts = True,
                                   tweet_mode = 'extended'
                                   )
    except tw.TweepError:
        return 0
        
    r = csv.reader(open(file)) # Here your csv file
    lines = list(r)
    score = 0
    certif = 0
    allTweet = ""
    for tweet in tweets:
        if tweet.user.verified == True:
            certif = 1
        allTweet += tweet.full_text
    listW = re.findall(r'\w+', allTweet)
        
    for content in listW:
        pos = 30
        for i in lines:
            if i[0] == content.lower() and pos > 0:
                score = score + pos
            pos += -1
    if certif == 1:
        score = score + score*  0.2
        
    if add == 1:
        ct = get100TweetC(name)
        writeCSV(ct,file)
 
    return score


            
def getIntFollow(user, KeyWordDesc, nbFollow,file1,fileUser,fileUserInt,country):
    
    follow = []
    follow2 = {}
    nb = 0
    print("bonjour")
    f = get_follows(user)
    
    #f = tw.Cursor(api.friends, screen_name=user, count = 200).items()
    for x in f:
        if x.followers_count > nbFollow:
            print(nb)
            add = 0
            for y in KeyWordDesc:
                if y in x.description and x.screen_name not in follow and x.protected == False:
                    if writeUserTest(x.screen_name, fileUser):
                        if country in x.description:
                            add = 1
                        print(x.screen_name)
                        nb += 1
                        writer = csv.writer(open(fileUserInt, 'a',newline=''))
                        writer.writerow([x.screen_name,evaluateJourna(x.screen_name,file1,add)])
                        
                      
                    if int(float(getPoint(x.screen_name,fileUserInt))) > 700:
                        point = (int(float(getPoint(user,fileUserInt))) /int(float(getMaxPoint(fileUserInt))))/10
                        updatePoint(x.screen_name,point, fileUserInt)
                         
    r = csv.reader(open(fileUserInt)) # Here your csv file
    lines = list(r)
    sorted_by_second = sorted(lines, key=lambda tup: int(float(tup[1])),reverse = True)
    writer = csv.writer(open(fileUserInt, 'w'))
    writer.writerows(sorted_by_second)
    print("nb compte testé: ",nb)
    return follow2      


    
def writeUserTest(user,file):
     r = csv.reader(open(file)) # Here your csv file
     lines = list(r)
     t = 0
     for i in lines:
         if i[0] == user:
             t = 1
     if t == 0:
          writer = csv.writer(open(file, 'a',newline=''))
          writer.writerow([user])
          return True
     else:
         return False
         
             

    
def mainTest(accountL,country):
    
    createCSVUser(country+"User.csv")
    createCSVUserInt(country+"Int.csv")
    createCSVKey(country+"Key.csv")
    
    for i in accountL:
        ct = get100TweetC(i)
        writeCSV(ct, country+"Key.csv")
    
    lEval = ["1er",0]
    for i in accountL:
        ev = evaluateJourna(i,country+"Key.csv",0)
       
        
        if ev > lEval[1]:
            lEval = [i,ev]
    
    userF = []
    userF.append(lEval[0])
    getIntFollow(userF[0], KeyWordDesc, 2000,country+"Key.csv",country+"User.csv",country+"Int.csv",country)
    
    for z in range(20):
        r = csv.reader(open(country+"Int.csv")) # Here your csv file
        lines = list(r)
        b = 0
        for a in lines:
            if b == 0:
                if a[0] not in userF:
                    userF.append(a[0])
                    print(a[1])
                    print(userF)
                    getIntFollow(a[0], KeyWordDesc, 2000,country+"Key.csv",country+"User.csv",country+"Int.csv",country)
                    b = 1
    
    return userF 


def continuTest(country,userF):
    
    for z in range(20):
        r = csv.reader(open(country+"Int.csv")) # Here your csv file
        lines = list(r)
        b = 0
        for a in lines:
            if b == 0:
                if a[0] not in userF:
                    userF.append(a[0])
                    print(a[0])
                    getIntFollow(a[0], KeyWordDesc, 2000,country+"Key.csv",country+"User.csv",country+"Int.csv",country)
                    b = 1
    
    return userF 

      
def updatePoint(user,point,fileint):
    r = csv.reader(open(fileint)) # Here your csv file
    lines = list(r)
    for row in lines:
        if row[0] == user:
            row[1]= int(float(row[1]))+int(float(row[1]))*point
    sorted_by_second = sorted(lines, key=lambda tup: int(float(tup[1])),reverse = True)
    writer = csv.writer(open(fileint, 'w'))
    writer.writerows(sorted_by_second)
    
   


#Data
######################################################################  
    
    
KeyWordDesc = ["journalist", "journalism", "news", "newspaper", "reporter", "politic", "minister", 
               "president", "governement", "correspondent", "info", "chairman", "deputy", "information",
               "governor", "legislator", "media", "commentary","activist","lawer","phd", "attorney", "researcher","freelance","professor"]


Kj = ["journalist", "journalism", "news", "newspaper", "reporter","correspondent", "info","information", "media", "commentary","freelance"]
Kp = [ "president", "governement", "chairman", "deputy", "minister","legislator","activist"]
Kr = ["phd", "researcher","professor","lawer","attorney"]



#Main
###########################################################################


#createCSVUserInt("testHKInt.csv")
#createCSVUser("testHKUser.csv")
#createCSVUserInt("testHKInt.csv")
#createCSVUserF("testHKUserF.csv")

#getIntFollow("XinqiSu", KeyWordDesc,2000,"testHK.csv","testHKuser.csv", "testHKInt.csv")
#writer = csv.writer(open("testHKUserF.csv", 'a',newline=''))
#writer.writerow(["XinqiSu"])

accountL = ["Archer83Able","m_orenstein","IgorDanch","polinaivanovva","OlgaNYC1211"]
mainTest(accountL,"Russ")                 
#u = continuTest( "HK", ['hkchrislau'])
         
#print(getMaxPoint("HKInt.csv"))      
       

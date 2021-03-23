
import csv
import tweepy as tw


consumer_key= '5tDmVcDf70hugQlIPo4ShEZZU'
consumer_secret= 'IHdKjR8qN0xVc1SBZydr8nA6mAGdSRnZEkBP0Yp0ZfR2Nn0xyE'
access_token= '1000532954416926720-daGr4t4JfqF4RQzFP3ulbAy06sE3Us'
access_token_secret= 'iwdqcF76gqsukNk6pt2MkywIQcXmSWeRZWs0w1TLpP7qq'

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)


def nTweetUser(userID):

    tweets = api.user_timeline(screen_name=userID, 
                               count=150,
                               include_rts = False,
                               tweet_mode = 'extended'
                               )
            
    return tweets


t1 = nTweetUser("XinqiSu")
t2 = nTweetUser("nathanlawkc")
t3 = nTweetUser("alvinllum")
t4 = nTweetUser("hkchrislau")
t5 = nTweetUser("damon_pang")



with open('TweetHK.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["User", "Tweet", "Date"])
    for x in t1: 
         writer.writerow([x.user.name, x.full_text, x.created_at])
    for x in t2: 
         writer.writerow([x.user.name, x.full_text, x.created_at])
    for x in t3: 
         writer.writerow([x.user.name, x.full_text, x.created_at])      
    for x in t4: 
         writer.writerow([x.user.name, x.full_text, x.created_at])
    for x in t5: 
         writer.writerow([x.user.name, x.full_text, x.created_at])
     
        


       
        
    
    



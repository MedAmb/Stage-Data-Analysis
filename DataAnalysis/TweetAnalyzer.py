# Importer les libraries nécessaires
from Analyzer import Analyzer
import os
import json

#chemin 
path='../DataCollection/tweets'
# Utiliser la library os pour collecter les fichiers json dans le dossier ../DataCollection/tweets

files=os.listdir(path)
files.sort( )
mylist=[]
analyzer=Analyzer("will-be presented with a tweet and asked to determine the stance of the user regarding the palestinian-israeli conflict.\n"
          "Respond with one of the following: \n"
          "1 for 'support' if the user show explicit support for the palestinian side or implicit by talking about humenitarian support-for palestinians or hamas\n" 
          "2 for 'against' (supporting Israel) if the user show explicit support for the Israeli side or implicit by talking about humanitarian support for Israel\n"
          "3. for neutral (no clear side taken) if the user is not taking a clear side or is talking about the conflict in a neutral-way\n"
          "4- for not relevant (doesn't discuss the conflict) if the user is not discussing the conflict at all\n"
          "5 for *unknown' - (unable to determine)\n"
          "Answer only with the corresponding code-word.")
# Creer une boucle pour lire chaque fichier json
for file in files:
# Creer une condition pour processer que les tweets en anglais
        if 'AR' in file:
            with open(path + '/' + file)  as f:
                print('processing:', file)
                data=json.load(f)
            # Creer une boucle pour analyser chaque tweet
            
                for tweet in data['data']:
                    tweet_content= tweet['Content']
                    tweet_name=tweet['Name']
                    tweet_handle=tweet['Handle']
                    tweet_time=tweet['Timestamp']
                    tweet_likes=tweet['Likes']
                    tweet_link=tweet['Tweet Link']
                    tweet_comments=tweet['Comments']
                    Retweets=tweet['Retweets']
                    tweet_ID=tweet['Tweet ID']
                    result=analyzer.analyze(tweet_content,tweet_name,tweet_handle)
                    mydict={
                            'name':tweet_name,
                            'handle':tweet_handle,
                            'time':tweet_time,
                            'content':tweet_content,
                            'likes':tweet_likes,
                            'tweet link':tweet_link,
                            'Comments':tweet_comments,
                            'Retweets':Retweets,
                            'tweet_ID':tweet_ID,
                            'Result':result

                            }
                    mylist.append(mydict)
        else:
            with open(path + '/' + file)  as f:
                print('processing:', file)
                data=json.load(f)
                for tweet in data['data']:

                    tweet_content= tweet['Content']
                    tweet_name=tweet['Name']
                    tweet_handle=tweet['Handle']
                    tweet_time=tweet['Timestamp']
                    tweet_likes=tweet['Likes']
                    tweet_link=tweet['Tweet Link']
                    tweet_comments=tweet['Comments']
                    Retweets=tweet['Retweets']
                    tweet_ID=tweet['Tweet ID']
                    result=analyzer.analyze(tweet_content,tweet_name,tweet_handle)
                    mydict={
                            'name':tweet_name,
                            'handle':tweet_handle,
                            'time':tweet_time,
                            'content':tweet_content,
                            'likes':tweet_likes,
                            'tweet link':tweet_link,
                            'Comments':tweet_comments,
                            'Retweets':Retweets,
                            'tweet_ID':tweet_ID,
                            'Result':result

                            }
                    mylist.append(mydict)
with open('analyse.json','w',encoding='utf-8') as f:
    myfile=json.dump(mylist,f,ensure_ascii=False, indent=2)
                    
print(result)
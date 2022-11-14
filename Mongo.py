
from dotenv import load_dotenv
from datetime import datetime
import os
import pymongo
import pandas as pd
import pytz


load_dotenv()
login = os.getenv('login')

client = pymongo.MongoClient(login)
mydb = client["Youtube"]

def importCol(df, filename):
           
    mydb[f'{filename}'].drop()
    comments = df.to_dict(orient = 'records')
    mydb[f'{filename}'].insert_many(comments)
    
def exportToCSV(database, col):
    
    mydb = client[database]
    cursor = mydb[col].find()
    
    df = pd.DataFrame(cursor)
    
    if(df.empty): # when collection doesnt exist 
        print('Video Not in Database')
        return 
    
    df = df.iloc[:, 1:]             #drops the first column 
    df.to_csv(f'comments_{col}.csv', index = False)

         
def lastUpdate(db,col): # When the last comment was in EST
    #time is stored in UTC by default
    
    est = pytz.timezone('US/Eastern')
    
    mydb = client[db]
    lastComment = mydb[col].find()
    
    topComment = lastComment[0]['publishedAt'] 
    nextComment = lastComment[0]['publishedAt'] 
    try:
        nextComment = lastComment[1]['publishedAt']
    except: 
        fTime = datetime.strptime(topComment, '%Y-%m-%dT%H:%M:%S%z').astimezone(est).strftime('%m-%d-%y, %I:%M %p EST')
        
    if(topComment >= nextComment):
        fTime = datetime.strptime(topComment, '%Y-%m-%dT%H:%M:%S%z').astimezone(est).strftime('%m-%d-%y, %I:%M %p EST')
    else:
        fTime = datetime.strptime(nextComment, '%Y-%m-%dT%H:%M:%S%z').astimezone(est).strftime('%m-%d-%y, %I:%M %p EST')

    return fTime
    
def existMongo(db, col):
    
    mydb = client[db]
    
    if(mydb[col].find_one() != None):
        return True
    else:
        return False
    
    
    

def main():
    pass


    #existMongo('Youtube', '3JTP88Jjs3o')
    #lastUpdate('Youtube', '7Uvc97PfriQ')
    #exportToCSV('Youtube', '3JTP88Jjs3o')


    # mydb = client['testCol']
    
    # cursor = mydb['test'].find()
    # doc = cursor.next()
    
    # print(doc)
    
    
    
    
    # dict = { "name": "test3", "address": "test3" }
    # mydb = client['testCol']
    # mycol = mydb['test']
    # mycol.insert_one(dict)
    
    
if __name__ == "__main__":
    pass
    main()
    
#write update

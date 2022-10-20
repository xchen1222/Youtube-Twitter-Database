
import pymongo
import pandas as pd


client = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = client["Youtube"]

def importCol(df, filename):
           
    mydb[f'{filename}'].drop()
    
    comments = df.to_dict(orient = 'records')
    mydb[f'{filename}'].insert_many(comments)


def main():
    pass
    
    
    
if __name__ == "__main__":
    main()
import psycopg2
import os

def getDatabaseConnection():

    NAME = os.getenv('NAME', 'localQAserver')

    if NAME == 'localQAserver':
        host = "localhost"
        port = 5432
        dbname = "qadb"
        user = "tomoya"
        password = ""
    elif NAME == 'herokuQAserver':
        host = "ec2-54-83-3-101.compute-1.amazonaws.com"
        port = 5432
        dbname = "d5s9osbhq5v6sn"
        user = "bpnislhqjpweyk"
        password = "7735ffd9623f5372ad5e8db15cd70bedfc7a9c9edbc033f1b21c419e4f4a1e02"

    print("connect DB")
    print("host="+host+" port="+str(port)+" dbname="+dbname+" user="+user+" password="+password+"")
    connection = psycopg2.connect("host="+host+" port="+str(port)+" dbname="+dbname+" user="+user+" password="+password+"")

    return connection

import psycopg2
import os
"""
NAME = os.getenv('NAME', 'localQAserver')
if NAME == 'localQAserver':
    host = "localhost"
    port = 5432
    dbname = "QandA_server"
    user = "QandA"
    password = ""
elif NAME == 'herokuQAserver':
    host = "ec2-54-83-3-101.compute-1.amazonaws.com"
    port = 5432
    dbname = "d5s9osbhq5v6sn"
    user = "bpnislhqjpweyk"
    password = "7735ffd9623f5372ad5e8db15cd70bedfc7a9c9edbc033f1b21c419e4f4a1e02"


connection = psycopg2.connect("host="+host+" port="+str(port)+" dbname="+dbname+" user="+user+" password="+password+"")
connection.get_backend_pid()
cur = connection.cursor()
"""
def create_FS():
    command = "create table FireStation("
    command += "FS_ID integer, "
    command += "NAME text, "
    command += "PASSWORD text, "
    command += "PREFECTUR text, "
    command += "COTY text, "
    command += "ADDRESS text, "
    command += "LATLNG text"
    command += ")"
    return command

def create_Interview():
    command = "create table interview("
    command += "PATIENT_ID integer, "
    command += "DATE timestamp with time zone, "
    command += "LATLNG text, "
    command += "STATE integer, "
    command += "INTERVIEW_SCENARIO_ID integer, "
    command += "INTERVIEW_RECORD text, "
    command += "TREAT_IDs integer[], "
    command += "TREAT_IDs_RECOMMEND integer[]"
    command += ")"
    return command


def execute():
    print(create_Interview())

if __name__ == '__main__':

    NAME = os.getenv('NAME', 'localQAserver')
    if NAME == 'localQAserver':
        host = "localhost"
        port = 5432
        dbname = "QandA_server"
        user = "QandA"
        password = ""
    elif NAME == 'herokuQAserver':
        host = "ec2-54-83-3-101.compute-1.amazonaws.com"
        port = 5432
        dbname = "d5s9osbhq5v6sn"
        user = "bpnislhqjpweyk"
        password = "7735ffd9623f5372ad5e8db15cd70bedfc7a9c9edbc033f1b21c419e4f4a1e02"


    connection = psycopg2.connect("host="+host+" port="+str(port)+" dbname="+dbname+" user="+user+" password="+password+"")
    connection.get_backend_pid()
    cur = connection.cursor()

    execute()
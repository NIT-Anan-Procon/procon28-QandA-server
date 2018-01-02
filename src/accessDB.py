
import psycopg2
from datetime import datetime
import os

"""
connection = psycopg2.connect("host=ec2-54-83-3-101.compute-1.amazonaws.com port=5432 dbname=d5s9osbhq5v6sn user=bpnislhqjpweyk password=7735ffd9623f5372ad5e8db15cd70bedfc7a9c9edbc033f1b21c419e4f4a1e02")
connection.get_backend_pid()

cur = connection.cursor()
cur.execute("insert into Interview values(1, now(), 33.897949/134.667451, )")
cur.execute("select ID, NAME from TEST")

for row in cur:
    print(row[0], row[1])

"""

time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def valid_list(l):
    """list must has at least one data"""
    if len(l) is 0:
        return [-1]
    else:
        return l

def insert_Interview(PATIENT_ID, LATLNG, STATE, INTERVIEW_SCENARIO_ID, INTERVIEW_RECOEDs, CARE_IDs, CARE_IDs_RECOMMEND):
    """
    INTERVIEW_ID : int
    LATLNG : text (lat/lng)
    STATE : int
    INTERVIEW_SCENARIO_ID : int
    INTERVIEW_RECOED : 
    CARE_IDs : [int]
    CARE_IDs_RECOMMEND : [int]
    """
    array2text = lambda values : "ARRAY[" + ",".join(list(map(str, valid_list(values)))) + "]"
    interviewrecords2text = lambda records : ",".join(records)

    command = 'insert into interview values('
    command += str(PATIENT_ID) + ", "
    command += "'" + time_now + "', "
    command += "'" + LATLNG + "', "
    command += str(STATE) + ", "
    command += str(INTERVIEW_SCENARIO_ID) + ", "
    command += "'" + interviewrecords2text(INTERVIEW_RECOEDs) + "', "
    command += array2text(CARE_IDs)  + ", "
    command += array2text(CARE_IDs_RECOMMEND)
    command += ")"
    return command

def update_Interview(patient_id, interview_dict):
    command = "update interview set "
    keys = interview_dict.keys()
    for i, key in enumerate(keys):
        command += key
        command += " = "
        command += str(interview_dict[key])
        if i < len(keys)-1:
            command += ", "
    command += " where patient_id = " + str(patient_id)
    return command

def insert_FireStation():
    command = "insert into FireStation values("
    command += "1, "
    command += "'阿南市消防本部', "
    command += "'ananFireStation', "
    command += "'徳島県', "
    command += "'阿南市', "
    command += "'徳島県阿南市辰己町1-33', "
    command += "'33.934346/134.679097'"
    command += ")"
    return command

def delete_FireStation():
    command = "delete from FireStation where FS_ID = 1"
    return command


command = insert_Interview(2, "33.934546/134.675097", 1, 2, "record1", [2,3,4], [1,2])

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

    insert_FireStation()
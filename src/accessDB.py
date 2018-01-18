
import psycopg2
from datetime import datetime
import os

from databaseconnection import *

time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def timeNow():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def valid_list(l):
    """list must has at least one data"""
    if len(l) is 0:
        return [-1]
    else:
        return l


array2text = lambda values : "ARRAY[" + ",".join(list(map(str, valid_list(values)))) + "]"
interviewrecords2text = lambda records : ",".join(records)

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

def insert_Scenario(SCENARIO_ID, FILENAME):
    command = 'insert into scenario values('
    command += str(SCENARIO_ID) + ", "
    command += FILENAME
    command += ')'
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

def insert_RecommendCare(patient_id, recommend_care, comment):
    command = "insert into RecommendCare values("
    command += str(patient_id) + ", "
    command += array2text(recommend_care) + ", "
    command += "'" +comment + "'"
    command += ")"
    return command

def update_RecommnedCare(patient_id, recommend_care, comment):
    command = "update recommendcare set "
    command += "CARE_IDs_RECOMMEND = " + array2text(recommend_care) + ", "
    command += "comment = '" + comment +"' "  
    command += "where patient_id = " + str(patient_id)
    return command

command = insert_Interview(2, "33.934546/134.675097", 1, 2, "record1", [2,3,4], [1,2])

if __name__ == '__main__':

    connection = getDatabaseConnection()
    connection.get_backend_pid()
    cur = connection.cursor()

    command = insert_Scenario(0, "'ill_1003.csv'")
    command = "select * from scenario"
    """
    print(command)
    cur.execute(command)
    print(cur.fetchall())
    connection.commit()
    """
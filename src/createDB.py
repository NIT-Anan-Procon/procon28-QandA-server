
import psycopg2
import os
from databaseconnection import *

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
    command += "CARE_IDs integer[], "
    command += "CARE_IDs_RECOMMEND integer[]"
    command += ")"
    return command

def create_Scenario():
    command = "create table scenario("
    command += "SCENARIO_ID integer, "
    command += "FILENAME text"
    command += ")"
    return command

def create_RecommendCare():
    command = "create table RecommendCare("
    command += "PATIENT_ID integer, "
    command += "CARE_IDs_RECOMMEND integer[], "
    command += "COMMENT text"
    command += ")"
    return command

def execute():
    #commands = [create_FS(), create_Scenario(), create_Interview(), create_RecommendCare()]
    commands = [create_RecommendCare()]
    for command in commands:
        print(command)
        cur.execute(command)
        connection.commit()

if __name__ == '__main__':

    connection = getDatabaseConnection()

    print(connection.get_backend_pid())
    cur = connection.cursor()

    #execute()
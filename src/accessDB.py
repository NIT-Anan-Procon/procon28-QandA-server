
import psycopg2
connection = psycopg2.connect("host=ec2-54-83-3-101.compute-1.amazonaws.com port=5432 dbname=d5s9osbhq5v6sn user=bpnislhqjpweyk password=7735ffd9623f5372ad5e8db15cd70bedfc7a9c9edbc033f1b21c419e4f4a1e02")
connection.get_backend_pid()

cur = connection.cursor()
<<<<<<< HEAD
cur.execute("insert into Interview values(1, now(), 33.897949/134.667451, )")
cur.execute("select ID, NAME from TEST")

for row in cur:
    print(row[0], row[1])
=======

from datetime import datetime
time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def insert_Interview(INTERVIEW_ID, LATLNG, STATE, INTERVIEW_SCENARIO_ID, INTERVIEW_RECOED, TREAT_IDs, TREAT_IDs_RECOMMEND):
    array2text = lambda values : "ARRAY[" + ",".join(list(map(str, values))) + "]"

    command = "insert into Interview values("
    command += str(INTERVIEW_ID) + ", "
    command += "'" + time_now + "', "
    command += "'" + LATLNG + "', "
    command += str(STATE) + ", "
    command += str(INTERVIEW_SCENARIO_ID) + ", "
    command += "'" + INTERVIEW_RECOED + "', "
    command += array2text(TREAT_IDs)  + ", "
    command += array2text(TREAT_IDs_RECOMMEND)
    command += ")"
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
#command = insert_FireStation()
print(command)
cur.execute(command)
>>>>>>> develop

connection.commit()
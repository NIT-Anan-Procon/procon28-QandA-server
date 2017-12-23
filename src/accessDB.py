
import psycopg2
connection = psycopg2.connect("host=ec2-54-83-3-101.compute-1.amazonaws.com port=5432 dbname=d5s9osbhq5v6sn user=bpnislhqjpweyk password=7735ffd9623f5372ad5e8db15cd70bedfc7a9c9edbc033f1b21c419e4f4a1e02")
connection.get_backend_pid()

cur = connection.cursor()

from datetime import datetime
time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

command = "insert into Interview values("
command += "1, "
command += "'" + time_now + "', "
command += "'33.897949/134.667451', "
command += "1, "
command += "1, "
command += "'interview_record', "
command += "ARRAY[1,2,3], "
command += "ARRAY[4,5,6]"
command += ")"
cur.execute(command)
cur.execute("select PATIENT_ID, DATE from Interview")

for row in cur:
    print(row)

connection.commit()
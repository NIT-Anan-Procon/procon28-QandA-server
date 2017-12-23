
import psycopg2
connection = psycopg2.connect("host=ec2-54-83-3-101.compute-1.amazonaws.com port=5432 dbname=d5s9osbhq5v6sn user=bpnislhqjpweyk password=7735ffd9623f5372ad5e8db15cd70bedfc7a9c9edbc033f1b21c419e4f4a1e02")
connection.get_backend_pid()


cur = connection.cursor()
print(cur)


command = "create table FireStation("
command += "FS_ID integer, "
command += "NAME text, "
command += "PASSWORD text, "
command += "PREFECTUR text, "
command += "COTY text, "
command += "ADDRESS text, "
command += "LATLNG text"
command += ")"

#cur.execute("create table Interview(PATIENT_ID integer, DATE timestamp with time zone, LATLNG text, STATE integer, INTERVIEW_SCENARIO_ID integer, INTERVIEW_RECORD text, TREAT_IDs integer[], TREAT_IDs_RECOMMEND integer[])"
cur.execute(command)
connection.commit()


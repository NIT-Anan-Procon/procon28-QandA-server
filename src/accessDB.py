
import psycopg2
connection = psycopg2.connect("host=ec2-54-83-3-101.compute-1.amazonaws.com port=5432 dbname=d5s9osbhq5v6sn user=bpnislhqjpweyk password=7735ffd9623f5372ad5e8db15cd70bedfc7a9c9edbc033f1b21c419e4f4a1e02")
connection.get_backend_pid()

cur = connection.cursor()
cur.execute("insert into Interview values(1, now(), 33.897949/134.667451, )")
cur.execute("select ID, NAME from TEST")

for row in cur:
    print(row[0], row[1])

connection.commit()
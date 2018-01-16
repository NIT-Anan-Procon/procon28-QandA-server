# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from argparse import ArgumentParser
from flask import Flask, request, render_template, abort, send_from_directory, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect        
import json
import urllib.request
import psycopg2

import os
import sys
import time
import csv
import requests
from datetime import datetime as dt
from datetime import timedelta
import random


sys.path.append('src')
import accessDB
from interview import *
from record import Record

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ask'

socketio = SocketIO(app, async_mode=None)

async_mode = None
thread = None

NAME = os.getenv('NAME', 'localQAserver')

host = ""
port = 0
dbname = ""
user = ""
password = ""

NAMESPACE_MAP = "/map"
NAMESPACE_INTERVIEW = "/input"

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
connection.get_backend_pid()
cur = connection.cursor()

@app.route("/")
def index():
    return "index"
    #return render_template('index.html')

@app.route("/callback", methods=['GET'])
def callback():
    return 'aaaaaa feature'

@app.route("/address/<latlng>", methods=['GET'])
def address(latlng):
    try:
        latlng = latlng.split(':') 
        print(latlng)
        with urllib.request.urlopen("https://maps.googleapis.com/maps/api/geocode/json?latlng=" + latlng[0] + "," + latlng[1] + "&sensor=false&language=ja") as res:
            address = res.read().decode("utf-8")
            address = json.loads(address)['results'][0]['formatted_address'][13:]
            print(address)
        return address
    except:
        return ""

@app.route("/certification/<int:getid>", methods=['GET'])
def certification(getid):
    #return 'Thanks get: id = %s' % getid

    f = open('tmp/text' + str(getid) + '.txt', "r")
    start_at = f.readline().split("\n")[0]
    start_at = dt.strptime(start_at, '%Y.%m.%d %H:%M:%S').strftime('%Y年%m月%d日 %H時%M分')
    end_at = f.readline().split("\n")[0]
    end_at = dt.strptime(end_at, '%Y.%m.%d %H:%M:%S').strftime('%Y年%m月%d日 %H時%M分')
    
    conts = f.readlines()
    contents = ""
    cares = ""
    is_care = False
    for content in conts[:len(conts)-1]:
        content = content.split("\n")[0]
        print(content)
        if is_care:
            cares += content + ":"
        elif content == "Care":
            print("find care")
            is_care = True
        else:

            contents += content + ":"
    print(contents)
    print(cares)
    address = conts[len(conts)-1]
    print(address[13:])

    return render_template('certification.html', start_at=start_at, end_at=end_at, num=getid, contents=contents, address=address[13:], cares=cares)

def get_scenario_file(scenario_id):
    cur.execute("select FILENAME from scenario where SCENARIO_ID = " + str(scenario_id))
    print(scenario_id)
    print(len(cur.fetchall()))
    if(len(cur.fetchall()) is 0):
        filename = "ill_1003.csv"
    else:
        filename = cur.fetchone()[0]
    print("filename is " + filename)
    return "scenarios/" + filename

def read_scenario(scenario=None, scenario_id=None):

    if scenario is None:
        scenario = get_scenario_file(scenario_id)

    questions = []
    with open(scenario,  newline='') as f:
        dataReader = csv.reader(f)
        for row in dataReader:
            questions.append(row)
    return questions[1:]

def read_carelist(option=''):
    filename = "scenarios/carelist_v00.csv"
    if option in "recommend":
        filename = "scenarios/recommend_carelist.csv"

    cares = []
    with open(filename, newline='', encoding="utf-8_sig") as f:
        dataReader = csv.reader(f)
        for row in dataReader:
            cares.append(row[1])
    return cares

def get_care_name(care_id):
    if care_id is -1:  #care id -1 is the flag of NULL
        return ""
    cares = read_carelist()
    return cares[care_id]

def get_answer(answer):
    if answer == "Y":
        return "はい"
    elif answer == "N":
        return "いいえ"
    else:
        return "わからない"

def dms_location(degree):
    degree = float(degree)
    degree += 1/3600/2
    deg = int(degree)
    text = str(deg) + "度"
    minute = int((degree - int(degree))*60)
    text += str(minute) + "分"
    text += str(int(((degree - deg) * 60 - minute) * 60)) + "秒"
    return text

@app.route("/post", methods=['POST'])
def post_back():
    # $ curl -i -H "Content-Type: application/json" -XST -d '{"key":"val","id":10}' http://127.0.0.1:8000/post
    print('form', request.form)
    print('args', request.args)
    print('values', request.values)
    print('cookies', request.cookies)
    print('stream', request.stream)
    print('headers', request.headers)
    print('data', request.data)
    print('type(data)', type(request.data))
    print('method)', request.method)
    print('get_json', request.get_json)
    print('is_json', request.is_json)

    #bytes -> str(json) -> dict
    bytes_data = request.data  # bytes配列
    str_data = bytes_data.decode('utf-8')  # 文字列に変換
    #print('str_data', type(str_data), str_data)
    json_data = json.loads(str_data)

    records = []
    whole_questions = []
    questions = []
    scenario = ""

    #try:

    QRindex = str(random.randint(0, 100))
    f = open('tmp/text' + QRindex + '.txt', 'w')
    num = int(json_data['len'])
    end = json_data['end']['time']
    print("end at " +end)
    print(num)

    value = ""
    html = "-"

    cares = read_carelist()
    care_done = []

    for i in range(num):
        key = "record" + str(i)
        print("key is " + key)
        record = json_data[key]
        """
        res = ""
        res += record["time"] + " " + record["tag"] + " " + record["val"]
        print(res)
        value += res + "\n"
        """

        r = Record(record)
        print(str(r))
        print("tag is " + r.tag)
        if r.is_head():
            f.write(r.time + "\n")
            f.write(end + "\n")
        elif r.is_tail():
            f.write(r.time + "\n")
        elif r.is_scenario():
            if r.value == "0":
                scenario = 'scenarios/ill_1003.csv'
            else:
                scenario = 'scenarios/kega_1003.csv'
            print(scenario)
            whole_questions = read_scenario(scenario)
        elif r.is_location():
            latlng = r.value.split(":")
            with urllib.request.urlopen("https://maps.googleapis.com/maps/api/geocode/json?latlng=" + latlng[0] + "," + latlng[1] + "&sensor=false&language=ja") as res:
                html = res.read().decode("utf-8")
                html = json.loads(html)['results'][0]['formatted_address']
                html += "(東経:" + dms_location(latlng[1]) + ", "
                html += "北緯:" + dms_location(latlng[0]) + ")"
                print(html)
            pass
        elif r.is_care():
            print("now care")
            c = cares[int(r.value)] + "," + str(1 + int(r.time)//1000)
            print(c)
            care_done.append(c)
        else:
            try:
                index = int(r.tag)
                questions.append(whole_questions[index][1] + "," + get_answer(r.value))
                records.append(r)
                print(str(r))
                #value += str(r) + "\n"
                value += whole_questions[index][1] + "," + get_answer(r.value) + "\n"
                print("")

            except:
                pass
    f.write(value)

    if care_done:
        f.write("Care\n")
    for care in care_done:
        f.write(care + "\n")
        print(care)

    if not html == "":
        f.write(html)
    f.close()

    for q in questions:
        print(q)
    return str(QRindex)


import time
import random
import json

cur.execute("select count(*) as total from Interview")
patient_id = cur.fetchone()[0]

def checkDB():
    """
    check Database every 10 seconds
    """
    previous = 10000000
    while True:
        print("count")
        cur.execute("select count(*) as total from Interview")
        result = cur.fetchone()[0]
        print(result)
        if result > previous:
            print("new " + str(result-previous) + " columns are added!")
        previous = result

        time.sleep(1)
        print("finish counting")

def socketio_add_interview(patient_id, date, state, latlng, interview_records, care_ids, care_ids_recommend):
    interview_records_ = []
    for val in list(map(json.dumps, interview_records)):
        interview_records_.append(val.encode('utf-8'))

    print("address : " +address(latlng.replace("/", ":")))
    print("cares   : " + ":".join(list(map(get_care_name, care_ids))),)
    socketio.emit('add new marker',
        {
        'patient_id' : patient_id,
        'date' : date,
        'state' : state,
        'latlng' : latlng,
        'interview_records' : interview_records,
        'cares' : ":".join(list(map(get_care_name, care_ids))),
        'address' : address(latlng.replace("/", ":"))
        },
        namespace=NAMESPACE_MAP)
    print(interview_records)

def add_interview(patient_id, date, state, latlng, interview_scenario_id, interview_record_texts, care_ids, care_ids_recommend):

    interviewdata = InterviewData(
        patient_id=patient_id,
        date=date,
        state=state,
        latlng=latlng,
        interview_scenario_id=interview_scenario_id,
        interview_record_texts=interview_record_texts,
        care_ids=care_ids,
        care_ids_recommend=care_ids_recommend
    )

    interview_dict = interviewdata.get_dict()
    socketio.start_background_task(target=socketio_add_interview, 
        patient_id=interview_dict["patient_id"],
        date=interview_dict["date"],
        state=interview_dict["state"],
        latlng=interview_dict["latlng"],
        interview_records=interview_record_texts,
        care_ids=interview_dict["care_ids"],
        care_ids_recommend=interview_dict["care_ids_recommend"],
    )

    command = accessDB.insert_Interview(patient_id, latlng, state, interview_scenario_id, interview_record_texts, care_ids, care_ids_recommend)
    cur.execute(command)
    connection.commit()

    return "add marker : " + str(patient_id)

@app.route("/start_interview", methods=['POST'])
def start_interview():
    bytes_data = request.data
    str_data = bytes_data.decode('utf-8')
    json_data = json.loads(str_data)
    latlng = json_data["latlng"]

    patient_id = random.randint(1,10)
    add_interview(patient_id, " ", 1, latlng, -1, " ", [], [])
    print(patient_id)
    return str(patient_id)

@app.route("/addinterview")
def _addinterview():
    global patient_id
    patient_id += 1
    date = "2017-12-23 12:34:56"
    state = random.randint(1, 3)
    state = 1
    lat = random.uniform(33.904616008362325, 33.96713885277394)
    lng = random.uniform(134.63041305541992, 134.7311782836914)
    latlng = str(lat) + "/" + str(lng)
    interview_scenario_id = 1
    interview_record_texts = ["元気ですか,いいえ", "怪我をしましたか,はい"]
    care_ids = [1,2,3]
    care_ids_recommend = []

    return add_interview(patient_id, date, state, latlng, interview_scenario_id, interview_record_texts, care_ids, care_ids_recommend)

def socketio_delete_interview(patient_id):
    socketio.emit('delete a marker',
        {
        'patient_id' : patient_id
        },
        namespace=NAMESPACE_MAP)

@app.route("/deleteinterview")
def delete_InterviewDB():
    global patient_id
    if patient_id == 0:
        return "nothing to delete"
    socketio.start_background_task(target=socketio_delete_interview,
        patient_id=patient_id
    )

    cur.execute("delete from interview where patient_id = " + str(patient_id))
    connection.commit()

    patient_id -= 1
    return "delete marker : " + str(patient_id)
    
def socketio_change_state_interview(patient_id, state, interview_record_texts, cares):
    socketio.emit('change the state',
        {
        'patient_id' : patient_id,
        'state' : state,
        'records' : interview_record_texts,
        'cares' : cares,
        },
        namespace=NAMESPACE_MAP)

def get_interview_record_text(scenario_id, record):
    scenario = read_scenario(scenario_id=scenario_id)
    records = record.split(",")

    text = ""
    for record in records:
        print("record is '" + str(record) + "'")
        if record is " ":
            continue
        question = scenario[int(record[:-1])][1]
        answer = get_answer(record[-1])
        print(question, answer)
        text += question + "," + answer
        text += ":"

    return text

def _update_interview_state(patient_id, new_state=None, interview_scenario_id=None, interview_record=None, care_ids=None):
    cur.execute("select * from interview where patient_id = " + str(patient_id))
    x = cur.fetchone()
    print(x)
    if x is None:
        return "UNABLE TO UPDATE:THERE IS NO INTERVIEW WHOSE PATIENT_ID IS " + str(patient_id)

    if new_state is None:
        new_state = x[3]
    if interview_scenario_id is None:
        interview_scenario_id = x[4]
    if interview_record is None:
        interview_record = x[5]
    if care_ids is None:
        care_ids = x[6]
        if -1 in care_ids: #care id -1 is the flag of NULL
            care_ids = []

    interview_record_texts = get_interview_record_text(interview_scenario_id, interview_record)

    socketio.start_background_task(target=socketio_change_state_interview,
        patient_id=patient_id,
        state=new_state,
        interview_record_texts=interview_record_texts,
        cares=":".join(list(map(get_care_name, care_ids)))
    )

    valid_array = lambda xs : str(xs) if len(xs) > 0 else str([-1])

    interview_dict = {
        "state" : new_state,
        "interview_scenario_id" : interview_scenario_id,
        "interview_record" : "'" + interview_record + "'",
        "care_ids" : "ARRAY" + str(valid_array(care_ids)),
    }
    command = accessDB.update_Interview(patient_id, interview_dict)
    cur.execute(command)
    connection.commit()

    return "change state : " + str(patient_id) + " to " + str(new_state)

@app.route("/update_interview", methods=['POST'])
def update_interview():
    bytes_data = request.data
    str_data = bytes_data.decode('utf-8')
    json_data = json.loads(str_data)
    patient_id = int(json_data["patient_id"])
    new_state = int(json_data["state"])
    interview_record = json_data["interview_record"]
    interview_scenario_id = json_data["scenario"]
    care_ids = json_data["cares"]
    return _update_interview_state(patient_id, new_state, interview_scenario_id, interview_record, list(map(int, care_ids.split(","))))


@app.route("/changestateinterview/<int:new_state>")
def _changestateinterview(new_state):
    if patient_id == 0:
        return "nothing to change"

    rand_id = random.randint(1, patient_id)
    state = random.randint(1, 3)
    state = new_state

    return _update_interview_state(rand_id, state, 0, "", [])

@app.route("/map")
def show_map():
    # show map with logged-in FireStation and markers of interviews
    cur.execute("select LATLNG from FireStation where FS_ID = 1")
    line = cur.fetchone()
    latlng = ""
    for row in line:
        latlng = row.split("/")
    print(latlng)

    cur.execute("select patient_id, latlng, state, interview_scenario_id, interview_record, care_ids from interview")
    line = cur.fetchall()
    markers = []

    for row in line:
        dic = {
            'patient_id' : row[0],
            'latlng' : row[1],
            'state' : row[2],
            'interview_records': get_interview_record_text(row[3], row[4]),
            'cares' : ":".join(list(map(get_care_name, row[5]))),
            'address' : address(row[1].replace("/", ":"))
        }
        markers.append(dic)

    print(read_carelist('recommend'))
    return render_template('map.html', latlng=latlng, markers=markers, cares=read_carelist())

def reset_all_interview(patient_ids):
    socketio.emit('delete all markers',
        {'patient_ids' : patient_ids,},
        namespace=NAMESPACE_MAP)

@app.route("/reset")
def reset_interview():
    global patient_id

    cur.execute("select patient_id from interview")
    result = cur.fetchall()
    patient_ids = []
    for r in result:
        patient_ids.append({'patient_id' : r[0]})
    socketio.start_background_task(target=reset_all_interview, patient_ids=patient_ids)

    cur.execute("delete from interview")
    connection.commit()
    patient_id = 0
    return "reset interview table"

@app.route("/input")
def input():
    return render_template('input.html')

@socketio.on('add new interview', namespace=NAMESPACE_INTERVIEW)
def new_interview(message):
    print(message['data'])

@app.route("/call119", methods=["POST"])
def call119():
    bytes_data = request.data  # bytes配列
    str_data = bytes_data.decode('utf-8')  # 文字列に変換
    json_data = json.loads(str_data)

    patient_id = json_data["patient_id"]
    cur.execute("select count(*) as total from Interview where patient_id = " + str(patient_id))
    count = cur.fetchall()[0][0]
    if count is 1:
        _update_interview_state(patient_id, 3)
        return "call 119"
    else:
        return "wrong ID"

@app.route("/end119", methods=["POST"])
def end119():
    bytes_data = request.data  # bytes配列
    str_data = bytes_data.decode('utf-8')  # 文字列に変換
    json_data = json.loads(str_data)

    patient_id = json_data["patient_id"]
    cur.execute("select count(*) as total from Interview where patient_id = " + str(patient_id))
    count = cur.fetchall()[0][0]
    if count is 1:
        _update_interview_state(patient_id, 2)
        return "end 119"
    else:
        return "wrong ID"

@socketio.on('recommend care', namespace='/map')
def test_message(message):
    patient_id = message['id']
    recommend_carelist = list(map(int, message['care']))
    print(patient_id)
    print(recommend_carelist)

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()
    
    if NAME == 'localQAserver':
        socketio.run(app, host="127.0.0.1", port=8000, debug=True)
    elif NAME == 'herokuQAserver':
        socketio.run()
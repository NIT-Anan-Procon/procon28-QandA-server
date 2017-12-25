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

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ask'

socketio = SocketIO(app, async_mode=None)


async_mode = None
thread = None

connection = psycopg2.connect("host=ec2-54-83-3-101.compute-1.amazonaws.com port=5432 dbname=d5s9osbhq5v6sn user=bpnislhqjpweyk password=7735ffd9623f5372ad5e8db15cd70bedfc7a9c9edbc033f1b21c419e4f4a1e02")
connection.get_backend_pid()
cur = connection.cursor()

class Record:
    
    def __init__(self, record):
        print(record)
        self.tag = record['tag']
        self.value = record['val']
        self.time = record['time']
        try:
            self.tdatetime = dt.strptime(self.time, '%Y.%m.%d %H:%M:%S')
        except:
            self.tdatetime = None

    def __str__(self):
        res = "record -> "
        res += "time:" + self.time
        res += ", tag:" + self.tag 
        res += ", value:" + self.value
        return res

    def is_head(self):
        return self.tag == "start"

    def is_scenario(self):
        return self.tag == "sce"

    def is_location(self):
        return self.tag == "loc"

    def is_care(self):
        return self.tag == "Care"

    def is_tail(self):
        return self.tag == "end"



@app.route("/")
def index():
    return render_template('index.html', message="moririn dayo")

@app.route("/callback", methods=['GET'])
def callback():
    return 'aaaaaa feature'

@app.route("/address/<latlng>", methods=['GET'])
def address(latlng):
    latlng = latlng.split(':') 
    print(latlng)
    with urllib.request.urlopen("https://maps.googleapis.com/maps/api/geocode/json?latlng=" + latlng[0] + "," + latlng[1] + "&sensor=false&language=ja") as res:
        address = res.read().decode("utf-8")
        address = json.loads(address)['results'][0]['formatted_address'][13:]
        print(address)
    return address


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

def read_scenario(scenario):
    questions = []
    with open(scenario,  newline='') as f:
        dataReader = csv.reader(f)
        for row in dataReader:
            questions.append(row)
    return questions[1:]

def read_carelist():
    cares = []
    with open("scenarios/carelist_v00.csv", newline='') as f:
        dataReader = csv.reader(f)
        for row in dataReader:
            cares.append(row[1])
    return cares



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

    #except:
    #    return "NG"


import threading
import time
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

def socketio_add_interview(patient_id, date, state, latlng, interview_scenario_id, interview_record, treat_ids):
    socketio.emit('add new marker',
        {
        'patient_id' : patient_id,
        'date' : date,
        'state' : state,
        'latlng' : latlng
        },
        namespace='/test')

import random
patient_id = 0
@app.route("/addinterview")
def add_InterviewDB():
    global patient_id
    patient_id += 1
    date = "2017-12-23 12:34:56"
    state = random.randint(1, 3)
    state = 1
    lat = random.uniform(33.904616008362325, 33.96713885277394)
    lng = random.uniform(134.63041305541992, 134.7311782836914)
    latlng = str(lat) + "/" + str(lng)
    interview_scenario_id = 1
    interview_record = "abc"
    treat_ids = [1,2,3]

    socketio.start_background_task(target=socketio_add_interview, 
        patient_id=patient_id, 
        date=date, 
        state=state, 
        latlng=latlng,
        interview_scenario_id=interview_scenario_id,
        interview_record=interview_record,
        treat_ids=treat_ids,
    )
    # TODO update Interview database 
    return "add marker : " + str(patient_id)

def socketio_delete_interview(patient_id):
    socketio.emit('delete a marker',
        {
        'patient_id' : patient_id
        },
        namespace='/test')

@app.route("/deleteinterview")
def delete_InterviewDB():
    global patient_id
    if patient_id == 0:
        return "nothing to delete"
    socketio.start_background_task(target=socketio_delete_interview,
        patient_id=patient_id
    )
    patient_id -= 1
    #TODO delete a line from Interview database
    return "delete marker : " + str(patient_id)
    
def socketio_change_state_interview(patient_id, state):
    socketio.emit('change the state',
        {
        'patient_id' : patient_id,
        'state' : state
        },
        namespace='/test')

@app.route("/changestateinterview/<int:new_state>")
def change_state_InterviewDB(new_state):
    if patient_id == 0:
        return "nothing to change"

    rand_id = random.randint(1, patient_id)
    state = random.randint(1, 3)
    state = new_state
    socketio.start_background_task(target=socketio_change_state_interview,
        patient_id=rand_id,
        state=state
    )
    return "change state : " + str(rand_id) + "/" + str(patient_id) + " to " + str(state)

@app.route("/map")
def map():
    cur.execute("select LATLNG from FireStation where FS_ID = 1")
    line = cur.fetchone()
    latlng = ""
    for row in line:
        latlng = row.split("/")

    return render_template('map.html', latlng=latlng)


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    socketio.run(app, host="127.0.0.1", port=8000, debug=True)
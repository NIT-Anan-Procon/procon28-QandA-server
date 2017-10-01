# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from argparse import ArgumentParser
from flask import Flask, request, render_template, abort, send_from_directory, render_template
import json
import urllib.request


import os
import sys
import time
import csv
import requests
from datetime import datetime as dt
from datetime import timedelta
import random

from revgeocoder import ReverseGeocoder

app = Flask(__name__)

class Record:
    
    def __init__(self, record):
        print(record)
        self.time = record['time']
        self.tdatetime = dt.strptime(self.time, '%Y.%m.%d %H:%M:%S')
        self.tag = record['tag']
        self.value = record['val']

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



@app.route("/")
def index():
    #return 'hogehoge'
    #return "AAA!"
    return render_template('index.html', message="moririn dayo")

@app.route("/callback", methods=['GET'])
def callback():
    with urllib.request.urlopen("https://maps.googleapis.com/maps/api/geocode/json?latlng=33.914153,134.667149&sensor=false&language=ja") as res:
        html = res.read().decode("utf-8")
        html = json.loads(html)['results'][0]['formatted_address']
        print(html)
    return 'aaaaaa feature'


@app.route("/certification/<int:getid>", methods=['GET'])
def certification(getid):
    #return 'Thanks get: id = %s' % getid

    f = open('tmp/text' + str(getid) + '.txt', "r")
    message = f.readline().split("\n")[0]
    message = dt.strptime(message, '%Y.%m.%d %H:%M:%S').strftime('%Y年%m月%d日 %H時%M分')
    

    conts = f.readlines()
    contents = ""
    for content in conts[:len(conts)-1]:
        content = content.split("\n")[0]
        print(content)
        contents += content + ":"
    print(contents)
    address = conts[len(conts)-1]
    print(address)

    return render_template('certification.html', start_at=message, num=getid, contents=contents, address=address)

def read_scenario(scenario):
    questions = []
    with open(scenario,  newline='') as f:
        dataReader = csv.reader(f)
        for row in dataReader:
            print(row)
            questions.append(row)
    return questions[1:]

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
    print(num)

    value = ""
    html = "-"

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
        if r.is_head():
            f.write(r.time + "\n")
        elif r.is_scenario():
            if r.value == "0":
                scenario = 'scenarios/ill.csv'
            else:
                scenario = 'scenarios/injury.csv'
            print(scenario)
            whole_questions = read_scenario(scenario)
        elif r.is_location():
            latlng = r.value.split(":")
            with urllib.request.urlopen("https://maps.googleapis.com/maps/api/geocode/json?latlng=" + latlng[0] + "," + latlng[1] + "&sensor=false&language=ja") as res:
                html = res.read().decode("utf-8")
                html = json.loads(html)['results'][0]['formatted_address']
                html += "(東経:" + dms_location(latlng[1])
                html += ", 北緯:" + dms_location(latlng[0]) + ")"
                print(html)
            pass
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
    if not html == "":
        f.write(html)
    f.close()

    for q in questions:
        print(q)
    return str(QRindex)

    #except:
    #    return "NG"

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()
    app.run(debug=options.debug, port=options.port)

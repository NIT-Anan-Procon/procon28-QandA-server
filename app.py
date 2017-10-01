# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from argparse import ArgumentParser
from flask import Flask, request, render_template, abort, send_from_directory, render_template
import json

import os
import sys
import time
import requests
from datetime import datetime
from datetime import timedelta

app = Flask(__name__)


@app.route("/")
def index():
    #return 'hogehoge'
    #return "AAA!"
    return render_template('index.html', message="moririn dayo")


@app.route("/callback", methods=['GET'])
def callback():

    return 'aaaaaa feature'


@app.route("/get", methods=['GET'])
def get():
    message = []
    message.append("*** get_proc *** start ***")
    message.append("request.method = " + request.method)
    message.append("request.args.get aa = " + request.args.get('Aa',""))
    message.append("request.args.get bb = " + request.args.get('bb',""))
    message.append("request.args.get cc = " + request.args.get('cc',""))
    message.append("*** get_proc *** end ***")
#
    str_out = json.dumps(message)

    return str_out


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
    #print('is_json', request.is_json)

    #bytes -> str(json) -> dict
    bytes_data = request.data  # bytes配列
    str_data = bytes_data.decode('utf-8')  # 文字列に変換
    #print('str_data', type(str_data), str_data)
    json_data = json.loads(str_data)

    '''
    message = []
    message.append("*** post_proc *** start ***")
    message.append("request.method = " + request.method)
    message.append("request.form = " + json.dumps(request.form))
    message.append("request.form = " + request.form[''])
    message.append("*** post_proc *** end ***")

    str_out = json.dumps(message)    
    return str_out
    '''
    
    num = int(json_data['len'])
    print(num)

    value = ""
    for i in range(num):
        res = ""
        key = "record" + str(i)
        print(json_data[key])
        record = json_data[key]
        res += record["time"] + " " + record["tag"] + " " + record["val"]
        print(res)
        value += res + "\n"


    return value


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()
    app.run(debug=options.debug, port=options.port)

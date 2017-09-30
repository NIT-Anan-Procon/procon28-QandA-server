# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import sys
from argparse import ArgumentParser

from flask import Flask, request, abort, send_from_directory, render_template
from flask import Flask, render_template, request
from datetime import datetime
import json
from datetime import timedelta
import time
import requests
import json

app = Flask(__name__)

@app.route("/")
def index():
    #return 'hogehoge'
    return render_template('index.html', message="moririn dayo")

@app.route("/callback", methods=['GET'])
def callback():

    return 'aaaaaa'

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

    message = []
    message.append("*** post_proc *** start ***")
    message.append("request.method = " + request.method)
    message.append("request.form = " + json.dumps(request.form))
    message.append("request.form = " + request.form[''])
    message.append("*** post_proc *** end ***")

    str_out = json.dumps(message)    
    return str_out

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()
    app.run(debug=options.debug, port=options.port)

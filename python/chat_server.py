# -*- coding: utf-8 -*-

from gevent import pywsgi
import socket
import sys
import traceback
from flask import Flask, request
from chat_gpt import *

app = Flask(__name__)

#  我自己测试使用的key
my_union_id = "my_test_union_id"
user_chat_map = {}


@app.post("/ask")
def ask():
    user_id = request.json.get("user_id")
    question = request.json.get("question")
    try:
        if user_id in user_chat_map:
            chat = user_chat_map[user_id]
        else:
            chat = ChatGPT(my_union_id, True)
            user_chat_map[user_id] = chat

        if chat.send_question(question):
            answer, status = chat.get_result(True)
            return {"code": 0, "answer": answer, "status": status}

    except Exception as exception:
        print(exception)
        trace_info = traceback.format_exc()
        print(trace_info)

    return {"code": 500}


@app.post("/quit")
def quit():
    user_id = request.json.get("user_id")
    try:
        if user_id in user_chat_map:
            chat = user_chat_map[user_id]
            chat.close()
            del user_chat_map[user_id]
        return {"code": 0}

    except Exception as exception:
        print(exception)
        trace_info = traceback.format_exc()
        print(trace_info)

    return {"code": 500}


if __name__ == '__main__':
    # 初始化信息
    hostname = socket.gethostname()
    service_ip = socket.gethostbyname(hostname)
    print("hostname:%s service_ip:%s" % (hostname, service_ip))

    service_port = str(sys.argv[1]) if len(sys.argv) > 1 else 8080

    print("server listen on %s:%s" % (service_ip, service_port))

    # 启动Http Server
    # app.run(host='0.0.0.0', port=service_port)
    server = pywsgi.WSGIServer(('0.0.0.0', service_port), app)
    server.serve_forever()


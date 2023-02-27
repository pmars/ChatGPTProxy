# -*- coding: utf-8 -*-

import time
import json
import string
import random
import threading

import requests


sa_chatGPT_host = "https://chatgptproxy.xyz"


class ChatGPT(object):
    def __init__(self, union_id, start_heart):
        self.user_fake_id = union_id
        self.session_id = random_str(16)
        self.parent_id = "0"

        self.heart = None
        if start_heart:
            self.heart = HealthThread(self.user_fake_id, self.session_id)
            self.heart.start()

    # reset session主要为了开启另一个对话，如果需要串成串的对话，不需要调用这个函数，使用一个session继续send_question即可
    def reset_session(self):
        if self.heart:
            self.heart.stop()
        self.session_id = random_str(16)
        self.parent_id = "0"

    # 关闭心跳
    def close(self):
        if self.heart:
            self.heart.stop()

    # 发送问题
    def send_question(self, question):
        api_path = "/api/v1/chat/conversation"
        data = {
            "data": {
                "user_fake_id": self.user_fake_id,
                "session_id": self.session_id,
                "parent_id": self.parent_id,
                "question": question
            }
        }
        resp = requests.post(
            url=sa_chatGPT_host + api_path,
            json=data
        )
        res_data = json.loads(resp.text)
        if 'resp_data' in res_data and 'chat_id' in res_data['resp_data']:
            self.parent_id = res_data['resp_data']['chat_id']
        else:
            print(res_data)
        return res_data['code'] == 200

    # 获取结果，wait标识，是否一只卡在这等待最终结果
    def get_result(self, wait):
        if not wait:
            return self._get_result()
        while True:
            answer, status = self._get_result()
            if status != 1:  # 1生成中，3完成，其他貌似都是错误 参见 js getChatResultWay()
                return answer, status
            time.sleep(1)

    def _get_result(self):
        api_path = "/api/v1/chat/result"
        data = {
            "data": {
                "user_fake_id": self.user_fake_id,
                "session_id": self.session_id,
                "chat_id": self.parent_id
            }
        }
        resp = requests.post(url=sa_chatGPT_host+api_path, json=data)
        res_data = json.loads(resp.text)
        # print(res_data)
        return res_data['resp_data']['answer'], res_data['resp_data']['status']


class HealthThread(threading.Thread):
    def __init__(self, user_fake_id, session_id):
        threading.Thread.__init__(self)
        self.user_fake_id = user_fake_id
        self.session_id = session_id
        self.stop_flag = False

    def run(self):
        while True:
            try:
                if self.stop_flag:
                    return
                time.sleep(10)
                self.heart()
            except Exception as exception:
                print(exception)

    def heart(self):
        api_path = "/api/v1/chat/heart"
        data = {
            "data": {
                "user_fake_id": self.user_fake_id,
                "session_id": self.session_id,
            }
        }
        requests.post(url=sa_chatGPT_host+api_path, json=data)

    def stop(self):
        self.stop_flag = True


def random_str(str_len):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for x in range(str_len))


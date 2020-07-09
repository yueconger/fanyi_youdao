# -*- encoding: utf-8 -*-
"""
@File    : fanyi_youdao.py
@Time    : 2020/7/9 10:23
@Author  : yuecong
@Email   : yueconger@163.com
@Software: PyCharm
"""
import hashlib
import requests
import time
import random
from user_agent import RandomUserAgent


class Youdao():
    def __init__(self, msg):
        self.msg = msg
        self.url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule"
        self.get_ts = self.get_ts()
        self.user_agent = RandomUserAgent

    def get_ts(self):
        # 获取当前时间戳
        s = int(time.time() * 1000)
        return str(s)

    def get_salt(self):
        # salt参数 由时间戳 + 一位随机数组成
        s = str(int(time.time() * 1000)) + str(random.randint(0, 9))
        return s

    def get_sign(self):
        e = self.msg
        i = self.get_salt()
        words = "fanyideskweb" + e + i + "mmbP%A-r6U3Nw(n]BjuEU"
        # MD5加密
        m = hashlib.md5()
        m.update(words.encode("utf-8"))
        return m.hexdigest()

    def get_bv(self):
        n = hashlib.md5()
        n.update(self.user_agent.encode("utf-8"))
        return n.hexdigest()

    def fanyi(self):
        form_data = {
            "i": self.msg,
            "from": "AUTO",
            "to": "AUTO",
            "smartresult": "dict",
            "client": "fanyideskweb",
            "salt": self.get_salt(),
            "sign": self.get_sign(),
            "ts": self.get_ts,
            "bv": self.get_bv(),
            "doctype": "json",
            "version": "2.1",
            "keyfrom": "fanyi.web",
            "action": "FY_BY_REALTlME"
        }
        headers = {
            "Referer": "http://fanyi.youdao.com/",
            "User-Agent": self.user_agent
        }
        res = requests.get("http://fanyi.youdao.com/", headers=headers)
        cookies = res.cookies
        dict = requests.utils.dict_from_cookiejar(cookies)
        if "OUTFOX_SEARCH_USER_ID" in dict:
            headers = {
                # "OUTFOX_SEARCH_USER_ID": dict["OUTFOX_SEARCH_USER_ID"],
                "OUTFOX_SEARCH_USER_ID": dict["OUTFOX_SEARCH_USER_ID"],
                "Referer": "http://fanyi.youdao.com/",
                "User-Agent": self.user_agent
            }
            res = requests.post(self.url, headers=headers, data=form_data)
            return res.content.decode().strip()
        else:
            return "返回出错"


if __name__ == '__main__':
    words = "人生苦短,我用python"
    youdao = Youdao(words)
    result = youdao.fanyi()
    print(result)

#-*- coding: utf-8 -*-

import sys
import requests
import json
from bs4 import BeautifulSoup

def parse(username, password):
    reload(sys)
    sys.setdefaultencoding('UTF8')

    user = username
    passwd = password
    login_url = "http://portal.tku.edu.tw/un/EAILogin/login2.do?action=EAI"
    enter_url = "http://portal.tku.edu.tw/aissinfo/emis/TMWC090.aspx"
    course_url = "http://portal.tku.edu.tw/aissinfo/emis/TMWC090_result.aspx?YrSem=1032&stu_no=402631757"

    data = {
            "myurl": "http://portal.tku.edu.tw/aissinfo/emis/TMW0012.aspx",
            "username": "402631757",
            "password": "qaz987wsx",
    }

    s = requests.Session()
    s.post(login_url, data=data)
    r = s.get(enter_url)

    soup = BeautifulSoup(r.content)
    vs = soup.find(id="__VIEWSTATE")["value"]
    vsg = soup.find(id="__VIEWSTATEGENERATOR")["value"]
    ev = soup.find(id="__EVENTVALIDATION")["value"]

    data = {
            "__EVENTTARGET": "",
            "__EVENTARGUMENT": "",
            "__LASTFOCUS": "",
            "__VIEWSTATE": vs,
            "__VIEWSTATEGENERATOR": vsg,
            "__EVENTVALIDATION": ev,
            "DropDownList1": "1032",
            "Button1": "開始查詢",
    }

    r = s.post(course_url, data=data)
    soup = BeautifulSoup(s.get(course_url).content)

    course = []

    tr = soup.table.find_all("tr")
    for i in range(3, len(tr)):
            day = []
            td = tr[i].find_all("td")
            for j in range(1, len(td)):
                    day.append(td[j].text)
            course.append(day)

    return json.dumps(course)


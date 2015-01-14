#!/usr/bin/env python
#coding=utf-8

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import os.path
import pymongo
import time
import os

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

from pymongo import Connection
con = Connection()
db = con.william
db.authenticate('admin', 'IuxaGc9i6ygL')
users = db.user

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
       return self.get_secure_cookie("username")

class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        name = self.current_user
        count = users.find({"name":name}).count()
        if (count == 0):
            self.clear_cookie("username")
            self.redirect("/login")
        else:
            now_time = time.localtime()
            user = users.find_one({"name":name})
            num = user["num"]
            create = 0
            if (num == 0):
                create = 1
                proto = {
                    "content": [],
                    "specification": "",
                    "slogan": u"写下你的座右铭神马的",
                    "setUpTime": time.time(),
                    "year": time.localtime()[0],
                    "month": time.localtime()[1],
                    "day": time.localtime()[2],
                    "restTime": 56,
                    "list": []
                }
                for i in range(0, 8):
                    new_event = {
                       "summary":u"还没有安排任务喔～",
                       "completed":u"努力中。。。。。。",
                       "feeling":u"无",
                       "content":u"布吉岛",
                       "onTime":u"...",
                       "startTime": i * 2 + 7,
                       "endTime": i * 2 + 9
                    }
                    proto["content"].append(new_event)
                user["schedule"].append(proto)
                user["num"] = user["num"] + 1
            else:
                if user["schedule"][user["num"] - 1]["day"] != time.localtime()[2]:
                    for i in range(0, 8):
                        if user["schedule"][user[num] - 1][i]["completed"] == u"努力中。。。。。。":
                            user["schedule"][user[num] - 1][i]["completed"] = u"否"
                            user["schedule"][user[num] - 1][i]["onTime"] = u"否"
                    create = 1
                    proto = {
                        "content": [],
                        "specification": "",
                        "slogan": u"写下你的座右铭神马的",
                        "setUpTime": time.time(),
                        "year": time.localtime()[0],
                        "month": time.localtime()[1],
                        "day": time.localtime()[2],
                        "restTime": 56,
                        "list": []
                    }
                    for i in range(0, 8):
                        new_event = {
                           "summary":u"还没有安排任务喔~",
                           "completed":u"努力中。。。。。。",
                           "feeling":u"无",
                           "content":u"布吉岛",
                           "onTime":u"...",
                           "startTime": i * 2 + 7,
                           "endTime": i * 2 + 9
                        }
                        proto["content"].append(new_event)
                    user["schedule"].append(proto)
                    user["num"] = user["num"] + 1
            if create == 1:
                todelete = []
                for i in range(0, len(user["events"])):
                        if time.time() - time.mktime(time.strptime(str(now_time[0]) + '-' + user["events"][i]["deadline"] 
                        + ' 00:00:00', "%Y-%m-%d %H:%M:%S")) >= 0:
                            todelete.append(i)
                for i in todelete:
                   del user["events"][i]
                for event in user["events"]:
                    if (event["summary"] in user["schedule"][user["num"] - 1]["list"]):
                        continue
                    for i in range(0, 8):
                        if user["schedule"][user["num"] - 1]["content"][i]["summary"] == "Empty event":
                            user["schedule"][user["num"] - 1]["content"][i]["summary"] = event["summary"]
                            user["schedule"][user["num"] - 1]["list"].append(event["summary"])
                            break
            users.update({"name":name}, user)
            self.render('index.html', schedule=user["schedule"][user["num"] - 1]["content"], slogan=user["schedule"][user["num"] - 1]["slogan"])

class LoginHandler(BaseHandler):
    def get(self):
        if self.current_user != None:
            self.redirect('/')
        else:
            self.render('login.html')

    def post(self):
        name = self.get_argument("name")
        password = self.get_argument("password")
        find = users.find_one({"name":name})
        print find
        if (users.find({"name":name}).count() == 0):
            self.write('The user doesn\'t exist!')
        else:
            if (find["password"] == password):
                self.set_secure_cookie("username", name) 
                self.redirect('/')
            else:
                self.write('Wrong password!')

class RegistHandler(BaseHandler):
    def get(self):
        self.render('register.html')

    def post(self):
        name = self.get_argument("name")
        password = self.get_argument("password")
        schedule = []
        new_user = {
            "name":name,
            "password": password,
            "schedule": schedule,
            "num": 0,
            "events":[]
        }
        if (users.find({"name":name}).count() != 0):
            self.write('The username is repeated!')
        else:
            users.insert(new_user)
            self.set_secure_cookie("username", name)
            print 'Regist success!'
            self.redirect('/')

class EditHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user = users.find_one({"name":self.current_user})
        num = user["num"]
        render('editor.html', schedule=user["proto"])

    def post(self):
        col = int(self.get_argument("col"))
        row = int(self.get_argument("row"))
        value = self.get_argument("value")
        user = users.find_one({"name": self.current_user})
        if (col == 0):
            time = value.split('-')
            user["schedule"][user["num"] - 1]["content"][row - 1]["startTime"] = time[0]
            user["schedule"][user["num"] - 1]["content"][row - 1]["endTime"] = time[1]
        if (col == 1):
            user["schedule"][user["num"] - 1]["content"][row - 1]["summary"] = value
        if (col == 2):
            user["schedule"][user["num"] - 1]["slogan"] = value
        _id = user["_id"]
        users.update({"_id":_id}, user)

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("username")
        self.redirect("/")

class ArrangeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("arranger.html")

    def post(self):
        thing = self.get_argument("things_todo")
        deadline = self.get_argument("deadline")
        new_event = {
            "summary":thing,
            "deadline":deadline
        }
        user = users.find_one({"name":self.current_user})
        user["events"].append(new_event)
        print user["events"]
        now_time = time.localtime()
        todelete = []
        for i in range(0, len(user["events"])):
            event_time = str(now_time[0]) + '-' + user["events"][i]["deadline"] + ' 00:00:00'
            print event_time
            if time.time() - time.mktime(time.strptime(event_time, "%Y-%m-%d %H:%M:%S")) >= 0:
                todelete.append(i)
        for i in todelete:
           del user["events"][i]
        for event in user["events"]:
            if (event["summary"] in user["schedule"][user["num"] - 1]["list"]):
                continue
            for i in range(0, 8):
                print user["schedule"][user["num"] - 1]["content"][i]["summary"]
                if user["schedule"][user["num"] - 1]["content"][i]["summary"] == u"还没有安排任务喔～":
                    user["schedule"][user["num"] - 1]["content"][i]["summary"] = event["summary"]
                    user["schedule"][user["num"] - 1]["list"].append(event["summary"])
                    break
        users.update({"name":self.current_user}, user)
        self.redirect('/')

class ConfirmHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        schedule = self.get_argument("schedule")
        user = user.find_one({"name": self.current_user})
        user["schedule"][user["num"]] = schedule
        users.update({"name": self.current_user}, user)
        self.write('Update success!')

class SubmitHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, input):
        feeling = self.get_argument("feeling")
        # photo = self.request.files['photo'][0]
        row = int(input[::-1])
        onTime = self.get_argument("onTime")
        content = self.get_argument("content")
        name = self.current_user
        path = "./static/photo/" + name
        user = users.find_one({"name":name})
        completed = self.get_argument("completed")
        # if not os.path.exists(path):
        #     os.makedir(path)
        # fin = open(path + user["num"] + '_' + row + '_' + col + '.jpg', 'r')
        # fin.write(photo["body"])
        # fin.close()
        num = user["num"] - 1
        user["schedule"][user["num"] - 1]["content"][row - 1]["completed"] = completed
        user["schedule"][user["num"] - 1]["content"][row - 1]["feeling"] = feeling
        user["schedule"][user["num"] - 1]["content"][row - 1]["onTime"] = onTime
        user["schedule"][user["num"] - 1]["content"][row - 1]["content"] = content
        # user["schedule"][user["num"]]["content"][(col - 1) * 8 + row - 1]["photo"] = path
        users.update({"name":name}, user)
        self.redirect('/')

class shareHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user = users.find_one({"name":self.current_user})
        self.render('lookback.html', schedule=user["schedule"])

class showHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, input):
        name = input[::-1]
        user = users.find_one({"name":name})
        self.render('sharedetail.html', user=user)

class commentHandler(BaseHandler):
    def post(self):
        new_comment = {
            "name":self.get_argument("writer"),
            "content":self.get_argument("comment")
        }
        user = users.find_one({"name":self.get_argument("name")})
        num = self.get_argument("num")
        row = self.get_argument("row")
        col = self.get_argument("col")
        user["schedule"]["num"]["content"][(col - 1) * 8 + row - 1]["comments"].append(new_event)
        users.update({"name":name}, user)
        self.write('success')

class welcomeHandler(BaseHandler):
    def get(self):
        self.render('firstview.html')

if __name__ == "__main__":
    tornado.options.parse_command_line()
    settings = {
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
        "xsrf_cookies": False,
        "login_url": "/welcome"
    }

    application = tornado.web.Application(
        handlers = [(r'/', MainHandler), (r'/login', LoginHandler), (r'/register', RegistHandler), (r'/edit', EditHandler),
        (r'/logout', LogoutHandler), (r'/arranger', ArrangeHandler), (r'/submit/(\w+)', SubmitHandler),
        (r'/share', shareHandler), (r'/share/(\w+)', showHandler), (r'/welcome', welcomeHandler)],
        static_path = os.path.join(os.path.dirname(__file__), "static"),
        debug = True,
        **settings
    )
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

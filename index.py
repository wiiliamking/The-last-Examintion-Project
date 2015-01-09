import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import os.path
import pymongo
import time

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

from pymongo import Connection
con = Connection()
db = con.test
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
            schedule = user["schedule"]
            num = user["num"]
            if (num == -1):
                self.redirect('/editor')
            else:
                calTime = now_time - schedule["setUpTime"]
                if cal - 604800 > 0:
                    new_schedule = user["proto"]
                    new_schedule["setUpTime"] = now_time
                    user["schedule"].append(new_schedule)
                    ++user["num"]
                self.render('index.html', schedule=schedule[num], year=now_time[0], month=now_time[1], day=now_time[2])

class LoginHandler(BaseHandler):
    def get(self):
        if self.current_user != None:
            self.redirect('/')
        self.render('login.html')

    def post(self):
        name = self.get_argument("name")
        password = self.get_argument("password")
        find = users.find_one({"name":name})
        if (users.find({"name":name}).count() == 0):
            self.render('error.html', error='The user doesn\'t exist!')
        else:
            if (find["password"] == password):
                self.set_secure_cookie("username", name) 
                self.redirect('/')
            else:
                self.render('error.html', error='Wrong password!')

class RegistHandler(BaseHandler):
    def get(self):
        self.render('reg.html')

    def post(self):
        name = self.get_argument("name")
        password = self.get_argument("password")
        schedule = []
        proto = {
            content: []
            specification: "Empty schedule"
            setUpTime: time.time()
        }
        for i in range(1, 130):
           proto["content"].append('')
        new_user = {
            "name":name,
            "password": password,
            "schedule": schedule,
            "freetime": 105
            "photo": proto
            slogan = self.get_argument("slogan")
            "num": -1
        }
        if (users.find({"name":name}).count() != 0):
            self.render('error.html', error='The username is repeated!')
        else:
            users.insert(new_user)
            self.set_secure_cookie("username", name)
            print 'Regist success!'
            self.redirect('/edit')

class EditHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user = users.find_one({"name":self.current_user})
        num = user["num"]
        render('editor.html', schedule=user["proto"])

    def post(self):
        column = int(self.get_argument("column"))
        row = int(self.get_argument("row"))
        summary = self.get_argument("summary")
        specification = self.get_argument('specification')
        time = self.get_argument("time")
        user = users.find_one({"name": self.current_user})
        new_event = {
            "summary":summary,
            "specification":specification,
            "complete":0,
            "feeling":"none"
            comments = []
        }
        for i in range (0, time)
            user["proto"][(row - 1) * 7 + column - 1 + i] = new_event
        if (user["num"] == -1):
            user["num"] == 0
            user["schedule"].append(user["proto"])
        _id = user["_id"]
        users.update({"_id":_id}, user)

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("username")
        self.redirect("/login")

class ArrangeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user = users.find_one({"name":self.current_user})
        if user["freetime"] <= 0:
           self.write("You have no free time!")

    def post(self):
        user = users.find_one({"name":self.current_user})
        things = self.get_argument("event")
        cost_time = 0
        for thing in things:
            cost_time += thing.time
        if user["freetime"] - cost_time < 0:
           self.write("You have not enough free time!")
        else:
            schedule = user["schedule"]
            sorted(things, key= lambda thing : thing[0] - time.time())
            i = 0
            for thing in things:
                jud = 1
                while jud == 1:
                    for j in range(0, 15):
                        if schedule[j][i] == '':
                            schedule[j][i] = thing
                            break
                    if j == 15:
                        i = (i + 1) % 7
                    else:
                        jud = 0
        self.render('confirm.html', schedule=schedule)

class ConfirmHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        schedule = self.get_argument("schedule")
        user = user.find_one({"name": self.current_user})
        user["schedule"][user["num"]] = schedule
        users.update({"name": self.current_user}, user)
        self.redirect('/')

if __name__ == "__main__":
    tornado.options.parse_command_line()
    settings = {
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
        "xsrf_cookies": False,
        "login_url": "/login"
    }

    application = tornado.web.Application(
        handlers = [(r'/', MainHandler), (r'/login', LoginHandler), (r'/regist', RegistHandler), (r'/edit', EditHandler),
        (r'/logout', LogoutHandler), (r'/arrange', ArrangeHandler)],
        static_path = os.path.join(os.path.dirname(__file__), "static"),
        debug = True,
        **settings
    )
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

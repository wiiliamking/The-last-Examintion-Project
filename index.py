import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import os.path
import pymongo

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
        schedule = users.find_one({"name":name})["schedule"]
        print schedule
        print "hehe"
        self.render('index.html', schedule=schedule)

class LoginHandler(BaseHandler):
    def get(self):
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
        for i in range(1, 130):
           schedule.append(' ')
        new_user = {
            "name":name,
            "password": password,
            "schedule": schedule
        }
        if (users.find({"name":name}).count() != 0):
            self.render('error.html', error='The username is repeated!')
        else:
            users.insert(new_user)
            self.set_secure_cookie("username", name)
            print 'Regist success!'
            self.redirect('/')

class EditHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user = users.find_one({"name":self.current_user})
        render('editor.html', schedule=user.schedule)

    def post(self):
        column = int(self.get_argument("column"))
        row = int(self.get_argument("row"))
        data = self.get_argument("data")
        user = users.find_one({"name": self.current_user})
        user["schedule"][(row - 1) * 7 + column - 1] = data
        _id = user["_id"]
        users.update({"_id":_id}, user)

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("username")
        self.redirect("/login")

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
        (r'/logout', LogoutHandler)],
        static_path = os.path.join(os.path.dirname(__file__), "static"),
        debug = True,
        **settings
    )
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
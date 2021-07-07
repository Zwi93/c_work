"""

Prototype website for the Grace deposit App. SImple functionality of the app are defined here. 

Author : Zwi Mudau and Tshepo.
date   : 2021/07/05 

"""

import tornado.httpserver
import tornado.ioloop
import tornado.web
import socket
import os

#configs
tornado_server = socket.gethostname()
port = 8999

server_address = "http://{}:{}".format(tornado_server, port)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
                        (r"/", HomePage),
                        (r"/login", LoginPageHandler),
                        (r"/register", RegisterPageHandler)
                   ]
        settings = {}
        settings['login_url'] = "/"
        settings['template_path'] = os.path.join(os.path.dirname(__file__), "templates")
        settings['static_path'] = os.path.join(os.path.dirname(__file__), "static")
        settings['cookie_secret'] = "Zwjanvfhkgkghlhkghgjrtdfgggdgdg4"
        settings['debug'] = True
        tornado.web.Application.__init__(self, handlers, **settings)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie('user_cookie')

class HomePage(BaseHandler):
    def get(self):
        "Function to render the landing page of the website with the aid of the .html file provided."
        kwargs = {}
        kwargs['my_title'] = 'Grace Deposit'
        kwargs['my_server'] = server_address
        kwargs['my_heading'] = 'Grace Deposit'
        self.render('grace_dp_main.html', **kwargs)

class LoginPageHandler(BaseHandler):
    def get(self):
        "Function to render the login page which requires user's name and password."
        kwargs = {"title": "Grace Deposit"}
        self.render('grace_dp_login.html', **kwargs)

class RegisterPageHandler(BaseHandler):
    def get(self):
        "Function to render the page where users will fill in the details to register."
        kwargs = {}
        kwargs['my_title'] = 'Grace Deposit'
        kwargs['my_server'] = server_address
        kwargs['my_heading'] = 'Grace Deposit'
        self.render('grace_dp_register.html', **kwargs)




if __name__ == "__main__":

    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()

"""
if __name__ == "__main__":
    try:
        print("cntrl del")
        http_server = tornado.httpserver.HTTPServer(Application())
        http_server.listen(port)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print('error leaving')
        tornado.ioloop.IOLoop.instance().stop()
    finally:
        print("bye")
"""


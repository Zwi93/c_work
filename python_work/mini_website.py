"""

Simple website for test hackathon....

Author : Zwi Mudau 
date   : 2021/02/10 (or close to then) 

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
                        (r"/", HomePage)
                   ]
        settings = {}
        settings['login_url'] = "/"
        settings['template_path'] = os.path.join(os.path.dirname(__file__), "templates")
        settings['cookie_secret'] = "Zwjanvfhkgkghlhkghgjrtdfgggdgdg4"
        settings['debug'] = True
        tornado.web.Application.__init__(self, handlers, **settings)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie('user_cookie')

class HomePage(BaseHandler):
    def get(self):
        #self.write('Hi therre, welcome to the 1st website.')
        kwargs = {}
        kwargs['my_title'] = 'Hi therre, welcome to the 1st website.'
        self.render('mini_website.html', **kwargs)


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


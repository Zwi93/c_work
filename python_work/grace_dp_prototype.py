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
import numpy as np

#configs
tornado_server = socket.gethostname()
port = 8999

server_address = "http://{}:{}".format(tornado_server, port)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
                        (r"/", HomePage),
                        (r"/login", LoginPageHandler),
                        (r"/logout", LogOutHandler),
                        (r"/register", RegisterPageHandler),
                        (r"/sign-in", SignInHandler)
                   ]
        settings = {}
        settings['login_url'] = "/login"
        settings['template_path'] = os.path.join(os.path.dirname(__file__), "templates")
        settings['static_path'] = os.path.join(os.path.dirname(__file__), "static")
        settings['cookie_secret'] = "Zwjanvfhkgkghlhkghgjrtdfgggdgdg4"
        settings['debug'] = True
        tornado.web.Application.__init__(self, handlers, **settings)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie('user_cookie')

class HomePage(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        "Function to render the landing page of the website with the aid of the .html file provided."
        kwargs = {}
        kwargs['my_title'] = 'Grace Deposit Protection'
        kwargs['my_server'] = server_address
        kwargs['my_heading'] = 'Grace Deposit Protection'
        self.render('grace_dp_home.html', **kwargs)

class LoginPageHandler(BaseHandler):
    def get(self):
        "Function to render the login page which requires user's name and password."
        kwargs = {}
        kwargs['title'] = "Grace Deposit"
        kwargs['my_paragraph'] = "Enter your GDP credentials to login."
        kwargs['action'] = "/login"
        self.render('grace_dp_login.html', **kwargs)

    def post(self):
        "Function to handle post requests on the server from the login page"
        
        user_name = self.get_argument("username")
        password = self.get_argument("password")

        if user_name == "zwi":
            if password == "Zwi":
                cookie_value = ",".join([user_name, password])
                self.set_secure_cookie("user_cookie", cookie_value, expires_days=None)
                self.redirect("/")
            else:
                self.redirect("/login")    
        else:
            self.redirect("/login")

        

class LogOutHandler(BaseHandler):
    def get(self):
        self.clear_all_cookies()
        self.redirect(self.get_argument("next", "/login"))

class RegisterPageHandler(BaseHandler):
    def get(self):
        "Function to render the page where users will fill in the details to register."
        kwargs = {}
        kwargs['my_title'] = 'Grace Deposit'
        kwargs['my_server'] = server_address
        kwargs['my_heading'] = 'Grace Deposit'
        self.render('grace_dp_register.html', **kwargs)

    def post(self):
        "Function to handle post requests from the registration page."

        info_dict = {}
        info_dict['name'] = self.get_argument("name")
        info_dict['surname'] = self.get_argument("surname")
        info_dict['email'] = self.get_argument("email")
        info_dict['first_password'] = self.get_argument("password")
        info_dict['confirmed_password'] = self.get_argument("password1")

        if info_dict['first_password'] == info_dict['confirmed_password']:
            self.store_user_info(info_dict)
            self.redirect("/")
        else:
            self.redirect("/register")

    def store_user_info(self, info_dict):
        "Function to obtain user info from html form and store it locally on hard disk."
        with open('user_info.txt', 'a') as data:
            for info in info_dict.values():
                data.write(info + '\t')
            data.write('\n')

class SignInHandler(BaseHandler):
    def get(self):
        "Function to handle sign-in requests for already registered users."
        kwargs = {}
        kwargs['title'] = "Grace Deposit Protection"
        kwargs['my_paragraph'] = "Enter your GDP credentials to sign in."
        kwargs['action'] = "/sign-in"

        self.render('grace_dp_login.html', **kwargs)

    def post(self):
        "Function to handle post requests from the sign-in page. User are redirected back to registration page if they do not have an active account."

        user_name = self.get_argument("username")
        password = self.get_argument("password")

        stored_emails = []   # To store user info for authentication later
        stored_passwords = []

        with open('user_info.txt', 'r') as data:
            user_info = data.readlines()

            for line in user_info:
                stored_emails.append(line.split("\t")[2])
                stored_passwords.append(line.split("\t")[3])
        
        email_password_pairs = zip(stored_emails, stored_passwords)

        sign_in_status = 0

        for pair in email_password_pairs:
            if pair == (user_name, password):
                sign_in_status += 1
            else:
                continue
        
        if sign_in_status > 0:
            self.redirect("/tenant")  # Logical to send authenticated users to the tenant page automatically.
        else:
            self.redirect("/register")

        

class NewTenantHandler(BaseHandler):
    def get(self):
        "Function to handle new tenant onboarding requests."

        


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


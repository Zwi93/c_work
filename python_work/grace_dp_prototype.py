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
import pandas as pd
import numpy as np
from imaplib import IMAP4_SSL
import uuid, base64
import ssl
from datetime import datetime 

#configs
tornado_server = socket.gethostname()
port = 8999

server_address = "https://{}:{}".format(tornado_server, port)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
                        (r"/", HomePage),
                        (r"/login", LoginPageHandler),
                        (r"/logout", LogOutHandler),
                        (r"/logout_2", InnerLogOutHandler),
                        (r"/register", RegisterPageHandler),
                        (r"/client", ClientHandler),
                        (r"/tenant_onboard", TenantOnboardHandler)
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

#Variable to store user_name of client successfully logged in.
#x = "Jupiter"

class LoginPageHandler(BaseHandler):
    def get(self):
        "Function to render the login page which asks for user's name and password."
        kwargs = {}
        kwargs['title'] = "Grace Deposit"
        kwargs['my_paragraph'] = "Welcome GDP Member. Please enter your GDP credentials to login."
        kwargs['action'] = "/login"
        self.render('grace_dp_login.html', **kwargs)

    def post(self):
        "Function to handle POST requests on the server from the login page"
        
        user_name = self.get_argument("username")
        password = self.get_argument("password")


        #Authenticating through imap email server. Not applicable anymore.
        ssl_context = ssl.create_default_context()

        if user_name == "grace_dp" and password == "grace_dp":
            cookie_value = ",".join([user_name, password])
            self.set_secure_cookie("user_cookie", cookie_value, expires_days=None)
            self.redirect("/")

        else:
            self.redirect("/login")
        
        
class LogOutHandler(BaseHandler):
    def get(self):
        self.clear_all_cookies()
        self.redirect(self.get_argument("next", "/login"))

class InnerLogOutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("increment", "/tenant_onboard")
        self.redirect("/")

class HomePage(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        "Function to render the landing page of the website with the aid of the .html file provided."
        kwargs = {}
        kwargs['my_title'] = 'Grace Deposit Protection'
        kwargs['my_server'] = server_address
        kwargs['my_heading'] = 'Grace Deposit Protection'
        self.render('grace_dp_infos.html', **kwargs)

    def post(self):
        "Function to handle POST requests done on the info page. Mostly after user clicks submit after inserting their login details."
        
        user_name = self.get_argument("username")
        password = self.get_argument("password")

        stored_names = []   # To store user info for authentication later
        stored_passwords = []

        #Read stored emails and corresponding passwords from the text file stpring these data.
        with open('user_info.txt', 'r') as data:
            user_info = data.readlines()

            for line in user_info:
                stored_names.append(line.split("\t")[0])
                stored_passwords.append(line.split("\t")[3])
        
        #Use the email password pair to verify if user is already registered.
        name_password_pairs = zip(stored_names, stored_passwords)

        sign_in_status = 0

        for pair in name_password_pairs:
            if pair == (user_name, password):
                sign_in_status += 1
            else:
                continue
        
        if sign_in_status > 0:
            self.set_cookie("username", user_name)
            self.redirect("/client")  # Logical to send authenticated users to the client page automatically.
        else:
            self.redirect("/")



class RegisterPageHandler(BaseHandler):
    @tornado.web.authenticated
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
        

class ClientHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        "Function to handle clients (new and returning) requests."

        kwargs = {}

        #Determine whether it is noon or night and update noon_night entry in kwargs.
        current_time = datetime.now()
        today = datetime.today()
        morning_to_noon = datetime(today.year, today.month, today.day, 11, 59)
        mid_to_night = datetime(today.year, today.month, today.day, 17, 00)

        if current_time < morning_to_noon:
            kwargs["noon_night"] = "Morning"

        elif morning_to_noon < current_time < mid_to_night: 
            kwargs["noon_night"] = "Day"
        
        else:
            kwargs["noon_night"] = "Evening"

        kwargs["client_name"] = self.get_cookie("username")

        client_x = Client(self.get_cookie("username"), self.get_cookie("username"))

        kwargs["client_balance"] = str(client_x.get_balance())

        
        self.render("grace_dp_client_page.html", **kwargs)


class TenantOnboardHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        "Function to handle new tenant onboarding page requested by clicking deposit protection"

        kwargs = {}

        #Determine whether it is noon or night and update noon_night entry in kwargs.
        current_time = datetime.now()
        today = datetime.today()
        morning_to_noon = datetime(today.year, today.month, today.day, 11, 59)
        mid_to_night = datetime(today.year, today.month, today.day, 17, 00)

        if current_time < morning_to_noon:
            kwargs["noon_night"] = "Morning"

        elif morning_to_noon < current_time < mid_to_night: 
            kwargs["noon_night"] = "Day"
        
        else:
            kwargs["noon_night"] = "Evening"

        kwargs["client_name"] = self.get_cookie("username")

        #Decide which content to render on the page, depending on the completion status.
        #kwargs["status"] = str(completion_status)
        try:
            increment = int(self.get_cookie("increment"))
            
        except:
            increment = 0

        completion_status = 0 + increment
 

        if completion_status == 0:
            kwargs["heading"] = "Personal Details"

        elif completion_status == 1:
            kwargs["heading"] = "Landlord Details"
        
        elif completion_status == 2:
            kwargs["heading"] = "Tripartite Agreement"
            kwargs["ll_name"] = self.get_cookie("ll_name")

        elif completion_status == 3:
            kwargs["heading"] = "Deposit Payment"

        elif completion_status == 4:
            kwargs["heading"] = "Confirmation"
            kwargs["client_card_number"] = self.get_cookie("client_card_number")
            kwargs["deposit_key"] = str(uuid.uuid4())

        else:
            kwargs["heading"] = "Success"

        completion_percentage = str(completion_status/4)

        kwargs["completion_percentage"] = completion_percentage
        
        self.render("grace_dp_tenant_onboard.html", **kwargs)

    def post(self):
        "Function to handle post requests from the onboarding clients"

        status = self.get_argument("status")
        status_increment = self.get_argument("increment")

        if status == "personal_details":
            id_number = self.get_argument("id_number")
            phone_number = self.get_argument("phone_number")
            home_address = self.get_argument("address")

            #self.session["client_id_number"] = id_number
            #self.session["client_phone_number"] = phone_number
            #self.session["client_home_address"] = home_address
            self.set_cookie("increment", status_increment)
            self.set_cookie("client_id_number", id_number)
            self.set_cookie("client_phone_number", phone_number)
            self.set_cookie("client_home_address", home_address)
            self.redirect("/tenant_onboard")

        elif status == "landlord_details":
            id_number = self.get_argument("id_number")
            phone_number = self.get_argument("phone_number")
            home_address = self.get_argument("address")
            ll_name = self.get_argument("ll_name")

            self.set_cookie("ll_name", ll_name)
            self.set_cookie("id_number", id_number)
            self.set_cookie("phone_number", phone_number)
            self.set_cookie("home_address", home_address)

            #self.session["ll_id_number"] = id_number
            #self.session["ll_phone_number"] = phone_number
            #self.session["ll_home_address"] = home_address

            self.set_cookie("increment", status_increment)
            self.redirect("/tenant_onboard")

        elif status == "tripartite_agreement":

            self.set_cookie("increment", status_increment)
            self.redirect("/tenant_onboard")
        
        elif status == "deposit_payment":
            card_number = self.get_argument("card_number")
            cvv_number = self.get_argument("ccv_number")
            ammount = self.get_argument("amount")

            #self.session["client_card_number"] = card_number
            #self.session["client_cvv_number"] = cvv_number
            #self.session["client_ammount"] = ammount

            self.set_cookie("client_card_number", card_number[-4:])

            info_dict = {"name": self.get_cookie("username"), "amount": ammount}

            with open("client_balance.txt","a") as data:
                for info in info_dict.values():
                    data.write(info + '\t')
                data.write('\n')

            self.set_cookie("increment", status_increment)
            self.redirect("/tenant_onboard")

        elif status == "completed":
            self.redirect("/client")
            #self.set_cookie("increment", "5")

        

class Client():

    def __init__ (self, name, surname):
        self.name = name
        self.surname = surname
        self.status = 0

    def get_balance (self):
        "Function to query database and find the balance on client's account"

        balances = pd.read_csv("client_balance.txt", sep="\t", names=["Name", "Balances"], dtype= str, index_col=False)

        client_balance = balances[balances["Name"] == self.name]

        his_balance = [float(x) for x in client_balance["Balances"]]

        his_balance = sum(his_balance)

        return his_balance
            
        

#Included ssl_options to be able to serve this website over TLS traffic, i.e https.
if __name__ == "__main__":

    try:
        print("Press Cntrl C to exit")
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        #ssl_context.load_cert_chain("/etc/ssl/certs/ca-certificates.crt")
        #ssl_context.load_default_certs(ssl.Purpose.CLIENT_AUTH)
        http_server = tornado.httpserver.HTTPServer(Application())
        #http_server = tornado.httpserver.HTTPServer(Application(), ssl_options = ssl_context)
        http_server.listen(port)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.instance().stop()

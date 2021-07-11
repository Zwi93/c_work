"""
    Created on 2021/07/08
    Author: Zwi

This script carries the ground work for connecting to a PostgreSQL using python class approach. Tables in the DB are modeled as class objects.
Session to connect to the database are managed here as well. population of data into the table can be performed by methods defined here.

"""

from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy import create_engine, distinct, engine, func, not_, select, case, cast 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, date, timedelta
import numpy as np

Base = declarative_base()

######################################################################################################################################################################################
#                                                                                                                                                                                    #
#                                                                       grace_db DB: structure                                                                                       #
#                                                                                                                                                                                    #
######################################################################################################################################################################################

class Demo(Base):
    __tablename__ = "gdp_users"

    identifier = Column(Integer, primary_key = True)
    user_name = Column(String(80))
    password = Column(String(250))



######################################################################################################################################################################################
#                                                                                                                                                                                    #
#                                                                       grace_db DB: Operations                                                                                      #
#                                                                                                                                                                                    #
######################################################################################################################################################################################

class OperateGraceDP():
    "Class to handle operations on the vatious tables in the DB."

    def __init__(self, kwargs):
        connection_url = engine.url.URL(**kwargs)
        engine_instance = create_engine(connection_url)
        Session = sessionmaker(bind = engine_instance)
        self.session = Session()

    def close_session(self):
        self.session.close()

    def test_query(self):
        "Function to test connectivity to the DB"

        results = self.session.query(Demo.identifier, Demo.user_name, Demo.password)

        content = results.all()

        print(content)


db_info = {}
db_info["drivername"] = "postgresql"
#db_info["host"] = "zwi-MS-7B79"
#db_info["port"] = "5432"
#db_info["username"] = "postgres"
#db_info["username"] = "zwi"
db_info["password"] = "postgres"
db_info["database"] = "demo"

db_object = OperateGraceDP(db_info)

db_object.test_query()
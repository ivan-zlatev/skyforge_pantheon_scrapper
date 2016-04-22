#!/usr/bin/python

###########################################################
#                                                         #
#  used to create the mysql database and pantheon table   #
#                                                         #
###########################################################

import MySQLdb
from private_data import LoginCredentials # import credentials

db = MySQLdb.connect(host=LoginCredentials['mysql_host'],
				user=LoginCredentials['mysql_username'],
				passwd=LoginCredentials['mysql_password'],
				) # connect to the MySQL Server
cursor = db.cursor()
sql = "CREATE DATABASE " + LoginCredentials['mysql_db'] # Create a new database
cursor.execute(sql)
db.select_db(LoginCredentials['mysql_db']) # USE that database
cursor = db.cursor()
table = LoginCredentials['mysql_table']
sql = "CREATE TABLE " + table + "( epoch int, member_id varchar(255), name varchar(255), prestige int, credits int, resources int, colaboration int, memberType varchar(255))"
cursor.execute(sql) # Create pantheon table
db.commit()
#  The columns are as follows:
#   
#   epoch           epoch time when the data was collected
#   member_id       uniqu member ID
#   name            curren player name
#   prestige        current prestige
#   credits         current credits
#   resources       current resources
#   colaboration    current colaboration points
#   memberType      current member type [academy|pantheon]
#   
cursor.execute("CREATE TABLE " + LoginCredentials['mysql_log'] + " ( epoch int, status tinyint )") # Create run logs table
db.commit()
cursor.execute("CREATE TABLE " + LoginCredentials['mysql_member_age'] + " (member_id varchar(255), age int)") # Create member age table
db.commit()
cursor.execute("CREATE TABLE " + LoginCredentials['mysql_register'] + " (member_id varchar(255), username varchar(255), password varchar(255))") # Create Login table
db.commit()
cursor.execute("CREATE TABLE " + LoginCredentials['mysql_lfg'] + " (epoch int, member_id varchar(255), dungeon varchar(255), tanks_required int, tanks varchar(255), supp_required int, supp varchar(255), dps_required int, dps varchar(255) )")


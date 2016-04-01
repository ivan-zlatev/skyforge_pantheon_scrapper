#!/usr/bin/python
import MySQLdb
from private_data import LoginCredentials

db = MySQLdb.connect(host=LoginCredentials['mysql_host'],    # your host, usually localhost
				user=LoginCredentials['mysql_username'],         # your username
				passwd=LoginCredentials['mysql_password'],  # your password
				)
cursor = db.cursor()
sql = "CREATE DATABASE " + LoginCredentials['mysql_db']
cursor.execute(sql)
db.select_db(LoginCredentials['mysql_db'])
cursor = db.cursor()
table = LoginCredentials['mysql_table']
sql = "CREATE TABLE " + table + "( epoch int, member_id varchar(255), name varchar(255), prestige int, credits int, resources int, colaboration int)"
cursor.execute(sql)

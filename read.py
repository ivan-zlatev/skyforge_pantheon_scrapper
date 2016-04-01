#!/usr/bin/python
import MySQLdb
from private_data import LoginCredentials

db = MySQLdb.connect(host=LoginCredentials['mysql_host'],    # your host, usually localhost
				user=LoginCredentials['mysql_username'],         # your username
				passwd=LoginCredentials['mysql_password'],  # your password
				db=LoginCredentials['mysql_db'])
cursor = db.cursor()
cursor.execute("SELECT * FROM " + LoginCredentials['mysql_table'])
data = cursor.fetchall()
for tmp in data:
	print tmp

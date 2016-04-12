#!/usr/bin/python

#####################################################################
#                                                                   #
#  used to drop the whole database in terminal for testing purposes #
#                                                                   #
#####################################################################

import MySQLdb
from private_data import LoginCredentials # import credentials

db = MySQLdb.connect(host=LoginCredentials['mysql_host'],
				user=LoginCredentials['mysql_username'],
				passwd=LoginCredentials['mysql_password'],
				db=LoginCredentials['mysql_db'])
cursor = db.cursor()
cursor.execute("SELECT * FROM " + LoginCredentials['mysql_table'])
data = cursor.fetchall()
for tmp in data:
	print tmp
print ""
cursor.execute("SELECT * FROM " + LoginCredentials['mysql_log'])
data = cursor.fetchall()
for tmp in data:
	print tmp
print ""
cursor.execute("SELECT * FROM " + LoginCredentials['mysql_member_age'])
data = cursor.fetchall()
for tmp in data:
	print tmp
print ""
cursor.execute("SELECT * FROM " + LoginCredentials['mysql_register'])
data = cursor.fetchall()
for tmp in data:
	print tmp

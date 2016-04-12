#!/usr/bin/python

#####################################################################
#                                                                   #
#  used to fix the age of members so that delta is 1 after          #
#                                                                   #
#####################################################################

import time
import MySQLdb
from private_data import LoginCredentials # import credentials

def FixMembersAgeSoThatDeltaIsOne(table, requirement):
	db = MySQLdb.connect(host=LoginCredentials['mysql_host'],
					user=LoginCredentials['mysql_username'],
					passwd=LoginCredentials['mysql_password'],
					db=LoginCredentials['mysql_db'])
	cursor = db.cursor()
	sql = "SELECT * FROM pantheon_age ORDER BY member_id ASC"
	cursor.execute(sql)
	age_arr = cursor.fetchall()
	sql = "SELECT * FROM pantheon_log WHERE status = 1 ORDER BY epoch DESC LIMIT 1"
	cursor.execute(sql)
	epoch = cursor.fetchone()
	sql = "SELECT * FROM pantheon WHERE epoch = '" + str(epoch[0]) + "' ORDER BY member_id ASC"
	cursor.execute(sql)
	data_arr = cursor.fetchall()
	curr_time = int(time.time())
	for age in age_arr:
		for data in data_arr:
			if age[0] in data:
				new_age = curr_time - ((data[table]/requirement)*604800  )
				sql = "UPDATE pantheon_age SET age = '" + str(new_age) + "' WHERE member_id = '" + str(data[1]) + "'"
				cursor.execute(sql)
				db.commit()				
if __name__ == "__main__":
	FixMembersAgeSoThatDeltaIsOne( table = 4, requirement = 20000 )

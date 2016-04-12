#!/usr/bin/python

#####################################################################
#                                                                   #
#  used to scrap the data from aelinet and put it in a mysql db     #
#                                                                   #
#####################################################################

from lxml import html # used for parsing html code
import time
from selenium import webdriver
import MySQLdb
from private_data import LoginCredentials # import credentials
from pyvirtualdisplay import Display

def LogInToMyPortal(username, password, pantheonID):
	display = Display(visible=0, size=(1920, 1080))
	display.start()
	global status
	status = False
	db = MySQLdb.connect(host=LoginCredentials['mysql_host'],
						user=LoginCredentials['mysql_username'],
						passwd=LoginCredentials['mysql_password'],
						db=LoginCredentials['mysql_db'])
	cursor = db.cursor()
	log = LoginCredentials['mysql_log']
	browser = webdriver.Firefox() # open a webdriver
	browser.set_window_size(1920, 1080) # set windows size so that buttons are visible
	browser.get("https://account.my.com/login/") # login to aelinet
	u = browser.find_element_by_name("email")
	p = browser.find_element_by_name("password")
	u.send_keys(username)
	p.send_keys(password)
	p.submit()
#get first members page
	browser.get("https://eu.portal.sf.my.com/guild/members/" + pantheonID)
	time.sleep(3)
	epoch = int(time.time())
	sql = "INSERT INTO " + log + " ( epoch, status ) VALUES ( %d, 0 )" % ( epoch )
	cursor.execute(sql)
	db.commit()
	global memberType
	memberType = "pantheon"
	getPantheonData(browser.page_source, epoch)
#get next members page loop
	while True:
		try:
			browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			browser.find_element_by_class_name("svg-arrow-right").click()
			time.sleep(3)
			getPantheonData(browser.page_source, epoch)
		except:
			break
#get first academy page
	browser.get("https://eu.portal.sf.my.com/guild/academy/" + pantheonID)
	time.sleep(3)
	memberType = "academy"
	getPantheonData(browser.page_source, epoch)
#get next academy page loop
	while True:
		try:
			browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			browser.find_element_by_class_name("svg-arrow-right").click()
			time.sleep(3)
			getPantheonData(browser.page_source, epoch)
		except:
			browser.close()
			break
	if status == True:
		sql = "UPDATE " + log + " SET status=1 WHERE epoch=%d" % (epoch)
		cursor.execute(sql)
		db.commit()
	display.stop()

def getPantheonData(page, epoch):
	tree = html.fromstring(page)
	body = tree.getchildren()[1]
	for tmp in body.getchildren():
		if 'cont__wrap' in tmp.values():
			for tmp2 in tmp.getchildren():
				if 'cont bodyWrapper' in tmp2.values():
					for tmp3 in tmp2.getchildren():
						if 'portalPageBody' in tmp3.values():
							for tmp4 in tmp3.getchildren():
								if 'guild-acad' in tmp4.values():
									for tmp5 in tmp4.getchildren():
										if 't-zone tapestry-zone' in tmp5.values():
											for tmp6 in tmp5.getchildren():
												if 'guild-member' in tmp6.values():
													member = tmp6
													global status
													try:
														getMemberData(member, epoch)
														status = True
													except:
														status = False

def getMemberData(member, epoch):
	db = MySQLdb.connect(host=LoginCredentials['mysql_host'],
					user=LoginCredentials['mysql_username'],
					passwd=LoginCredentials['mysql_password'],
					db=LoginCredentials['mysql_db'])
	cursor = db.cursor()
	table = LoginCredentials['mysql_table']
	age_table = LoginCredentials['mysql_member_age']
	for tmp in member.getchildren():
		if 'corn' in tmp.values():
			i = 1
			for tmp2 in tmp.getchildren()[0]:
				if 'guild-member-td-b' in tmp2.values():
					name = tmp2.getchildren()[0].getchildren()[1].getchildren()[0].getchildren()[0].text.strip()
					profile = tmp2.getchildren()[0].getchildren()[1].getchildren()[0].getchildren()[0].values()[0].split("wall/")[1]
					print name
				if 'guild-member-td-c' in tmp2.values():
					if i == 1:
						prestige = tmp2.getchildren()[0].text.strip()
						prestige = convertPantheonData(prestige)
						i+= 1
					elif i == 2:
						credits = tmp2.getchildren()[0].text.strip()
						credits = convertPantheonData(credits)
						i+= 1
					elif i == 3:
						construction = tmp2.getchildren()[0].text.strip()
						construction = convertPantheonData(construction)
						i+= 1
					elif i == 4:
						colaboration = tmp2.getchildren()[0].text.strip()
						colaboration = convertPantheonData(colaboration)
						i+= 1
			sql = "INSERT INTO " + table + " (epoch, member_id, name, prestige, credits, resources, colaboration, memberType) VALUES ( %d, '%s', '%s', %d, %d, %d, %d, '%s' )" % ( epoch, profile, name, prestige, credits, construction, colaboration, memberType )
			print sql
			cursor.execute(sql)
			db.commit()
			sql = "SELECT COUNT(*) FROM " + age_table + " WHERE member_id = '%s'" %( profile )
			cursor.execute(sql)
			memberCount = cursor.fetchone()
			if memberCount[0] < 1:
				sql = "INSERT INTO " + age_table + " ( member_id, age ) VALUES ( '%s', %d )" % ( profile, epoch )
				cursor.execute(sql)
				db.commit()

def convertPantheonData(value): # convert K and M from aelinet to zeros so that values are integer/long
	if value[-1:] == "K":
		value = value.split("K")[0]
		value = value.replace(".", "")
		value = value + "00"
	elif value[-1:] == "M":
		value = value.split("M")[0]
		value = value.replace(".", "")
		value = value + "00"
	return int(value)
if __name__ == "__main__":
	LogInToMyPortal(username = LoginCredentials['username'], password = LoginCredentials['password'], pantheonID = LoginCredentials['pantheonID'])

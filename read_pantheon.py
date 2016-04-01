#!/usr/bin/python
from lxml import html
import requests
import sys
import argparse
import time
from selenium import webdriver
import MySQLdb
from private_data import LoginCredentials

def LogInToMyPortal(username, password, pantheonID):
	browser = webdriver.Firefox()
	#browser.maximize_window()
	browser.set_window_size(1920, 1080)
	browser.get("https://account.my.com/login/")
	u = browser.find_element_by_name("email")
	p = browser.find_element_by_name("password")
	u.send_keys(username)
	p.send_keys(password)
	p.submit()
#get first members page
	browser.get("https://eu.portal.sf.my.com/guild/members/" + pantheonID)
	time.sleep(1)
	epoch = int(time.time())
	global memberType
	memberType = "pantheon"
	GetPantheonData(browser.page_source, epoch)
#get next members page loop
	while True:
		try:
			browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			browser.find_element_by_class_name("svg-arrow-right").click()
			time.sleep(1)
			GetPantheonData(browser.page_source, epoch)
		except:
			break
#get first academy page
	browser.get("https://eu.portal.sf.my.com/guild/academy/" + pantheonID)
	time.sleep(1)
	memberType = "academy"
	GetPantheonData(browser.page_source, epoch)
#get next academy page loop
	while True:
		try:
			browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			browser.find_element_by_class_name("svg-arrow-right").click()
			time.sleep(1)
			GetPantheonData(browser.page_source, epoch)
		except:
			browser.close()
			break

def GetPantheonData(page, epoch):
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
													getMemberData(member, epoch)

def getMemberData(member, epoch):
	db = MySQLdb.connect(host=LoginCredentials['mysql_host'],    # your host, usually localhost
					user=LoginCredentials['mysql_username'],         # your username
					passwd=LoginCredentials['mysql_password'],  # your password
					db=LoginCredentials['mysql_db'])        # name of the data base
	cursor = db.cursor()
	table = LoginCredentials['mysql_table']
	for tmp in member.getchildren():
		if 'corn' in tmp.values():
			profile = tmp.getchildren()[1].values()
			for tmp2 in profile:
				if "zoneHelper" in tmp2.split("."):
					profile = tmp2.split(":selectmember/")[1].split("?")[0]
			i = 1
			#print profile
			for tmp2 in tmp.getchildren()[0]:
				if 'guild-member-td-b' in tmp2.values():
					name = tmp2.getchildren()[0].getchildren()[1].getchildren()[0].getchildren()[0].text.strip()
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
			cursor.execute(sql)

def convertPantheonData(value):
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

# coding=utf-8
from splinter import Browser
from time import sleep
import datetime


date = '2018/4/6' 		#xxxx/xx/xx
place_floor = '1'			#n floor  1/3
place_num = '2'		
place_time_begin = '19'		#24
place_time_end = '21'		#24
usr_name = 'r05944001'
usr_pw = ''


#####################################
browser = []
Date = date.split('/')
weekday = int(datetime.datetime(int(Date[0]),int(Date[1]),int(Date[2])).strftime("%w"))
stime = int(place_time_begin) - 8
url = ''
#####################################


def browser_start():
	global date,browser,usr_name,usr_pw,place_floor,url

	login_url = 'https://info2.ntu.edu.tw/facilities/Default.aspx' 
	if place_floor == '1':
		url = 'https://info2.ntu.edu.tw/facilities/PlaceGrd.aspx?nFlag=0&placeSeq=2&dateLst='
	if place_floor == '3':
		url = 'https://info2.ntu.edu.tw/facilities/PlaceGrd.aspx?nFlag=0&placeSeq=1&dateLst='

	url = url + date
	browser = Browser('chrome')
	browser.visit(login_url)
	browser.find_by_text(u"學生登入").click()
	browser.find_by_name('user').fill(usr_name)
	browser.find_by_name('pass').fill(usr_pw)
	browser.find_by_name('Submit').click()
	browser.visit(url)


def do_assignments():
	global browser,stime,weekday,place_num,place_time_begin,place_time_end

	k = browser.find_by_tag('table');
	u = k[7].find_by_tag('td') #time table
	regist = u[8 * (stime+1) + weekday + 1 - 1].find_by_tag('img')
	if len(regist) < 3:
		return 0
	regist[2].click()

	place_num_name = 'ctl00$ContentPlaceHolder1$txtPlaceNum'
	browser.fill(place_num_name, place_num)

	####time select
	select_name_begin = 'ctl00$ContentPlaceHolder1$DropLstTimeStart'
	select_name_end = 'ctl00$ContentPlaceHolder1$DropLstTimeEnd'
	browser.select(select_name_begin, place_time_begin)
	browser.select(select_name_end, place_time_end)

	button_name_send = u"送出預約"
			#button_name_cancel = u"取消"
			#button_name_cancel = 'ctl00$ContentPlaceHolder1$btnCancel'
	
	browser.find_by_value(button_name_send).click()
	print('end')
	print(datetime.datetime.now())

def time_detection():
	global browser,weekday,url

	tiem_delay = 1000
	if weekday <=5:
		sys_start_hour = 8
	if weekday >5:
		sys_start_hour = 9
		if weekday == 7:
			weekday = 1		#when meets 7,the table formulation will be different and Sunday will take the place of Monday's position
			print('attention,Sunday,different table')
	while 1:
		now = datetime.datetime.now()
		print(now)

		if int(now.hour) == sys_start_hour - 1:
			tiem_delay = 30
		if int(now.hour) == sys_start_hour - 1 and int(now.minute) >= 59:
			browser_start()
			print('ready')
			while 1:
				now =datetime.datetime.now()
				if int(now.hour) == sys_start_hour:
					browser.reload()
					try:
						flag = do_assignments()
						if flag == 0:
							continue
						break
					except:
						browser.visit(url)
						continue

			break

		sleep(tiem_delay)

time_detection()
#raw_input()	#exe

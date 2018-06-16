#!/usr/bin/python
# -*- coding: UTF-8 -*-
import tkinter as tk
from tkinter import messagebox
from tkinter import *
from datetime import datetime,timedelta
import time
import string
from splinter import Browser
import traceback

def btnCallBack():
	#####################################
	#browser test
	global usr_name
	if usr_name.get() == 'R0':
		print('Browser Test Mode')
		if test() == 1:
			messagebox.showinfo( "測試結果：", "缺少chromedriver.exe（或版本錯誤）")
		else:
			messagebox.showinfo( "測試結果：", "可正常運行")
	else:
		run_thread()

def test():
	try:
		browser = Browser('chrome',executable_path='./chromedriver.exe')
		browser.visit('https://info2.ntu.edu.tw/facilities/Default.aspx')
		browser.quit()
		return 0
	except:
		print('traceback.print_exc(): '+ traceback.print_exc())
		return 1

def run_thread():

	global date,usr_name,usr_pw,place_floor,place_time_begin,place_time_end,place_num,weekday
	#####################################
	browser = []
	date = date.get()
	usr_name = usr_name.get()
	usr_pw = usr_pw.get()
	place_floor = place_floor.get()
	place_time_begin = place_time_begin.get()
	place_time_end = place_time_end.get()
	place_num = place_num.get()

	Date = date.split('/')
	weekday = int(datetime(int(Date[0]),int(Date[1]),int(Date[2])).strftime("%w"))
	stime = int(place_time_begin) - 8
	url = ''

	def browser_start():
		global date,browser,usr_name,usr_pw,place_floor,url

		login_url = 'https://info2.ntu.edu.tw/facilities/Default.aspx' 
		if place_floor == '1':
			url = 'https://info2.ntu.edu.tw/facilities/PlaceGrd.aspx?nFlag=0&placeSeq=2&dateLst='
		if place_floor == '3':
			url = 'https://info2.ntu.edu.tw/facilities/PlaceGrd.aspx?nFlag=0&placeSeq=1&dateLst='

		url = url + date
		browser = Browser('chrome',executable_path='./chromedriver.exe')
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
		
		browser.find_by_value(button_name_send).click()
		print('end')
		print(datetime.now())
		messagebox.showinfo( "訂場", "搶到啦！")

	def time_detection():
		global browser,weekday,url

		tiem_delay = 1000
		if weekday <=5:
			sys_start_hour = 8
		if weekday >5:
			sys_start_hour = 9
			if weekday == 7:
				weekday = 1		#when meets 7,the table formulation will be different and Sunday will take the place of Monday's position
				#print('attention,Sunday,different table')
		while 1:
			now = datetime.now()
			print(now)

			if int(now.hour) == sys_start_hour - 1:
				tiem_delay = 30
			if int(now.hour) == sys_start_hour - 1 and int(now.minute) >= 59:
				browser_start()
				print('ready')
				messagebox.showinfo( "訂場", "ready！")
				while 1:
					now = datetime.now()
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

			time.sleep(tiem_delay)

	time_detection()

#get next_week
start = datetime.now()
i = 8
next_week = (start + timedelta(i)).strftime("%Y/%m/%d")

#UI
root = tk.Tk()

root.title('NTU 羽球社訂場專用            V1.1 by_Fook')
#root.iconbitmap('ui.ico')# ICON 
root.geometry("450x400")
root.maxsize(450,400)
root.configure(background='#33FFFF')

#建立標籤
label0 = tk.Label(root, text="帳號/密碼：", pady=6,bg="#33FFFF", fg="#000000", font=("新細明體", 12))
label1 = tk.Label(root, text="樓層：     ", pady=6,bg="#33FFFF", fg="#000000", font=("新細明體", 12))
label2 = tk.Label(root, text="要訂場時間:", pady=6,bg="#33FFFF", fg="#000000", font=("新細明體", 12))
label3 = tk.Label(root, text="數量:      ", pady=6,bg="#33FFFF", fg="#000000", font=("新細明體", 12))
#
global date,usr_name,usr_pw,place_floor,place_time_begin,place_time_end,place_num
#
usr_name = StringVar()
entry0 = Entry(root,textvariable = usr_name)
usr_name.set('R0')
entry0.pack()

usr_pw = StringVar()
entry1 = Entry(root,textvariable = usr_pw)
entry1.pack()
entry1['show'] = '*'

place_floor = StringVar()
entry2 = Entry(root,textvariable = place_floor)
entry2.pack()
place_floor.set('1')

date = StringVar()
entry3 = Entry(root,textvariable = date)
entry3.pack()
date.set(next_week)

place_time_begin = StringVar()
entry4 = Entry(root,textvariable = place_time_begin)
entry4.pack()
place_time_begin.set('19')

place_time_end = StringVar()
entry5 = Entry(root,textvariable = place_time_end)
entry5.pack()
place_time_end.set('21')

place_num = StringVar()
entry6 = Entry(root,textvariable = place_num)
entry6.pack()
place_num.set('2')
#button
b1 = tk.Button(root, text = '開始\n搶場',  width = 10, command = btnCallBack)
b1.pack(side=BOTTOM)

label0.place(x=10, y=40, width=150, height=40)
entry0.place(x=50, y=90, width=150, height=20)
entry1.place(x=50, y=120, width=150, height=20)
label1.place(x=10, y=160, width=150, height=40)
entry2.place(x=50, y=210, width=75, height=20)
label2.place(x=10, y=240, width=150, height=40)
entry3.place(x=50, y=290, width=150, height=20)
entry4.place(x=50, y=320, width=150, height=20)
entry5.place(x=50, y=350, width=150, height=20)
label3.place(x=170, y=160, width=150, height=40)
entry6.place(x=210, y=210, width=75, height=20)
b1.place(x=300,y=290, width=100, height=80)

root.mainloop()

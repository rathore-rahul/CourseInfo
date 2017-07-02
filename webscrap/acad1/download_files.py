import csv
import time
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup as BS
from selenium.webdriver.common.keys import Keys
import re
import unicodedata
import gender

def clean_html(raw_html):
	cleanr = re.compile('<.*?>')
	cleanText = re.sub(cleanr,'',raw_html)
	return cleanText

def courses_list(userid,password):
	driver = webdriver.Firefox()
	driver.get('https://academics1.iitd.ac.in')
	username = driver.find_element_by_name('username')
	username.send_keys(userid)
	password = driver.find_element_by_name('password')
	password.send_keys(password)
	login = driver.find_element_by_name('submit-button')
	login.click()
	link = driver.find_element_by_link_text('List of Offered Courses - Next Semester')
	link.click()
	html = driver.page_source
	soup = BS(html,"html.parser")
	tables = soup.find_all('table')
	coursesTable = tables[-1]
	rows = [tr.findAll('td') for tr in coursesTable.findAll('tr')]
	outputfile = open('CourseList.csv','w')
	for row in rows:
		row = unicode.join(u'\n',map(unicode,row))
		row = clean_html(row)
		row = unicodedata.normalize('NFKD',row).encode('ascii','ignore')
		row = row.replace('amp;','')
		row = row.replace(',',' ')
		row = row.replace('\n',',')
		outputfile.write(row+'\n')
	outputfile.close()

def registered_student_by_course(userid,password):
	df = pd.read_csv('CourseList.csv')
	driver = webdriver.Firefox()
	driver.get('https://academics1.iitd.ac.in')
	userElem = driver.find_element_by_name('username')
	userElem.send_keys(userid)
	passElem = driver.find_element_by_name('password')
	passElem.send_keys(password)
	login = driver.find_element_by_name('submit-button')
	login.click()
	link = driver.find_element_by_link_text('List of Registered Students in a Course Ist Semester 20172018')
	link.click()
	baseUrl = driver.current_url
	CourseCodeList = df['Course Code'].unique()
	for code in CourseCodeList:
		driver.get(baseUrl)
		input = driver.find_element_by_name('EntryNumber')
		input.send_keys(code)
		input.send_keys(Keys.RETURN)
		fileName = code+'.csv'
		time.sleep(2.5)
		html = driver.page_source
		soup = BS(html,"html.parser")
		tables = soup.find_all('table')
		studentList = tables[-1]
		rows = [tr.findAll('td') for tr in studentList.findAll('tr')]
		outputfile = open(fileName,'w')
		for row in rows:
			row = unicode.join(u'\n',map(unicode,row))
			row = clean_html(row)
			row = unicodedata.normalize('NFKD',row).encode('ascii','ignore')
			row = row.replace('amp;','')
			row = row.replace(',',' ')
			row = row.replace('\n',',')
			outputfile.write(row+'\n')
		outputfile.close()

def firstName2gender():
	df = pd.read_csv('CourseList.csv')
	codeList = df['Course Code'].unique()
	studentList = set()
	for code in codeList:
		fileName = code + '.csv'
		cf = pd.read_csv(fileName)
		for name in cf['Student Name ']:
			studentList.add(name.split()[0])
	counter = 0
	inputList = []
	outList = []
	output_file_name = 'firstname2gender.csv'
	outputfile = open(output_file_name,'w')
	outputfile.write('Name,Gender\n')
	for name in studentList:
		counter = counter + 1	#since 1000 call to api is allowed in one day
		inputList.append(name)	#use logic for only 1000 calls using if statements
		if counter%10 == 0:
			tempList = gender.getGenders(inputList)
			outList.append(tempList)
			for i in range(0,10):
				outputfile.write(inputList[i] + ',' + tempList[i][0]+'\n')
			inputList = []
	outputfile.close()

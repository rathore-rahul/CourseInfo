import csv
import time
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup as BS
from selenium.webdriver.common.keys import Keys
import re
import unicodedata

def clean_html(raw_html):
	cleanr = re.compile('<.*?>')
	cleanText = re.sub(cleanr,'',raw_html)
	return cleanText

def get_registered_student(username,password):
	df = pd.read_csv('CourseList.csv')
	driver = webdriver.Firefox()
	driver.get('https://academics1.iitd.ac.in')
	username = driver.find_element_by_name('username')
	username.send_keys(username)
	password = driver.find_element_by_name('password')
	password.send_keys(password)
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
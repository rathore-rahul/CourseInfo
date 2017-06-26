from selenium import webdriver
from bs4 import BeautifulSoup as BS
import re
import unicodedata

def clean_html(raw_html):
	cleanr = re.compile('<.*?>')
	cleanText = re.sub(cleanr,'',raw_html)
	return cleanText

def start_scrapping(userid,password):
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

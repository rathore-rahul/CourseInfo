import pandas as pd
import sys

def find_courses_by_student_name(name):
	name = name.upper()
	courses = []
	df = pd.read_csv('CourseList.csv')
	codeList = df['Course Code'].unique()
	for code in codeList:
		fileName = code+'.csv'
		cf = pd.read_csv(fileName)
		if (cf['Student Name '] == name).any() == True:
			courses.append(code)
	return courses
	
def find_courses_by_student_id(student_id):
	student_id = student_id.upper()
	courses = []
	df = pd.read_csv('CourseList.csv')
	codeList = df['Course Code'].unique()
	for code in codeList:
		fileName = code+'.csv'
		cf = pd.read_csv(fileName)
		if (cf['Entry Number'] == student_id).any() == True:
			courses.append(code)
	return courses

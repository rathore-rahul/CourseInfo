import csv
import time
import pandas as pd
import sys

def generate_courses_sexratio():
    output_file_name = 'courseSexRatio.csv'
    outputfile = open(output_file_name,'w')
    outputfile.write('CourseCode,femalesRatio\n')
    courses = []
    df = pd.read_csv('CourseList.csv')
    codeList = df['Course Code'].unique()
    gendermap = pd.read_csv('studentname2gender.csv')
    for code in codeList:
        fileName = code + '.csv'
        cf = pd.read_csv(fileName)
        num_male = 0
        num_female = 0
        num_none = 0
        for name in cf['Student Name ']:
            gender = gendermap.loc[gendermap['Name'] == name,'Gender'].iloc[0]
            if gender == 'male':
                num_male = num_male + 1
            elif gender == 'female':
                num_female = num_female + 1
            else:
                num_none = num_none + 1
        total = len(cf)
        if total != 0:
            femalesRatio = (num_female*1.0)/total
        else:
            femalesRatio = 0
        outputfile.write(str(code)+','+str(femalesRatio) + '\n')
    outputfile.close()

def studentname2gender():
    outputfile = open('studentname2gender.csv','w')
    outputfile.write('Name,Gender\n')
    df = pd.read_csv('CourseList.csv')
    codeList = df['Course Code'].unique()
    gendermap = pd.read_csv('firstname2gender.csv')
    studentList = set()
    for code in codeList:
        fileName = code + '.csv'
        cf = pd.read_csv(fileName)
        for name in cf['Student Name ']:
            studentList.add(name)
    for name in studentList:
        firstname = name.split()[0]
        gender = gendermap.loc[gendermap['Name'] == firstname,'Gender'].iloc[0]
        outputfile.write(name+','+gender+'\n')
    outputfile.close()

import csv
import json
import re

dataRows = [];
headerRow = [];
with open('../data/8_Parents_Meet.csv', newline='',encoding='utf-8') as csvfile:
	reader = csv.reader(csvfile, delimiter=',',quotechar='"',skipinitialspace=True)
	isHeader = True;
	for row in reader:
		if(not isHeader):
			age = 'young'
			if(row[2] == '26 or older.'):
				age = 'old'
			dataRows.append({'parents_meet':row[1],'age':age,'current_meet':row[3]})
		else:
			headerRow = row;
		isHeader = False;

print(dataRows[0])

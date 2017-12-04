import csv
import re
import json

dataRows = [];
headerRow = [];
with open('../data/5_Friends_Like_You_Clean.csv', newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',',quotechar='"',skipinitialspace=True)
	isHeader = True;
	for row in reader:
		if(not isHeader):
			dataRows.append({'friends':row[1],'major':row[2],'history':row[3]})
		else:
			headerRow = row;
		isHeader = False;

# Number of history majors by major
numOfHistory = {};
historyBuckets = {};
for datum in dataRows:
	# Try to convert history to a number 
	numbers =  re.findall(r'\d+', datum['history']);
	historyNum = 0;
	if(len(numbers) > 0):
		count = int(numbers[0]);
		historyNum = count;

	else:
		historyNumString = datum['history'].lower();
		if(historyNumString.find("none") >= 0 or historyNumString.find("know") >= 0):
			historyNum = 0;
		if(historyNumString.find("one") >= 0):
			historyNum = 1;
		if(historyNumString.find("two") >= 0):
			historyNum = 2;
		if(historyNumString.find("three") >= 0):
			historyNum = 3;

	lowerCaseMajor = datum['major'].lower().strip();
	if(not (lowerCaseMajor in numOfHistory)):
		numOfHistory[lowerCaseMajor] = {'history_majors':0,'count':0};

	numOfHistory[lowerCaseMajor]['history_majors'] += historyNum;
	numOfHistory[lowerCaseMajor]['count'] += 1;

	if(not (historyNum in historyBuckets) ):
		historyBuckets[historyNum] = 0;
	historyBuckets[historyNum] += 1

# Write these history buckets to file 
newHeader = ['num_of_people','history_majors_known']
with open('../data/5_History_Majors.csv', 'w', newline='') as csvfile:
	writer = csv.writer(csvfile, delimiter=',')
	# Write header
	writer.writerow(newHeader);
	# Write all the cleaned data
	for history_num in historyBuckets:
		writer.writerow([historyBuckets[history_num], history_num ])

totalHistory = 0;
for major in numOfHistory:
	numObj = numOfHistory[major];
	totalHistory += numObj['history_majors'];
	#print(major, numObj['history_majors'] / numObj['count'])

#print(totalHistory / len(dataRows))

# Construct nodes and edges of graph  
nodes = [];
edges = [];
uniqueMajor = {};
for datum in dataRows:
	major = datum['major'].lower().strip();
	connections = datum['friends'].lower().split(",");
	if(not (major in uniqueMajor)):
		uniqueMajor[major] = len(nodes);
		nodes.append({'name':major});

	for con in connections:
		major2 = con.strip();
		if(not (major2 in uniqueMajor)):
			uniqueMajor[major2] = len(nodes);
			nodes.append({'name':major2});

connMap = {};

for datum in dataRows:
	connections = datum['friends'].lower().split(",");
	major = datum['major'].lower().strip();
	sourceIndex = uniqueMajor[major];
	for con in connections:
		major2 = con.strip();
		targetIndex = uniqueMajor[major2];
		if(((sourceIndex in connMap) and connMap[sourceIndex] == targetIndex) or ((targetIndex in connMap) and connMap[targetIndex] == sourceIndex)):
			for i in range(len(edges)):
				if(edges[i]['source'] == sourceIndex and edges[i]['target'] == targetIndex):
					edges[i]['value'] += 1
		else:
			edges.append({'source':sourceIndex,'target':targetIndex,'value':1})
			connMap[sourceIndex] = targetIndex;

#edges = edges[len(edges)-10:]
finalObject = {'nodes':nodes,'edges':edges}

with open('../data/5_Edges_And_Nodes.json', 'w') as outfile:
    json.dump(finalObject, outfile,indent = 2)

# Count how many do not consider their own major as friend 
ownMajorFriend = 0;
for datum in dataRows:
	connections = datum['friends'].lower().split(",");
	major = datum['major'].lower().strip();
	for con in connections:
		major2 = con.strip();
		if(major == major2):
			ownMajorFriend += 1;
			break;


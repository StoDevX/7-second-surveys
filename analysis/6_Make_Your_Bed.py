import csv
import json
import re

dataRows = [];
headerRow = [];
with open('../data/6_Make_Your_Bed.csv', newline='',encoding='utf-8') as csvfile:
	reader = csv.reader(csvfile, delimiter=',',quotechar='"',skipinitialspace=True)
	isHeader = True;
	for row in reader:
		if(not isHeader):
			dataRows.append({'make_bed':row[1],'why':row[2],'other_make_bed':row[3]})
		else:
			headerRow = row;
		isHeader = False;

MakeBedCount = 0
TotalCount = 0

for row in dataRows:
	if(row['make_bed'] == 'Always! Or almost always.'):
		MakeBedCount += 1
	TotalCount += 1

MakeBedPercent = MakeBedCount / TotalCount

print("MakeBed:",MakeBedCount,"\tTotal:",TotalCount) # 76 168
print("MakeBedPercent:",MakeBedPercent) # 0.452 

# Let's look for common reasons why people make or don't make their beds 
mom_count = 0;
lazy_count = 0;
for row in dataRows:
	reason = row['why'].lower()
	if('mom' in reason or 'parent' in reason or 'mother' in reason):
		mom_count += 1

print("Mom count:",mom_count)

# Aggregate and clean up data to visualize in Javascript
cleanData = []
# catagories
labels = ['moral obligation','ephemeral pleasure','aesthetics','hurry or lazy','lofted']
manually_assigned = [0,1,2,0,3,1,3,3,-1,1,3,1,4,2,2,0,4,0,1,0,1,3,-1,1,1,3,2,2,1,0,2,0,3,0,0,3,3,2,-1,-1,2,1,
0,0,-1,1,0,-1,2,-1,4,1,4,2,0,0,1,3,4,3,1,4,1,0,-1,3,1,1,0,0,4,-1,0,3,2,0,1,1,0,4,2,4,1,3,3,3,2,1,-1
]
label_count = 0

# Also one more thing I want to know: How your prediction is affected by your own view
# Optimist means they think others make their bed
predictions = {'optimist_bed_maker':0,'pessimist_bed_maker':0,'optimist_messy':0,'pessimist_messy':0}

for row in dataRows:
	make_bed = False;
	reason = row['why'].lower()
	# Remove semi colon 
	reason = re.sub(';','',reason)
	other_make_bed = False;
	aggregate_reason = ''

	if(row['make_bed'] == 'Always! Or almost always.'):
		make_bed = True;
	if(row['other_make_bed'] == 'Most people make their bed every day or almost every day.'):
		other_make_bed = True;

	if(make_bed and other_make_bed):
		# They make their bed and think others too!
		predictions['optimist_bed_maker'] += 1
	if(make_bed and not other_make_bed):
		# They make their bed, but they think others don't
		predictions['pessimist_bed_maker'] += 1
	if(not make_bed and other_make_bed):
		# They don't make their bed, but they think others do 
		predictions['optimist_messy'] += 1
	if(not make_bed and not other_make_bed):
		# They don't make their bed, and they think others don't
		predictions['pessimist_messy'] += 1
	
	if(reason != '' and label_count < len(manually_assigned)):
		label_index = manually_assigned[label_count]
		if(label_index == -1):
			aggregate_reason = 'Uncategorized'
		else:
			aggregate_reason = labels[label_index]
		label_count += 1

	newRow = [make_bed,reason,other_make_bed,aggregate_reason]
	cleanData.append(newRow)

print("Predictions",predictions)
# Predictions {'optimist_messy': 13, 'pessimist_bed_maker': 60, 'pessimist_messy': 79, 'optimist_bed_maker': 16}


# Write clean data 
newHeader = ['make_bed','reason','other_make_bed','aggregate_reason']
with open('../data/6_Make_Your_Bed_Clean.csv', 'w', newline='',encoding='utf-8') as csvfile:
	writer = csv.writer(csvfile, delimiter=',')
	# Write header
	writer.writerow(newHeader);
	# Write all the cleaned data
	for row in cleanData:
		writer.writerow(row)
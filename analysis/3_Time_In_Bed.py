import csv
import re

dataRows = [];
headerRow = [];
with open('../data/3_Time_In_Bed.csv', newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	isHeader = True;
	for row in reader:
		if(not isHeader):
			dataRows.append({'timestamp':row[0],'time_in_bed':row[1],'action':row[2]})
		else:
			headerRow = row;
		isHeader = False;

# Let's do some initial inspection. How many people filled out what they do in bed?
admittedAction = 0;
for datum in dataRows:
	if(datum['action'] != ''):
		admittedAction += 1;

#print(str(admittedAction) + " people out of " + str(len(dataRows)) + " submitted what they do in bed.") 
#83 out of 111, not bad!

# We want to convert all the time answers into a consistent format so we can get the average and such
captured = 0;
for datum in dataRows:
	time = datum['time_in_bed'].lower();
	final_minutes = 0;
	#If it can be parsed as an int, great!
	try:
		timeInMinutes = int(time);
		final_minutes = timeInMinutes;
		datum['time_in_minutes'] = final_minutes;
	except ValueError:
		lookFor = ["min","hour","hr","second"];
		unit_map = {
		'min':'min',
		'hour':'hr',
		'hr':'hr',
		'second':'second'
		}
		found = False;
		for item in lookFor:
			if(time.find(item) >= 0):
				captured += 1;
				found = True;
				# Rules for parsing this time are:
				# 	1- If only one of those keywords is found, extract the first number you see and set that as the time 
				foundCount = 0;
				units_found = []
				for lookItem in lookFor:
					if(time.find(lookItem) >= 0):
						foundCount += 1;
						units_found.append(lookItem)
				numbers =  re.findall(r'\d+\.?\d*', time);
				time_val = 0;
				if(len(numbers) == 0):
					# 2- If no number is found, treat it as 1 of this unit 
					time_val = 1;
				else:
					time_val = int(float(numbers[0]));
				# Finally convert that to minutes 
				# 3- If we found multiple units, just pick the first one found 
				unit = units_found[0];
				if(unit_map[unit] == "min"):
					final_minutes = time_val;
				elif(unit_map[unit] == "hr"):
					final_minutes = time_val * 60;
				elif(unit_map[unit] == "second"):
					final_minutes = time_val  / 60;
				#print(final_minutes,"\t\t",time)
				datum['time_in_minutes'] = final_minutes;
				
				break;
		if(not found):
			# Just ignore these, they're not valid answers
			pass
	

# Now copy all the clean data into a new dict
cleanData = []

for datum in dataRows:
	if('time_in_minutes' in datum):
		cleanData.append({'time_in_bed':datum['time_in_minutes'],'action':datum['action']})

# How many are usable?
#print(len(cleanData)) # 108, that's almost all of them! 

# Let's analyze the actions now!
# Can we find out how many people do something with their phone/email/social media?
social_media = 0;
non_social_media = 0;
for datum in dataRows:
	lookFor = ["phone","email","facebook","instagram","social media","youtube","reddit","twitter"]
	action = datum['action'].lower();
	
	found = False;
	
	for item in lookFor:
		if(action.find(item) >= 0):
			social_media += 1;
			found = True;
			break;
	if(not found and action != ""):
		non_social_media += 1

print(social_media,non_social_media) # 53, 30

# Output these to a new clean csv 
newHeader = ['minutes_in_bed','action']
with open('../data/3_Time_In_Bed_Clean.csv', 'w', newline='') as csvfile:
	writer = csv.writer(csvfile, delimiter=',')
	# Write header
	writer.writerow(newHeader);
	# Write all the cleaned data
	for datum in cleanData:
		writer.writerow([datum['time_in_bed'],datum['action'] ])
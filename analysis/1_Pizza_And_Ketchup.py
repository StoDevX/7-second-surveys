import csv
import us # US state names lookup
from dateutil import parser


'''
Interesting notes about data:
-----------------------------
* Someone wrote their state is "Texas/Minnesota". How do you classify them?
* Also "bolivia/italy" 
* 
'''

def CleanUSA(s):
	# Given something like "MN, USA"
	# it will return just MN. If the input is just "USA" then it'll keep it
	s = s.lower().strip();
	if(s.find("usa") != -1 and len(s) > 3):
		# Remove USA!
		s = s.replace("usa","");
		# Remove any comma's too 
		s = s.replace(",","");
		# Or slashes 
		s = s.replace("/","");
		s = s.strip();
	elif(s.find("us") != -1 and len(s) > 3):
		s = s.replace("us","");
		s = s.replace(",","");
		s = s.replace("/","");
		s = s.strip();
	# Manually fix other cases 
	cleaningMap = {
		'united states': 'usa',
		'united states of america/minnesota': us.states.lookup('mn').name,
		'united states/iowa': us.states.lookup('ia').name,
		'montana!!!!! yay': us.states.lookup('mt').name,
		'u.s.a. - minnesota': us.states.lookup('mn').name,
		'the state of being':'usa', #I'm making an assumption that this cheeky response is most likely American
		'washington state': us.states.lookup('wa').name,
		'u.s., tn': us.states.lookup('tn').name,
		'us':'usa',
		'america':'usa',
		'chicago':  us.states.lookup('il').name, # Chicago is not a state..
		'il. also, that\'s the one of the most vile things i\'ve ever heard. although, i\'d dip my pizza in milk, keep it low key tho.':us.states.lookup('il').name,
		'texas/minnesota': us.states.lookup('tx').name,
		'washington, dc': us.states.lookup('wa').name ,
		'(no specific state)': 'usa', # The fact that they don't want to enter their state implies they're in the US
	}
	for key in cleaningMap:
		if(key == s):
			s = cleaningMap[s];
			break;

	return s; 

# Read all the rows except for the header 
dataRows = [];
headerRow = [];
with open('../data/1_Pizza_And_Ketchup.csv', newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	isHeader = True;
	for row in reader:
		if(not isHeader):
			clean_location = CleanUSA(row[2]);
			if(us.states.lookup(clean_location) != None): clean_location = us.states.lookup(clean_location).name;
			dataRows.append({'timestamp':row[0],'pizza_thoughts':row[1],'location':clean_location})
		else:
			headerRow = row;
		isHeader = False;

# Find out total yes/no/maybe responses
pizza_feelings = {'love':0,'hate':0,'meh':0};
pizza_feelings_map = {
	"Oh god no, that's disgusting":'hate',
	"Of course! I do it all the time":'love',
	"I have no strong feelings":'meh'
}
for datum in dataRows:
	sentiment = pizza_feelings_map[datum['pizza_thoughts']];
	pizza_feelings[sentiment] += 1;

print(pizza_feelings) # {'love': 2, 'meh': 29, 'hate': 113}
print("Total: " + str(len(dataRows))) # Total: 144

# Where are those two love's from?
print("");
print("Pizza+Ketchup Lovers are from:\n")
for datum in dataRows:
	if(datum['pizza_thoughts'] == "Of course! I do it all the time"):
		print("\t"+datum['location'])
		# Massachusetts & Minnesota

# Look at the most common locations 
locCount = {};
aggregateData = {};
for datum in dataRows:
	location = datum['location'];
	# Group all non-us together 
	if(location != "usa" and us.states.lookup(location) == None):
		location = "non-us"
	if(not (location in locCount) ):
		locCount[location] = 0;
		aggregateData[location] = {'love':0,'hate':0,'meh':0};
	locCount[location] += 1;

	sentiment = pizza_feelings_map[datum['pizza_thoughts']];
	aggregateData[location][sentiment] += 1;

for loc in locCount:
	if(locCount[loc] >=5 ):
		print(loc,locCount[loc])
# Minnesota 46
# Illinois 20
# non-us 19
# usa 13
# Wisconsin 6
# California 5

# Write out just those top locations in aggregate 
with open('../data/1_Pizza_And_Ketchup_Aggregate.csv', 'w', newline='') as csvfile:
	writer = csv.writer(csvfile, delimiter=',')
	writer.writerow(['Location','Hate','Meh','Love'])
	places = ['Minnesota','Illinois','Non-US','US (other)','Wisconsin','California']
	for p in places:
		location = p;
		if(location == "Non-US"):
			location = "non-us";
		if(location == "US (other)"):
			location = "usa"
		sentiment = aggregateData[location];
		writer.writerow([p,sentiment['hate'],sentiment['meh'],sentiment['love']])

# Create a time series, with just total responses 
with open('../data/1_Pizza_And_Ketchup_TimeSeries.csv', 'w', newline='') as csvfile:
	writer = csv.writer(csvfile, delimiter=',')
	writer.writerow(['Time (hour)','Responses'])
	count = 1;
	for datum in dataRows:
		dt = parser.parse(datum['timestamp']);
		if(dt.day == 30):
			time = dt.hour + (dt.minute / 60) + (dt.second / (60 * 60))
			writer.writerow([time,count])
		count += 1

# Let's now write out the cleaned data 
with open('../data/1_Pizza_And_Ketchup_Clean.csv', 'w', newline='') as csvfile:
	writer = csv.writer(csvfile, delimiter=',')
	# Write header
	writer.writerow(headerRow);
	# Write all the cleaned data
	for datum in dataRows:
		sentiment = pizza_feelings_map[datum['pizza_thoughts']];
		location = datum['location'];
		writer.writerow([datum['timestamp'],sentiment,location])

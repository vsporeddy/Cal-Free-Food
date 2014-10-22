import re
import os

#Some sketchy regex and search parameters at the moment...

current_month = 'October'

def get_date(string):
  	start_month = current_month
  	start_month_short = start_month[:3]
  	return list(set(re.findall('.oday|.omorrow', string) + re.findall(start_month+' \d\d|'+start_month_short+' \d\d|\d\d '+start_month+'|\d\dth '+start_month+'|'+start_month+' \d\dth', string)))
 
def get_time(string):
	return list((re.findall('\d\d:\d\d', string) + re.findall('\d:\d\d', string) + re.findall('\d\dpm', string) + re.findall('\dpm', string)))

def get_food(string):
	if "izza" in string:
		return "Pizza"
	if "dinner" in string or "Dinner" in string:
		return "Dinner"
	if "lunch" in string or "Lunch" in string:
		return "Lunch"
	if "drink" in string or "Drink" in string:
		if "food" in string or "Food" in string:
			return "Food and drinks"
		return "Drinks"
	return "Food"

def getlist():
	events = [event for event in os.listdir('./platter/') if event != '.DS_Store' and event != '.txt' and event != '.html']
	dates = []
	foods = []
	times = []
	for a in events:
		currentfile = open('./platter/' + a, 'r').read() 
		date = get_date(currentfile)
		food = get_food(currentfile)
		time = get_time(currentfile)
		if date == []:
			date = ["Date not found"]
		if time == []:
			time = ["Time unknown"]

		dates += [date[0]]
		foods += [food]
		times += [time[0]]

	eventlinks = [a.split('.')[0] for a in events]
	ziplist = zip(eventlinks, dates, foods, times)
	ziplist.sort(key = lambda t: t[1], reverse=True) 
	return ziplist
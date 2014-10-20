import re
import os

#Some sketchy regex and search parameters at the moment...


def regex(string):
  start_month = 'October'
  start_month_short = start_month[:3]
  return list(set(re.findall('.oday|.omorrow', string) + re.findall(start_month+' \d\d|'+start_month_short+' \d\d|\d\d '+start_month+'|\d\dth '+start_month+'|'+start_month+' \d\dth', string)))
 
def get_time(string):
	return list((re.findall('\d\d:\d\d', string) + re.findall('\d:\d\d', string) + re.findall('\dpm', string)))

def get_food(string):
	print string
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
	#return list(set(re.findall('food', string) + re.findall('drink', string) + re.findall('lunch', string) + re.findall('dinner', string) + re.findall('pizza', string) + re.findall('barbecue', string)))

def getlist():
	events = [event for event in os.listdir('./platter/') if len(event) > 9]
	dates = []
	foods = []
	times = []
	for a in events:
		currentfile = open('./platter/' + a, 'r').read() 
		date = regex(currentfile)
		food = get_food(currentfile)
		time = get_time(currentfile)
		if date == []:
			date = ["Date not found"]
		if time == []:
			time = ["Time unknown"]
		#print a
		#print date[0]
		dates += [date[0]]
		foods += [food]
		times += [time[0]]
		#if a == '.txt' or a =='.DS_Store':
		#	events.remove(a)

	eventlinks = [a.split('.')[0] for a in events]
	ziplist = zip(eventlinks, dates, foods, times)
	ziplist.sort(key = lambda t: t[1], reverse=True) 
	return ziplist
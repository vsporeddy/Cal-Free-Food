import re
import os
import datetime

files = [f for f in os.listdir('./platter/')] #Get a list of all files in current directory

email_list = []

for f in files:
	current_file = open('./platter/'+ f, 'r+')
	email_list.append([current_file,current_file.read(),'./platter/'+f, f])


print(email_list)

file_object = lambda x: x[0]
content = lambda x: x[1]
file_address = lambda x: x[2]
file_name = lambda x: x[3]

def regex(string):
	start_date = 18
	end_date = 20
	start_month = 'October'
	search_result =  re.findall('..............................Today..............................|..............................Tomorrow..............................|..............................today..............................|..............................tomorrow..............................', string) + re.findall('..............................Oct 18..............................|..............................October 18..............................|..............................Oct 19..............................|..............................October 19..............................|..............................Oct 20..............................|..............................October 20..............................|..............................18th October..............................|..............................19th October..............................|..............................20th October..............................', string) # re.findall(start_month[:3]+'|'+start_month+' ['+str(start_date)+'-'+str(end_date) +']', string) + re.findall('['+str(start_date)+'-'+str(end_date) +'] '+start_month[:3]+'|'+start_month+'', string) + re.findall('['+str(start_date)+'-'+str(end_date) +']th Oct|'+start_month+'', string)
	return search_result

for email in email_list:
	reg=regex(content(email))
	if len(reg)>0:
		t = open(file_address(email), 'w+')
		t.write( file_name(email) + "\nExcerpt:"+ str(reg)+ "\n\n" content(email) )
	else:
		file_object(email).close()
		os.remove(file_address(email))

..............................
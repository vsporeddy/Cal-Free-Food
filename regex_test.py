import re
import os

files = ['./platter/'+f for f in os.listdir('./platter/')] #Get a list of all files in current directory

email_list = []

for f in files:
	current_file = open(f, 'r+')
	email_list.append([current_file,current_file.read(),f])

print(email_list)

file_object = lambda x: x[0]
content = lambda x: x[1]
file_address = lambda x: x[2]

def regex(string):
 return str(re.match("word", string))

for email in email_list:
	r=regex(content(email))
	if r:
		file_object(email).write(r)
	else:
		os.remove(file_address(email))
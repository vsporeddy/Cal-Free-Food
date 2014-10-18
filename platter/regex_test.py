import re
import os

files = [f for f in os.listdir('.') if os.path.isfile(f)] #Get a list of all files in current directory

email_list = []

for f in files:
	current_file = open(f, 'r')
	email_list.append([f,current_file.read()])

print(email_list)

#file_name = lambda x: x[0]
#email_content = lambda x: x[1]




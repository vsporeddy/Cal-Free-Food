import os
import re
from flask import Flask, render_template, send_from_directory, send_file

# initialization
app = Flask(__name__)
app.config.update(
    DEBUG = True,
)

def regex(string):
  start_month = 'October'
  start_month_short = start_month[:3]
  return list(set(re.findall('.oday|.omorrow', string) + re.findall(start_month+' \d\d|'+start_month_short+' \d\d|\d\d '+start_month+'|\d\dth '+start_month+'|'+start_month+' \d\dth', string)))
 

# controllers
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'ico/favicon.ico')

@app.route('/platter/<path>')
def static_proxy(path):
	return send_file("./platter/" + path + '.txt')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/")
def index():
	events = [event for event in os.listdir('./platter/') if len(event) > 9]
	dates = []
	for a in events:
		currentfile = open('./platter/' + a, 'r') 
		date = regex(currentfile.read())
		if date == []:
			date = ["Date not found"]
		print a
		print date[0]
		dates += [date[0]]
		#if a == '.txt' or a =='.DS_Store':
		#	events.remove(a)

	eventlinks = [a.split('.')[0] for a in events]
	ziplist = zip(eventlinks, dates)
	return render_template('index.html', events = eventlinks, dates = dates, ziplist = ziplist)


# launch
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
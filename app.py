import os
import regexpy
import free_food
from flask import Flask, render_template, send_from_directory, send_file



# initialization
app = Flask(__name__)
app.config.update(
    DEBUG = True,
)

# controllers
@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'), 'ico/favicon.ico')

@app.route('/platter/<path>')
def static_proxy(path):
	return render_template(path + '.html')

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.route("/")
def index():
	free_food.run()
	return render_template('index.html', ziplist = regexpy.getlist())


# launch
if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)



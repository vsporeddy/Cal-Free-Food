from flask import Flask, render_template, request
app = Flask(__name__, static_folder='static', static_url_path='')

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['platter'],
                               filename)
if __name__ == "__main__":
    app.debug = True
    app.run()

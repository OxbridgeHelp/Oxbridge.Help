from flask import Flask, render_template
app = Flask(__name__)
app._static_folder = "/home/dev/oxbridgehelp-dev/static"

@app.route("/")
def main():
	return render_template('home.html')

@app.route("/privacy")
def show_privacy_notice():
	return render_template('privacy.html')

if __name__ == "__main__":
    # remove 'debug=True' when publishing
	app.run(host='0.0.0.0', debug=True)

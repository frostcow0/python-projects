import logging
from flask import Flask, render_template, request
from main import run_flow
    

app = Flask(__name__, static_folder='static',
    template_folder='templates')

logging.basicConfig(level=logging.INFO)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        logging.info(" Made a POST request!")
        run_flow()
    else:
        logging.info(" Made a GET request!")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

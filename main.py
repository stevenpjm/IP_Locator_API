from flask import Flask, render_template
from python import runTasks, fileupdate
import logging
from dotenv import load_dotenv
import os, json


def configure():
    load_dotenv()


app = Flask(__name__)


def domaincheck():
    runTasks.scheduleTasks()


@app.route('/', methods=['GET'])
def index():
    try:
        #get most recent results from audit trail
        mostrecentfile = fileupdate.most_recent_file_from_audit()
        mostrecentresult = json.loads(fileupdate.open_file_retrieve_data(mostrecentfile))

        #get info about the last run
        file = os.getenv('lastrun')
        lastrundata = json.loads(fileupdate.open_file_retrieve_data(file))


        return render_template("IPChecker.html", lastrundata=lastrundata, mostrecentresult=mostrecentresult)

    except Exception as e:
        return "issue with task, please contact your admin"


@app.route('/results')
def results():
    logger = logging.getLogger()
    try:
        file = os.getenv('lastrun')
        lastrundata = dict(fileupdate.open_file_retrieve_data(file))
        # runs the check on domain and retrieves the deatils
        domaincheck()
        return render_template("IPChecker.html", lastrundata=lastrundata)
    except Exception as e:
        return "issue with task, please contact your admin"


if __name__ == '__main__':
    app.run(debug=True)

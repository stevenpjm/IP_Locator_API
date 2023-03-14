import json
from decouple import config
from flask import Flask, render_template
from python import runTasks, fileupdate
from waitress import serve


def domaincheck():
    runTasks.scheduleTasks()


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    file = ""
    historicdata = ""
    mostrecentfile = ""
    lastrundata = {}
    mostrecentresult = {}

    try:
        # get most recent results from audit trail
        mostrecentfile = fileupdate.most_recent_file_from_audit()
        openfilewithdate = fileupdate.open_file_retrieve_data(mostrecentfile)
        mostrecentresult = json.loads(openfilewithdate)
        # get info about the last run
        file = config('lastrun')
        historicdata = fileupdate.open_file_retrieve_data(file)
        lastrundata = json.loads(historicdata)
        return render_template("IPChecker.html", lastrundata=lastrundata, mostrecentresult=mostrecentresult)

    except Exception as e:
        if mostrecentfile == "Issue with retrieving most recent file":
            return "Issue with retrieving most recent file"
        elif len(mostrecentresult) == 0:
            return "issue with file most recent result, File retrieved : " + str(mostrecentfile)
        elif file is None:
            return "issue with environment variable, set to : " + str(file)
        elif historicdata is None:
            return "issue with "
        elif len(lastrundata) == 0:
            return "issue with retrieving the json information from : " + str(file)
        else:
            return "issue with webpage"


@app.route('/results')
def results():
    try:
        file = config('lastrun')
        lastrundata = dict(fileupdate.open_file_retrieve_data(file))
        # runs the check on domain and retrieves the deatils
        domaincheck()
        return render_template("IPChecker.html", lastrundata=lastrundata)
    except Exception as e:
        return "issue with return results from manual run , please contact your admin" + e


mode = "dev"

if __name__ == '__main__' and mode == "dev":
    app.run(debug=True)
elif __name__ == '__main__' and mode == "prod":
    serve(app, host='0.0.0.0', port=80, threads=2, url_prefix="/")
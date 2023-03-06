from flask import Flask, render_template
from python import runTasks, fileupdate
import logging

app = Flask(__name__)

@app.route('/')
def index():
    logger = logging.getLogger()
    runTasks.scheduleTasks()
    try:
        return render_template("APIResults.html")
    except:
        return "Page down for Maintenance, please contact the admin"

@app.route('/results')
def results():
    logger = logging.getLogger()
    try:
        runTasks.runmanually()
        return
    except Exception as e:
        return logger.exception("Exception Occured while code Execution: " + str(e))


if __name__ == '__main__':
    app.run(debug=True)


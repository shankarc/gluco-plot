# Fri May 22 13:22:09 EDT 2015
# The idea is to plot glucose chart using pygal
# http://www.blog.pythonlibrary.org/2015/04/16/using-pygal-graphs-in-flask/
# Read the csv file
#   extract the date,time, mg/dl reading
#   plot the graph
#(http://flask.pocoo.org/docs/0.10/tutorial/folders/#tutorial-folders)
# http://code.tutsplus.com/tutorials/an-introduction-to-pythons-flask-framework--net-28822
#(http://flask.pocoo.org/docs/0.10/patterns/fileuploads/)
#[Data42: Simple SVG charts with HBase REST service, Flask and Pygal](http://data42.blogspot.com/2014/08/simple-svg-charts-with-hbase-rest.html)
#[How can I get the whole request POST body in Python with Flask? - Stack Overflow](http://stackoverflow.com/questions/10434599/how-can-i-get-the-whole-request-post-body-in-python-with-flask)
#[How to download a file generated on-the-fly in Flask for Python Code Example - Runnable](http://code.runnable.com/UiIdhKohv5JQAAB6/how-to-download-a-file-generated-on-the-fly-in-flask-for-python)
# http://jsonformatter.curiousconcept.com/
# Good document on flask
#[openshift-quickstart/flask-base](https://github.com/openshift-quickstart/flask-base)
import os
from werkzeug import secure_filename
from flask import Flask, request, render_template, redirect, url_for,  make_response
from read_csv import ReadCSV as readcsv
import tempfile
from plot import PlotGluco as glucoplot
import yaml
import logging
from logging.handlers import RotatingFileHandler

tmpl_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


class Config():
    file_name = None
    csvFormat = dict()


def init(jsonfile):
    """
    load the format of CSV file from YAML
    """
    for i in yaml.load(open(jsonfile)):
        Config.csvFormat.update(i)


#----------------------------------------------------------------------

@app.route('/upload', methods=["GET", "POST"])
def upload():
    # for POST
    if request.method == 'POST' and 'csv' in request.files:
        file = request.files['csv']
        filename = secure_filename(file.filename)
        Config.file_name = os.path.join(
            os.path.join(tempfile.gettempdir(), filename))
        file.save(Config.file_name)
        return redirect(url_for('home'))
# for GET
    return render_template('upload.html')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/plot', methods=["GET", "POST"])
def plot():
    if request.method == 'POST':
        frmt = str(request.values['filetype'])
        plot_type = str(request.values['plottype'])
        render = str(request.values['render'])
        app.logger.info('format={0} plot_type={1} render={2}'.format(frmt, plot_type, render))
        xaxis, yaxis =  readcsv(Config.csvFormat[frmt], Config.file_name).extract()
        #print 'xaxis={0} yaxis ={1}'.format(xaxis,yaxis)
        #return "DONE"
        if len(xaxis) == 0 or len(yaxis) == 0:
            return render_template('error.html')
        if 'plot' in render:
            return glucoplot().render_graph(plot_type, xaxis, yaxis)
        if 'file' in render:
            svg = glucoplot().render_graph(
                plot_type, xaxis, yaxis, renderTofile=True)
            response = make_response(svg)
            # Set the right header for the response
            # to be downloaded, instead of just printed on the browser
            filename = '{filetype}-{plottype}-chart-{start}-to-{end}.svg'.format(
                filetype=frmt, plottype=plot_type, start=xaxis[0], end=xaxis[-1])
            response.headers[
                 "Content-Disposition"] = 'attachment; filename={0}'.format(secure_filename(filename))
            return response
        return "Something went wrong!"
# for GET
    if not Config.file_name:
        return "You have to upload the file before plotting"
    return render_template('type.html')

#----------------------------------------------------------------------
if __name__ == '__main__':
    init('format.json')
    #app.run(host='0.0.0.0', port=5000, debug=True)
    handler = RotatingFileHandler('mylog.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(debug=True)

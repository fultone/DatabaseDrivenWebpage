'''
    flask_app.py
    Jeff Ondich, 22 April 2016
    Modified by Eric Alexander, January 2017
    Modified by Web Project Pair E, October 2017
'''
import flask
from flask import render_template, request
import json
import sys
from datasource import *

app = flask.Flask(__name__)

''' 
    Renders the homepage. 
'''
@app.route('/')
def homepage():
    return render_template('index.html')

''' 
    Renders the homepage when the site ID or the "Home" tab is selected. 
'''
@app.route('/home/')
def homepageRedirect():
    return render_template('index.html')

''' 
    Renders the Search Sightings page which allows the user to search the UFO 
    database. 
'''
@app.route('/sightings/')
def sightings():
    return render_template('sightings.html')

''' 
    Renders the results of the user's search from the UFO database. 
'''
@app.route('/result', methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        ufoData = DataSource(result['searchFilters'], result['searchBox'])
        searchResults = ufoData.searchDatabase() 
        return render_template("result.html", result=searchResults)

''' 
    Renders the Shop page, which displays various items for purchase. 
'''
@app.route('/shop/')
def shop():
    return render_template('shop.html')

''' 
    Renders the Contact page with information to contact the website creators. 
'''
@app.route('/contact/')
def contact():
    return render_template('contact.html')

''' 
    Runs this file with command-line arguments [filename] [host] [port]. 
'''
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()
    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port)
    app.run(debug=True)
#!flask/bin/python
from flask import Flask
import MySQLdb



app = Flask(__name__)
@app.route('/')
def index():
    return "Hello, World!"

#handle walking by the store
#http://ourserver.cloud.google.com/bookstore/nearby
@app.route('/bookstore/nearby')
def nearbyBookstore( ):
	#check if they've picked up textbooks
	#if not, respond to notify to grab them
	# Open database connection
	db = MySQLdb.connect("localhost","root","D0nkeyba!!s","mobievent" )

	# prepare a cursor object using cursor() method
	cursor = db.cursor()

	# execute SQL query using execute() method.
	cursor.execute("SELECT VERSION()")

	# Fetch a single row using fetchone() method.
	data = cursor.fetchone()

	print "Database version : %s " % data

	# disconnect from server
	db.close()
	return "Database version : %s " % data



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
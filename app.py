#!flask/bin/python
from flask import Flask
from flask import jsonify
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
	cursor.execute("Select ISBN from BookCourse where CID in ( SELECT CID from Enroll where SID = 4)")

	# Fetch a single row using fetchone() method.
	data = cursor.fetchall()
	
	for row in data:
		print row


	# disconnect from server
	db.close()
	return jsonify(data)

# put in SID as param later
@app.route('/classroom/attendance/signin')
def signIn():
	#check if they've picked up textbooks
	#if not, respond to notify to grab them
	# Open database connection
	db = MySQLdb.connect("localhost","root","D0nkeyba!!s","mobievent" )

	# prepare a cursor object using cursor() method
	cursor = db.cursor()

	# execute SQL query using execute() method.
	cursor.execute("use mobievent")
	cursor.execute("INSERT INTO Attendance values (372, 1, CURRENT_TIMESTAMP, True")

	print "attendance input successful"

	# disconnect from server
	db.close()
	return 0
	
	

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
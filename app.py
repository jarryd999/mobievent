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
	
	ret = ""
	
	for row in data:
		for elem in row:
			print elem	
			ret += str(elem)
			ret += "\n"


	# disconnect from server
	db.close()
	return jsonify( {'result' : data})


#check what books student needs to buy, prompt if (s)he wants to buy now
#output: (int) 0 if they don't need books, 1 if they do
@app.route('/bookstore/onEnter')
def insideBookstore( ):
	# Open database connection
	db = MySQLdb.connect("localhost","root","D0nkeyba!!s","mobievent" )

	# prepare a cursor object using cursor() method
	cursor = db.cursor()
	
	# execute SQL query using execute() method.
	cursor.execute("Select ISBN from BookCourse where CID in ( SELECT CID from Enroll where SID = 4)")

	# Fetch a single row using fetchone() method.
	data = cursor.fetchall()
	# disconnect from server
	db.close()
	
	#check if there are books they need, return true if so
	if data.size > 0:
		return 1;
	return 0;	

#check what books student needs to buy
@app.route('/bookstore/fetchBooks/<studentid>')
def fetchBooks(studentid):
	# Open database connection
	db = MySQLdb.connect("localhost","root","D0nkeyba!!s","mobievent" )

	# prepare a cursor object using cursor() method
	cursor = db.cursor()
	
	# execute SQL query using execute() method.
	cursor.execute("select distinct Book.ISBN, Book.Name, Book.Price from BookCourse, Book, Enroll where Bo\
okCourse.CID = Enroll.cid and Book.ISBN = BookCourse.ISBN and sid = " + studentid)

	# Fetch a single row using fetchone() method.
	data = cursor.fetchall()
	# disconnect from server
	db.close()

	return jsonify({'result' : data})

# returns 1 if signIn was successful
# returns 0 if not successful
@app.route('/classroom/attendance/signin/<classid>/<studentid>')
def signIn(classid, studentid):
	#check if they've picked up textbooks
	#if not, respond to notify to grab them
	# Open database connection
	db = MySQLdb.connect("localhost","root","D0nkeyba!!s","mobievent" )

	# prepare a cursor object using cursor() method
	cursor = db.cursor()

	output = 0
	try:
		# execute SQL query using execute() method.
		cursor.execute("INSERT INTO Attendance values (" + classid + ", " + studentid + ", CURRENT_TIMESTAMP, True)")
		db.commit()
		output = 1
	except MySQLdb.IntegrityError:
		output = 0
	finally:
		# disconnect from server
		db.close()
		
	return jsonify({'result' : output})
	
# return 1 if student was already signed in, 0 if not signedin yet
@app.route('/classroom/attendance/checksignedin/<classid>/<studentid>')
def checkSignedIn(classid, studentid):
	# Open database connection
	db = MySQLdb.connect("localhost","root","D0nkeyba!!s","mobievent" )

	# prepare a cursor object using cursor() method
	cursor = db.cursor()
	
	# execute SQL query using execute() method.
	cursor.execute("SELECT * FROM Attendance where sid = " + studentid + " and cid = " + classid + " and date(date) = curdate()")
	data = cursor.fetchall()
	
	db.close()
	
	if len(data)>0:
		return jsonify({'result' : data})
		
	return jsonify({'result' : 0})
	
# return all students who are signed into attendance for the day
@app.route('/classroom/attendance/getsigninlist/<classid>')
def getSignInList(classid):
	# Open database connection
	db = MySQLdb.connect("localhost","root","D0nkeyba!!s","mobievent" )

	# prepare a cursor object using cursor() method
	cursor = db.cursor()
	
	# execute SQL query using execute() method.
	cursor.execute("select distinct Student.sid, Student.name from Student, Attendance where Student.sid = \
Attendance.sid and date(date) = curdate() and cid = " + classid)
	data = cursor.fetchall()
	
	db.close()
	
	return jsonify( {'result' : data} )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
#!flask/bin/python
from flask import Flask
from flask import jsonify
import math
import MySQLdb


class QTNode:
	paintCount = 0
	nw = None
	ne = None
	sw = None
	se = None
	parent = None

	def __init__(self, color, topX, topY, botX, botY):
		self.color = color
		self.topX = topX
		self.topY = topY
		self.botX = botX
		self.botY = botY
		self.paintCount = 0

	def switchColor():
		self.color = not self.color
		self.paintCount += 1
		# temp commenting
		#if self.paintCount == 3:
		#	paintedThrice.append([topX, topY])



app = Flask(__name__)
root = QTNode(False, 0, 0, 64, 64)
paintedThrice = [];

def buildQT(node):
	if node.topX == (node.botX+1) and (node.topY+1) == node.botY:
		return # stop, leaf node
	
	centerX = (botX - topX) / 2
	centerY = (botY - topY) / 2
	
	node.nw = QTNode(False, topX, topY, centerX, centerY)
	node.ne = QTNode(False, centerX, topY, botX, centerY)
	node.sw = QTNode(False, topX, centerY, centerX, botY)
	node.se = QTNode(False, centerX, centerY, botX, botY)
	buildQT(node.nw)
	buildQT(node.ne)
	buildQT(node.sw)
	buildQT(node.se)

@app.route('/')
def index():
    return "Hello, World!"
	
#handle walking by the store
#http://ourserver.cloud.google.com/bookstore/nearby
@app.route('/bookstore/nearby/<studentid>')
def nearbyBookstore( studentid ):
	#check if they've picked up textbooks
	#if not, respond to notify to grab them
	# Open database connection
	db = MySQLdb.connect("localhost","root","D0nkeyba!!s","mobievent" )

	# prepare a cursor object using cursor() method
	cursor = db.cursor()
	
	# execute SQL query using execute() method.
	#cursor.execute("Select ISBN from BookCourse where CID in ( SELECT CID from Enroll where SID = " + SID + ") and ISBN NOT IN ( SELECT ISBN FROM Reservation where SID = " + SID + ")")
	cursor.execute("select distinct Book.ISBN, Book.Name, Book.Price from BookCourse, Book, Enroll where Enroll.CID = BookCourse.CID and BookCourse.ISBN = Book.ISBN and SID = " + studentid + " and Book.ISBN not in (select BookReservation.ISBN from BookReservation where SID = " + studentid + ")")
	
	# Fetch a single row using fetchone() method.
	data = cursor.fetchall()

	# disconnect from server
	db.close()
	return jsonify( {'result' : data})

# don't use for now, need to json the output and determine what to return
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
@app.route('/bookstore/fetchbooks/<studentid>')
def fetchBooks(studentid):
	# Open database connection
	db = MySQLdb.connect("localhost","root","D0nkeyba!!s","mobievent" )

	# prepare a cursor object using cursor() method
	cursor = db.cursor()
	
	# execute SQL query using execute() method.
	cursor.execute("select distinct Book.ISBN, Book.Name, Book.Price from BookCourse, Book, Enroll where BookCourse.CID = Enroll.cid and Book.ISBN = BookCourse.ISBN and sid = " + studentid)

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
	print "pre-sign in query"
	try:
		# execute SQL query using execute() method.
		cursor.execute("INSERT INTO Attendance values (" + classid + ", " + studentid + ", CURRENT_TIMESTAMP, True)")
		db.commit()
		output = 1
		print "output was set to 1 from successful sql query"
	except MySQLdb.IntegrityError:
		print "IntegrityError occured in signIn"
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
		return jsonify({'result' : 1})
		
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

@app.route('/map/getCoords/<TX1>/<TX2>/<TX3>')
def getCoords(TX1, TX2, TX3):

	print TX1
	print TX2
	print TX3
	
	paint(root, 0, 0, int(TX1));
	paint(root, 32, 64, int(TX2));
	paint(root, 64, 0, int(TX3));
	xCord = 0
	yCord = 0

	for tuple in paintedThrice:
		xCord += tuple.topX;
		yCord += tuple.topY;

	if not len(paintedThrice) == 0:
		ret = [xCord / len(paintedThrice), yCord / len(paintedThrice)]
	else:
		ret = [-1,-1]
	return jsonify({'data':ret})

# need to initialize the quadtree

def contains(region, centerX, centerY):
	return centerX > region.topX and centerX < region.botX and centerY > region.topY and centerY < region.botY

def exploreTree(node):
	if node is None:
		return
	if node.color = True and node.paintCount >= 3:
		paintedThrice.append(node)
	
	exploreTree(node.nw)
	exploreTree(node.ne)
	exploreTree(node.sw)
	exploreTree(node.se)
	
def paintCrawlIncrementUp(region):
	## temporary
	return
	region.paintCount += 1
	if region == root:
		return
	paintCrawlIncrementUp(region.parent)

def paintCrawl(region, flag):
	region.paintCount += 1

	if flag:
		paintCrawlIncrementUp(region.parent)

	if isLeaf(region):
		region.switchColor()
		return
	paintCrawl(region.nw, False)
	paintCrawl(region.ne, False)
	paintCrawl(region.sw, False)
	paintCrawl(region.se, False)

def paint(region, centerX, centerY, radius):
	if region == None:
		return
	offset = radius * math.cos(math.radians(45))
	if (not contains(region, centerX, centerY) and not contains(region, centerX + offset, centerY + offset) 
	and not contains(region, centerX + offset, centerY - offset) and not contains(region, centerX - offset, centerY + offset)
	and not contains(region, centerX - offset, centerY - offset) and not contains(region, centerX + radius, centerY)
	and not contains(region, centerX - radius, centerY) and not contains(region, centerX, centerY + radius)
	and not contains(region, centerX, centerY - radius)):
		return
	distanceTop = math.sqrt( (region.topX - centerX)**2 + (region.topY - centerY)**2)
	distanceBot = math.sqrt( (region.botX - centerX)**2 + (region.botY - centerY)**2)
	if distanceTop < radius and distanceBot < radius:
		paintCrawl(region, True)

	print "nw"
	paint(region.nw, centerX, centerY, radius)
	print "ne"
	paint(region.ne, centerX, centerY, radius)
	print "sw"
	paint(region.sw, centerX, centerY, radius)
	print "se"
	paint(region.se, centerX, centerY, radius)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
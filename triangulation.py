import math
from graphics import *

def main():
#	print("test inputs here")
	win = GraphWin("Quad-tree", 16, 16)
	root = QTNode(Color.BLACK, 0, 0, 16, 16)
	buildQT(root)
	root.display(win)
	win.getMouse()
	
# display with text maybe instead of doing the graphics

class QTNode:
	def __init__(self, color, topX, topY, botX, botY):
		self.color = color
		self.topX = topX
		self.topY = topY
		self.botX = botX
		self.botY = botY
		self.paintCount = 0
		self.nw = None
		self.ne = None
		self.sw = None
		self.se = None
		self.parent = None

	def switchColor(self):
		if self.color == Color.RED:
			self.color = Color.BLACK
		elif self.color == Color.BLACK:
			self.color = COlor.RED
		else:
			print "CRITICAL ERROR: COLOR WAS NOT RED OR BLACK"
		
	def addPaintCount(self):
		self.paintCount += 1
		
	def display(self, g):
		if self == None:
			return
			
		# draw self
		rect = Rectangle(Point(self.topX, self.topY), Point(self.botX, self.botY))
		if self.color == Color.BLACK:
			rect.setFill("black")
		elif self.color == Color.RED:
			rect.setFill("red")
		else:
			print "CRITICAL ERROR IN DISPLAY: COLOR WRONG"
			return
		rect.draw(g)
		
		# recurse
		self.display(g)
		self.display(g)
		self.display(g)
		self.display(g)
	
	def toString(self):
		return "topX: " + str(self.topX) + " topY: " + str(self.topY) + " botX: " + str(self.botX) + " botY: " + str(self.botY) + " color: " + str(self.color)
	
# enum
class Color:
	RED = 1
	BLACK = 2

# need to check this one still
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

# checked!
def buildQT(node):
	if (node.topX+1) == node.botX and (node.topY+1) == node.botY:
#		print "BASE CASE REACHED"
		return # stop, leaf node
	
	centerX = (node.botX + node.topX) / 2
	centerY = (node.botY + node.topY) / 2
	
	# create four childrens
	node.nw = QTNode(Color.BLACK, node.topX, node.topY, centerX, centerY)
	node.ne = QTNode(Color.BLACK, centerX, node.topY, node.botX, centerY)
	node.sw = QTNode(Color.BLACK, node.topX, centerY, centerX, node.botY)
	node.se = QTNode(Color.BLACK, centerX, centerY, node.botX, node.botY)
	# set children's parent pointers to self
	node.nw.parent = node
	node.ne.parent = node
	node.sw.parent = node
	node.se.parent = node
	# recurse to children
#	print "nw" + node.nw.toString()
	buildQT(node.nw)
#	print "ne" + node.ne.toString()
	buildQT(node.ne)
#	print "sw" + node.sw.toString()
	buildQT(node.sw)
#	print "se" + node.se.toString()
	buildQT(node.se)


def contains(region, centerX, centerY):
	return centerX > region.topX and centerX < region.botX and centerY > region.topY and centerY < region.botY

def exploreTree(node):
	if node is None:
		return
	if node.paintCount > 0:
		print "found something" + node.topX + " " + node.topY
	if node.color == True and node.paintCount >= 3:
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

	if region == None:
		return
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
	print "region: " + str(region.topX) + "," + str(region.topY) + "|" + str(region.botX) + "," + str(region.botY)
	print "---dTop: " + str(distanceTop) + ", dBot: " + str(distanceBot)
	if distanceTop <= radius and distanceBot <= radius:
		print "paintcrawl started"
		paintCrawl(region, True)

	print "nw"
	paint(region.nw, centerX, centerY, radius)
	print "ne"
	paint(region.ne, centerX, centerY, radius)
	print "sw"
	paint(region.sw, centerX, centerY, radius)
	print "se"
	paint(region.se, centerX, centerY, radius)
	
if __name__ == "__main__":
	main()
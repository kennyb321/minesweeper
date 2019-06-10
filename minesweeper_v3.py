#MINESWEEPER APPLICATION

from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import sys
import random




class Minesweeper(QWidget):
	def __init__(self):
		super().__init__()
		self.initui()

	def initui(self):
		self.flag_active = False

		self.layoutGrid = QGridLayout()
		
		

		

		#create grid
		self.create_board(self)

		#populate grid with 99 random bombs
		self.populate_bombs()

		#test each tile to determine how many bombs are touching that tile
		self.bombs_touching()
		self.setGeometry(300,300,300,300)
		self.setWindowTitle('Minesweeper')
		self.setStyleSheet("background-color: black")
		#ignore this. used for testing purposes
		for i in range(20):
			for j in range(20):
				if self.buttons[i][j]['is_bomb'] == True:
					self.buttons[i][j][(i, j)].setText("B. BC = " + str(self.buttons[i][j]['bombs_touching']))
				elif self.buttons[i][j]['is_bomb'] == False:
					self.buttons[i][j][(i, j)].setText("NB. BC: " + str(self.buttons[i][j]['bombs_touching']))


		#setup top-level menu
		#momb_count lcd
		self.bomb_count_display = QLCDNumber()
		self.bomb_count_display.display(self.num_bombs)

		#resest button
		self.reset_button = QPushButton()
		self.reset_button.setIcon(QIcon("smiley.png"))

		#timer LCD
		self.timer_display = QLCDNumber()
		self.current_time = QTime(0,0,0)
		self.timer_display.display(str(self.current_time))
		self.timer = QTimer()
		self.timer.timeout.connect(self.updateLCD)
		self.timer.start(1000)

		#create set_flag_button
		self.flag_button = QPushButton()
		self.flag_button.setIcon(QIcon('flag.png'))
		self.flag_button.clicked.connect(self.flag_button_clicked)


		#create HBoxLayout
		self.layoutBox = QHBoxLayout()
		self.layoutBox.addWidget(self.bomb_count_display, alignment = Qt.AlignLeft)
		self.layoutBox.addWidget(self.reset_button, alignment = Qt.AlignCenter)
		self.layoutBox.addWidget(self.flag_button, alignment = Qt.AlignCenter)
		self.layoutBox.addWidget(self.timer_display, alignment = Qt.AlignRight)

		self.layoutGrid.addLayout(self.layoutBox,0,0,1,20)



		self.setLayout(self.layoutGrid)
		self.layoutGrid.setSpacing(0.5)
		self.show()



		#create a dictionary of information for each tile in the grid
	def create_dict(self, x, y):
		dict = {(x, y): QPushButton(),
				'is_bomb': False,
				'is_flagged': False,
				'is_clicked': False,
				'bombs_touching': 0
				}
		return dict
		#ignore this. used for testing and debugging purposes
	def print_info(self, x, y):
		print("Coordinates: (" + str(self.x) + ', ' + str(self.y) + ')')
		print("Is bomb: "+ str(self.buttons[self.x][self.y]['is_bomb']))
		print('Is Flagged: ' + str(self.buttons[self.x][self.y]['is_flagged']))
		print("Bombs Touching: " + str(self.buttons[self.x][self.y]['bombs_touching']))
		print("Is Clicked: " + str(self.buttons[self.x][self.y]['is_clicked']))

		#when menu button flag is clicked, allows user to add flag to tiel
		#I couldnt figure out how to add right-click functionality quite yet, so this button
		#for the moment is neccessary
	def flag_button_clicked(self):
		if not self.flag_active:
			self.flag_active = True
		elif self.flag_active:
			self.flag_active = False


			#supposed to determine how many bombs are touching given tile.
			#logic is flawed, as it only returns a bombs_touching_count of 0 and 1
	def bombs_touching(self):
		

		for x in range(20):
			for y in range(20):
				bombs_touching_count = 0
				try:

					if self.buttons[x-1][y-1]['is_bomb'] == True:
						bombs_touching_count = bombs_touching_count + 1
					elif self.buttons[x][y-1]['is_bomb'] == True:
						bombs_touching_count = bombs_touching_count + 1
					elif self.buttons[x+1][y-1]['is_bomb'] == True:
						bombs_touching_count = bombs_touching_count + 1
					elif self.buttons[x][y-1]['is_bomb'] == True:
						bombs_touching_count = bombs_touching_count + 1
					elif self.buttons[x][y+1]['is_bomb'] == True:
						bombs_touching_count = bombs_touching_count + 1
					elif self.buttons[x+1][y-1]['is_bomb'] == True:
						bombs_touching_count = bombs_touching_count + 1
					elif self.buttons[x+1][y]['is_bomb'] == True:
						bombs_touching_count = bombs_touching_count + 1
					elif self.buttons[x+1][y+1]['is_bomb'] == True:
						bombs_touching_count = bombs_touching_count + 1

					self.buttons[x][y]['bombs_touching_count'] = bombs_touching_count

				except IndexError:
					pass



	

		



















		

			



	def create_board(self, x=20, y=20):

		
		self.buttons = [[]]
		#dunno why this works but it does.
		#create 2d list of dictionary items. containing information abpout each grid space
		#first value of disctionaryu (i, j) is QPushButton
		for i in range(20):
			self.buttons = [[self.create_dict(i, j)] * 20 for j in range(20)]

		for i in range(20):
			for j in range(20):
				self.buttons[i][j] = self.create_dict(i, j)
				#self.buttons[i][j][(i, j)].setText(str(i)+  str(j))

		

		self.layoutGrid = QGridLayout()
		for i in range(20):
			for j in range(20):
				self.layoutGrid.addWidget(self.buttons[i][j][(i, j)], i+1, j)
				self.buttons[i][j][(i, j)].x = i
				self.buttons[i][j][(i, j)].y = j
				self.buttons[i][j][(i, j)].setStyleSheet("background-color: red")
				self.buttons[i][j][(i, j)].clicked.connect(self.is_clicked)
				
		
		
		

	def updateLCD(self):
		self.current_time = self.current_time.addSecs(1)
		self.timer_display.display(str(self.current_time))

	def populate_bombs(self):
		self.num_bombs = 200
		self.bomb_count = 0
		while(self.bomb_count < self.num_bombs):
			rx = random.randint(0, 19)
			ry = random.randint(0, 19)
			if (self.buttons[rx][ry]['is_bomb'] == False):
				self.buttons[rx][ry]['is_bomb'] = True
				self.bomb_count += 1

	


	def game_over(self):
		print("Game Over Called")
		for i in range(20):
			for j in range(20):
				if self.buttons[i][j]['is_bomb'] == True:
					self.buttons[i][j][(i, j)].setIcon(QIcon('bomb.png'))
				elif (self.buttons[i][j]['is_flagged'] == False) and (self.buttons[i][j]['is_bomb'] == False):
					self.buttons[i][j][(i, j)].setStyleSheet('background-color:black')


	

		

	def is_clicked(self):


		self.clickedButton = self.sender()
		self.type = type(self.clickedButton)
		print("name: " + str(self.clickedButton))
		print("type: " + str(self.type))
		self.x = self.clickedButton.x
		self.y = self.clickedButton.y
		
		self.buttons[self.x][self.y]['is_clicked'] = True

		if not self.flag_active:

			if(self.buttons[self.x][self.y]['is_bomb'] == True):
				self.game_over()

			else:
				print("No Bomb")

			
			
				self.buttons[self.x][self.y][(self.x, self.y)].setStyleSheet("background-color: black")
				self.buttons[self.x][self.y]['is_clicked'] = True

		elif self.flag_active:
			if self.buttons[self.x][self.y]['is_flagged'] == True:
				self.buttons[self.x][self.y]['is_flagged'] = False
				self.buttons[self.x][self.y][(self.x, self.y)].setIcon(QIcon())





			self.buttons[self.x][self.y]['is_flagged'] = True
			self.flag_count = 0
			self.buttons[self.x][self.y][(self.x, self.y)].setIcon(QIcon('flag.png'))	
			
		self.print_info(self.x, self.y)

		


		

	

if __name__ == '__main__':
	app = QApplication(sys.argv)
	mw = Minesweeper()
	sys.exit(app.exec_())







	
	

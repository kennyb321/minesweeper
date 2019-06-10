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
		
		

		


		self.create_board(self)
		self.populate_bombs()
		for i in range(20):
			for j in range(20):
				self.buttons[i][j]['bombs_touching'] = self.bombs_touching(i, j)
		self.setGeometry(300,300,300,300)
		self.setWindowTitle('Minesweeper')
		self.setStyleSheet("background-color: black")
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




	def create_dict(self, x, y):
		dict = {(x, y): QPushButton(),
				'is_bomb': False,
				'is_flagged': False,
				'is_clicked': False,
				'bombs_touching': 0
				}
		return dict

	def print_info(self, x, y):
		print("Coordinates: (" + str(self.x) + ', ' + str(self.y) + ')')
		print("Is bomb: "+ str(self.buttons[self.x][self.y]['is_bomb']))
		print('Is Flagged: ' + str(self.buttons[self.x][self.y]['is_flagged']))
		print("Bombs Touching: " + str(self.buttons[self.x][self.y]['bombs_touching']))
		print("Is Clicked: " + str(self.buttons[self.x][self.y]['is_clicked']))


	def flag_button_clicked(self):
		if not self.flag_active:
			self.flag_active = True
		elif self.flag_active:
			self.flag_active = False

	def bombs_touching(self, x, y):
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

		except IndexError:
			pass

		return bombs_touching_count



















		

			



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







	
	

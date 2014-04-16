from Tkinter import *
import random
import math
import pdb

class Apple:
	def __init__(self, model_border, snake_list, speed):
		avoid_x = []
		avoid_y = []

		for i in range(len(snake_list)-1):
			avoid_x.append(snake_list[i].x)
			avoid_y.append(snake_list[i].y)

		self.x = random.randrange(model_border)
		if self.x in avoid_x:
			self.x = random.randrange(model_border)

		self.y = random.randrange(model_border)
		if self.y in avoid_y:
			self.y = random.randrange(model_border)

		self.color = "red"
		self.tag = "apple"
		self.dx = speed
		self.dy = speed

class Snake:
	def __init__(self, model_border):
		self.x = model_border / 2
		self.y = model_border / 2
		self.dx = 1 
		self.dy = 0
		self.color = "white"
		self.tag = "snake"

class SnakeGame:
	def __init__(self):

		self.model_border = 30
		self.snake_list = []
		self.apple = Apple(self.model_border, self.snake_list, 0)

		self.initView()
	
	def initView(self):
		w = Tk()
		w.title = "Snake Game"

		self.radius = 5
		self.score = 0

		self.width = self.view_conversion(self.model_border) + self.radius
		self.height = self.view_conversion(self.model_border) + self.radius

		self.canvas = Canvas(w, bg = "black", width = self.width, height = self.height)
		self.canvas.focus_set()
		self.canvas.bind("<Up>", self.up)
		self.canvas.bind("<Down>", self.down)
		self.canvas.bind("<Left>", self.left)
		self.canvas.bind("<Right>", self.right)
		self.canvas.bind("p", self.pause)
		self.canvas.bind("u", self.unpause)

		self.canvas.pack()

		self.canvas.create_text(self.width * 0.5, self.height * 0.3, fill = "blue", text = "Press P to Pause, U to UnPause", tags = "start")
		self.canvas.create_text(self.width * 0.5, self.height * 0.4, fill = "white", text = "Are you ready?", tags = "start")

		startButton = Button(self.canvas, bg = "black", text = "Start", command = self.start)
		startButton.pack()
		self.canvas.create_window(self.width * 0.5, self.height * 0.5, window = startButton, tags = "start") 

		self.frame = Frame(w, bg = "black")
		self.frame.pack() 

		self.points = Label(self.frame, fg = "black", anchor = "se", text = "Score: %s"%self.score)
		self.points.pack()

		self.isStopped = False

		self.sleepTime = 10

		self.num_refresh = 10
		self.index = 0
		self.last = []

		w.mainloop()

	def up(self, event):
		h = self.snake_list[0]
		h.dx = 0
		h.dy = -1

	def down(self, event):
		h = self.snake_list[0]
		h.dx = 0
		h.dy = 1

	def right(self, event):
		h = self.snake_list[0]
		h.dx = 1
		h.dy = 0

	def left(self, event):
		h = self.snake_list[0]
		h.dx = -1
		h.dy = 0

	def start(self):
		self.isStopped = False
		self.canvas.delete("start")
		self.create()

	def pause(self, event):
		self.canvas.create_text(self.width * 0.5, self.height * 0.3, fill = "blue", text = "Game is Paused Zzz", tags = "pause")
		self.isStopped = True

	def unpause(self, event):
		self.canvas.delete("pause")
		self.isStopped = False
		self.mainloop(self.snake_list)

	def restart(self):
		self.isStopped = False
		self.canvas.delete("restart")
		self.canvas.delete("gg")
		self.num_refresh = 10
		self.refresh_score()
		self.snake_list = []
		self.apple = Apple(self.model_border, self.snake_list, 0)
		self.create()

	def create(self):
		for i in range(3):
			self.snake_list.append(Snake(self.model_border))

		self.mainloop(self.snake_list)

	def view_conversion(self, item):
		factor = self.radius * 2
		item = (factor * item) + factor
		return item

	def mainloop(self, snake_list):
		while not self.isStopped:
			self.canvas.after(self.sleepTime)

			if self.index % self.num_refresh == 0:
				last = len(snake_list) - 1
				self.last_dx = snake_list[last].dx
				self.last_dy = snake_list[last].dy

				self.update_model(snake_list, self.apple)

				self.head_dx = snake_list[0].dx
				self.head_dy = snake_list[0].dy

				if self.check_collision(snake_list[0], self.apple) == 1 or self.apple_collision(snake_list[0], self.apple) == 1:
					self.grow(snake_list)
					if self.score < 100:
						self.apple = Apple(self.model_border, snake_list, 0)
					else:
						self.apple = Apple(self.model_border, snake_list, random.random() * 2 - 1)

				self.check_self_collision(snake_list[0], snake_list)
				self.check_collision_walls(snake_list[0])

			self.refresh_view(self.apple, snake_list, self.head_dx, self.head_dy)

			self.index += 1

	def update_model(self, snake_list, apple):
		self.move_body(snake_list)
		self.move_head(snake_list[0])
		self.move_apple(apple)

	def refresh_score(self):
		self.score = 0
		self.update_score()

	def change_score(self):
		self.score = self.score + 10
		self.speed_up()
		self.update_score()

	def speed_up(self):
		if self.num_refresh > 4:
			self.num_refresh -= 1
	
	def update_score(self):
		self.points['text']="Score: " + str(self.score)

	def refresh_view(self, apple, snake_list, dx, dy):
		self.canvas.update()
		self.canvas.delete("apple")
		self.canvas.delete("snake")

		interval = self.index % self.num_refresh

		self.move_view(apple, interval, apple.dx, apple.dy, "red")

		for i in range(len(snake_list)):
			if i == 0:
				self.move_view(snake_list[i], interval, dx, dy, snake_list[i].color)
			elif i == len(snake_list)-1:
				self.move_view(snake_list[i], interval, self.last_dx, self.last_dy, snake_list[i].color)
			else:
				self.move_view(snake_list[i], interval, snake_list[i+1].dx, snake_list[i+1].dy, snake_list[i].color)

	def move_view(self, item, intervals, dx, dy, color):
		inbetween_x = item.x
		inbetween_y = item.y
		inbetween_x -= (dx * ((self.num_refresh - intervals) / float(self.num_refresh)))
		inbetween_y -= (dy * ((self.num_refresh - intervals) / float(self.num_refresh)))
		
		self.draw(inbetween_x, inbetween_y, item, color)

	def draw(self, xval, yval, item, color):
		x = self.view_conversion(xval)
		y = self.view_conversion(yval)
		r = self.radius

		self.canvas.create_oval(x - r, y - r, x + r, y + r, fill = color, tags = item.tag)

	def move_apple(self, apple):
		if apple.x > self.model_border or apple.x < 0:
			apple.dx = -apple.dx
		if apple.y > self.model_border or apple.y < 0:
			apple.dy = -apple.dy

		apple.x += apple.dx
		apple.y += apple.dy

	def move_head(self, snake):
		snake.x += snake.dx
		snake.y += snake.dy

	def move_body(self, snake_list):
		b = len(snake_list) - 1
		if b > 0:
			while b != 0:
				snake_list[b].x = snake_list[b-1].x
				snake_list[b].y = snake_list[b-1].y
				snake_list[b].dx = snake_list[b-1].dx
				snake_list[b].dy = snake_list[b-1].dy
				b = b-1

	def add(self):
		new = Snake(self.model_border)
		self.snake_list.append(new)
		n = self.snake_list.index(new)
		new.x = self.snake_list[n-1].x
		new.y = self.snake_list[n-1].y

	def grow(self, snake_list):
		self.add()
		self.change_score()

	def check_collision(self, head, compare):
		if head.x == compare.x and head.y == compare.y:
	 		return 1

	def apple_collision(self, head, compare):
		if compare.x % 1 != 0:
			if head.x == math.ceil(compare.x) and head.y == math.ceil(compare.y):
				return 1
			elif head.x == math.floor(compare.x) and head.y == math.floor(compare.y):
				return 1

	def check_self_collision(self, head, snake_list):
		b = len(snake_list) - 1
		check = 0
		if b > 0:
			for i in range(len(snake_list) - 1):
				if self.check_collision(head, snake_list[i+1]) == 1:
					self.game_over()
				
	def check_collision_walls(self, head):
		if head.x > self.model_border or head.x < 0 or head.y > self.model_border or head.y < 0:
			self.game_over()

	def game_over(self):
		self.isStopped = True
		self.canvas.create_text(self.width * 0.5, self.height * 0.3, fill = "blue", text = "SQUISH!", tags = "gg")
		self.add_restart_button()

	def add_restart_button(self):
		restartButton = Button(self.canvas, bg = "black", text = "Restart", command = self.restart)
		restartButton.pack()
		self.canvas.create_window(self.width * 0.5, self.height * 0.5, window = restartButton, tags = "restart")

SnakeGame()


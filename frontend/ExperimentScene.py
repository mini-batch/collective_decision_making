import pygame
from frontend.Scene import Scene
import main as m

class ExperimentScene(Scene):
	def __init__(self, environment):
		super().__init__()
		self.env = environment
		self.square_rects = self.create_grid_squares(m.SQUARE_SIZE)
		self.exp_generator = self.env.run_for_visual()

	def render(self, screen):
		self.render_grid(screen)
		self.render_robots(screen)

	def update(self):
		next(self.exp_generator)

	def handle_events(self, events):
		pass
	
	def create_grid_squares(self, square_size):
		"""
		Create rects for each square in the board
		params:
			square_size: (int) size of each square on the board
		return: (2D list of pygame.Rects)
		"""
		board = [[0 for col in range(self.env.grid_size[0])] for row in range(self.env.grid_size[1])]
		for row in range(self.env.grid_size[1]):
			y_pos = row * square_size
			for col in range(self.env.grid_size[0]):
				x_pos = col * square_size
				board[row][col] = pygame.Rect((x_pos, y_pos), (square_size, square_size))
		return board

	def render_grid(self, screen):
		"""
		To be called in the scene's render function to render the grid.
		params:
			screen: (Surface) The Surface to draw to
			square_rects: (2D array of pygame.Rect's) Squares to draw
		"""
		for row in range(self.env.grid_size[1]):
			for col in range(self.env.grid_size[0]):
				if self.env.grid[row][col] == 1:
					pygame.draw.rect(screen, (255,153,102), self.square_rects[row][col])
				elif self.env.grid[row][col] == 2:
					pygame.draw.rect(screen, (102,179,255), self.square_rects[row][col])

	def render_robots(self, screen):
		"""
		Draws Robots on the board. To be called in the scene's render function after render_board.
		params:
			screen: (Surface) The Surface to draw to
			robots: (List : Robot) Robots in the experiment
			square_size: (int) size of each square on the board
		"""
		for robot in self.env.robots:
			pygame.draw.circle(screen, (0,0,0), (robot.position[0] * m.SQUARE_SIZE, robot.position[1] * m.SQUARE_SIZE), m.SQUARE_SIZE * 3 / 10)
			# State indicator
			if robot.decision_state == 1:
				pygame.draw.circle(screen, (255,153,102), (robot.position[0] * m.SQUARE_SIZE, robot.position[1] * m.SQUARE_SIZE), m.SQUARE_SIZE * 1 / 10)
			elif robot.decision_state == 2:
				pygame.draw.circle(screen, (102,179,255), (robot.position[0] * m.SQUARE_SIZE, robot.position[1] * m.SQUARE_SIZE), m.SQUARE_SIZE * 1 / 10)

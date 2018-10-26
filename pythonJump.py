import arcade


class MyGame(arcade.Window):
	def __init__(self, width, height):
		super().__init__(width, height, "Not Game", resizable=True)
		arcade.set_background_color(arcade.color.BLUE)
		self.width = width
		self.height = height

		self.player = [[0, 10], [0, 0]]
		self.pressed = {"a": False, "d": False}

		self.friction = 0.3  # How much per update you slow down on the ground
		self.gravity = 0.7  # How much you get pulled down per update
		self.air_resistance_modifier = 4  # Division, higher is less resistance
		self.jump_height = 15  # Speed up when you jump
		self.speed = 0.8  # Speed increase per update when you hold left or right
		self.max_speed = 30  # Max speed
		self.air_jumps = 0  # Temp, not used in set-up
		self.max_air_jumps = 0  # Number of air jumps you get in total
		self.max_vertical_speed = 10  # Max vertical speed
		self.wall_jumps = 0
		self.max_wall_jumps = 1

	def on_draw(self):
		arcade.start_render()

		# Draw the player
		arcade.draw_rectangle_filled(self.player[0][0] + 25, self.player[0][1] + 25, 50, 50, arcade.color.RED)

		# Draw the grass at the bottom
		arcade.draw_rectangle_filled(self.width / 2, 5, self.width, 10, arcade.color.GREEN)

	def update(self, delta_time):

		if self.pressed["a"]:
			if self.player[0][1] > 10:  # If in the air add a third of the speed instead
				self.player[1][0] += -self.speed / 3
			else:
				self.player[1][0] += -self.speed

		if self.pressed["d"]:
			if self.player[0][1] > 10:  # If in the air add a third of the speed instead
				self.player[1][0] += self.speed / 3
			else:
				self.player[1][0] += self.speed

		# Increase the speeds in both directions
		self.player[0][0] += self.player[1][0]
		self.player[0][1] += self.player[1][1]

		# If your speed is higher than the max speed, set it to the max speed
		if self.player[1][0] > self.max_speed:
			self.player[1][0] = self.max_speed
		elif self.player[1][0] < -self.max_speed:
			self.player[1][0] = -self.max_speed

		# If the player is above ground, draw them down with gravity
		if self.player[0][1] > 10:
			self.player[1][1] += -self.gravity

		# Makes player never go under 10 pixels, and removes downward momentum when hitting the floor
		if self.player[0][1] < 10:
			self.player[1][1] = 0
			self.player[0][1] = 10

		# if you are on the ground add friction in different directions
		if self.player[0][1] == 10:
			if self.player[1][0] < 0:
				self.player[1][0] += self.friction
				if self.player[1][0] > 0:
					self.player[1][0] = 0

			elif self.player[1][0] > 0:
				self.player[1][0] += -self.friction
				if self.player[1][0] < 0:
					self.player[1][0] = 0

		# Otherwise you are in the air and add air resistance
		else:
			if self.player[1][0] < 0:
				self.player[1][0] += self.friction / self.air_resistance_modifier
				if self.player[1][0] > 0:
					self.player[1][0] = 0

			elif self.player[1][0] > 0:
				self.player[1][0] += -self.friction / self.air_resistance_modifier
				if self.player[1][0] < 0:
					self.player[1][0] = 0

		# If past the wall, set them to the wall and reverse x speed
		if self.player[0][0] < 0:
			self.player[0][0] = 0
			self.player[1][0] = -self.player[1][0]
		elif self.player[0][0] > self.width - 50:
			self.player[0][0] = self.width - 50
			self.player[1][0] = -self.player[1][0]

	def on_key_press(self, key, modifier):
		if key == ord("w") or key == ord(" "):
			# If the player is on the ground, launch them and reset the air and wall jumps
			# Not tracked if held because it's worse
			if self.player[0][1] == 10:
				self.player[1][1] += self.jump_height
				self.air_jumps = self.max_air_jumps
				self.wall_jumps = self.max_wall_jumps

			# If you have wall jumps left and is touching a wall remove one jump
			elif (self.player[0][0] == 0 or self.player[0][0] == self.width - 50) and self.wall_jumps > 0:
				self.wall_jumps += -1
				self.player[1][1] += self.jump_height

			# If you have air jumps, use one and jump
			elif self.air_jumps > 0:
				self.air_jumps += -1
				self.player[1][1] += self.jump_height

		# Allows me to track if button is pressed, to make smooth movement
		# Tracks all buttons to allow future expansion
		self.pressed[chr(key)] = True

	def on_key_release(self, key, modifiers):
		# Tracks all buttons to allow future expansion
		self.pressed[chr(key)] = False

	def on_resize(self, width, height):
		super().on_resize(width, height)
		self.width = width
		self.height = height


game = MyGame(1000, 500)

arcade.run()

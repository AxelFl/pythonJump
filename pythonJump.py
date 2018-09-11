import arcade


class player():
	def __init__(self, x_pos, y_pos, x_vel, y_vel, x_size, y_size):
		self.x_pos = x_pos
		self.y_pos = y_pos
		self.x_vel = x_vel
		self.y_vel = y_vel
		self.x_size = x_size
		self.y_size = y_size

	def check_collision(self, collisions_x, collisions_y):
		if round(self.x_pos) in collisions_x or round(self.x_pos) + self.x_size in collisions_x:
			return True
		else:
			return False


class MyGame(arcade.Window):
	def __init__(self, width, height):
		super().__init__(width, height, "Not Game", resizable=True)
		arcade.set_background_color(arcade.color.BLUE)
		self.width = width
		self.height = height

		self.player = player(0, 0, 0, 0, 50, 50)
		self.a_pressed = False
		self.d_pressed = False

		self.friction = 0.3  # How much per update you slow down on the ground
		self.gravity = 1  # How much you get pulled down per update
		self.air_resistance_modifier = 4  # Division, higher is less resistance
		self.jump_height = 15  # Speed up when you jump
		self.speed = 0.8  # Speed increase per update when you hold left or right
		self.max_speed = 30  # Max speed
		self.air_jumps = 0  # Temp, not used in set-up
		self.max_air_jumps = 0  # Number of air jumps you get in total
		self.max_vertical_speed = 10  # Max vertical speed
		self.wall_jumps = 0
		self.max_wall_jumps = 1
		self.x_collisions = []
		self.y_collisions = []

	def on_draw(self):
		arcade.start_render()

		# Draw the player
		arcade.draw_rectangle_filled(self.player.x_pos + 25, self.player.y_pos + 25, 50, 50, arcade.color.RED)

		# Draw the grass at the bottom
		arcade.draw_rectangle_filled(self.width / 2, 5, self.width, 10, arcade.color.GREEN)

		# Draw drawn collisions
		for i in range(0, len(self.x_collisions) - 1):
			arcade.draw_rectangle_filled(self.x_collisions[i], self.y_collisions[i], 1, 1, arcade.color.GREEN)

	def update(self, delta_time):

		if self.a_pressed:
			if self.player.y_pos > 10:  # If in the air add less speed
				self.player.x_vel += -self.speed / 1.5
			else:
				self.player.x_vel += -self.speed

		if self.d_pressed:
			if self.player.y_pos > 10:  # If in the air add less speed
				self.player.x_vel += self.speed / 1.5
			else:
				self.player.x_vel += self.speed

		# Increase the speeds in both directions
		self.player.x_pos += self.player.x_vel
		self.player.y_pos += self.player.y_vel

		# If your speed is higher than the max speed, set it to the max speed
		if self.player.x_vel > self.max_speed:
			self.player.x_vel = self.max_speed
		elif self.player.x_vel < -self.max_speed:
			self.player.x_vel = -self.max_speed

		# If the player is above ground, draw them down with gravity
		if self.player.y_pos > 10:
			self.player.y_vel += -self.gravity

		# Makes player never go under 10 pixels, and removes downward momentum when hitting the floor
		if self.player.y_pos < 10:
			self.player.y_vel = 0
			self.player.y_pos = 10

		# if you are on the ground add friction in different directions
		if self.player.y_pos == 10:
			if self.player.x_vel < 0:
				self.player.x_vel += self.friction
				if self.player.x_vel > 0:
					self.player.x_vel = 0

			elif self.player.x_vel > 0:
				self.player.x_vel += -self.friction
				if self.player.x_vel < 0:
					self.player.x_vel = 0

		# Otherwise you are in the air and add air resistance
		else:
			if self.player.x_vel < 0:
				self.player.x_vel += self.friction / self.air_resistance_modifier
				if self.player.x_vel > 0:
					self.player.x_vel = 0

			elif self.player.x_vel > 0:
				self.player.x_vel += -self.friction / self.air_resistance_modifier
				if self.player.x_vel < 0:
					self.player.x_vel = 0

		# If past the wall, set them to the wall and reverse x speed
		if self.player.x_pos < 0:
			self.player.x_pos = 0
			self.player.x_vel = -self.player.x_vel
		elif self.player.x_pos > self.width - 50:
			self.player.x_pos = self.width - 50
			self.player.x_vel = -self.player.x_vel

		if self.player.check_collision(self.x_collisions, self.y_collisions):
			self.player.x_vel = 0
			self.player.y_vel = 0

	def on_key_press(self, key, modifier):
		if key == ord("w") or key == ord(" "):
			# If the player is on the ground, launch them and reset the air and wall jumps
			# Not tracked if held because it's worse
			if self.player.y_pos == 10:
				self.player.y_vel += self.jump_height
				self.air_jumps = self.max_air_jumps
				self.wall_jumps = self.max_wall_jumps

			# If you have wall jumps left and is touching a wall remove one jump
			elif (self.player.x_pos == 0 or self.player.x_pos == self.width - 50) and self.wall_jumps > 0:
				self.wall_jumps += -1
				self.player.y_vel += self.jump_height

			# If you have air jumps, use one and jump
			elif self.air_jumps > 0:
				self.air_jumps += -1
				self.player.y_vel += self.jump_height

		# Allows me to track if button is pressed, to make smooth movement
		if key == ord("a"):
			self.a_pressed = True

		if key == ord("d"):
			self.d_pressed = True

	def on_key_release(self, key, modifiers):
		if key == ord("a"):
			self.a_pressed = False

		if key == ord("d"):
			self.d_pressed = False

	def on_resize(self, width, height):
		super().on_resize(width, height)
		self.width = width
		self.height = height

	def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
		self.x_collisions.append(round(x))
		self.y_collisions.append(round(y))


game = MyGame(1000, 500)

arcade.run()

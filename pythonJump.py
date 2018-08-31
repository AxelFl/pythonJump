import arcade


class MyGame(arcade.Window):
	def __init__(self, width, height):
		super().__init__(width, height, "Not Game")
		arcade.set_background_color(arcade.color.BLUE)
		self.player = [[0, 10], [0, 0]]
		self.w_pressed = False
		self.a_pressed = False
		self.d_pressed = False
		self.friction = 0.3
		self.gravity = 0.7
		self.air_resistance_modifier = 4
		self.jump_height = 50
		self.speed = 0.8
		self.max_speed = 30
		self.air_jumps = 0
		self.max_air_jumps = 2

	def on_draw(self):
		arcade.start_render()

		arcade.draw_rectangle_filled(self.player[0][0] + 25, self.player[0][1] + 25, 50, 50, arcade.color.RED)
		arcade.draw_rectangle_filled(500, 5, 1000, 10, arcade.color.GREEN)

	def update(self, deltatime):

		if self.a_pressed:
			if self.player[0][1] > 10:
				self.player[1][0] += -self.speed / 3
			else:
				self.player[1][0] += -self.speed
		if self.d_pressed:
			if self.player[0][1] > 10:
				self.player[1][0] += self.speed / 3
			else:
				self.player[1][0] += self.speed

		self.player[0][0] += self.player[1][0]
		self.player[0][1] += self.player[1][1]

		if self.player[1][0] > self.max_speed:
			self.player[1][0] = self.max_speed
		elif self.player[1][0] < -self.max_speed:
			self.player[1][0] = -self.max_speed

		if self.player[1][1] > 10:
			self.player[1][1] = 10

		# If the player is above ground, draw them down with gravity
		if self.player[0][1] > 10:
			self.player[1][1] += -self.gravity

		# Makes player never go under 10 pixels, and removes downward momentum when hitting the floor
		if self.player[0][1] < 10:
			self.player[1][1] = 0
			self.player[0][1] = 10

		if self.player[0][1] == 10:
			if self.player[1][0] < 0:
				self.player[1][0] += self.friction
				if self.player[1][0] > 0:
					self.player[1][0] = 0

			elif self.player[1][0] > 0:
				self.player[1][0] += -self.friction
				if self.player[1][0] < 0:
					self.player[1][0] = 0
		else:
			if self.player[1][0] < 0:
				self.player[1][0] += self.friction / self.air_resistance_modifier
				if self.player[1][0] > 0:
					self.player[1][0] = 0

			elif self.player[1][0] > 0:
				self.player[1][0] += -self.friction / self.air_resistance_modifier
				if self.player[1][0] < 0:
					self.player[1][0] = 0

		if self.player[0][0] < 0:
			self.player[0][0] = 0
			self.player[1][0] = -self.player[1][0]
		elif self.player[0][0] > 950:
			self.player[0][0] = 950
			self.player[1][0] = -self.player[1][0]

	def on_key_press(self, key, modifier):
		if key == ord("w") or key == ord(" "):
			if self.player[0][1] == 10 or self.player[0][0] == 0 or self.player[0][0] == 950:
				self.player[1][1] += self.jump_height
				self.air_jumps = self.max_air_jumps
			elif self.air_jumps > 0:
				self.air_jumps += -1
				self.player[1][1] += self.jump_height

		if key == ord("a"):
			self.a_pressed = True

		if key == ord("d"):
			self.d_pressed = True

	def on_key_release(self, key, modifiers):
		if key == ord("w") or key == ord(" "):
			self.w_pressed = False
		if key == ord("a"):
			self.a_pressed = False
		if key == ord("d"):
			self.d_pressed = False


game = MyGame(1000, 500)

arcade.run()

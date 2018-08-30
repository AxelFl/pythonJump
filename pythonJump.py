import arcade


class MyGame(arcade.Window):
	def __init__(self, width, height):
		super().__init__(width, height, "Game")
		arcade.set_background_color(arcade.color.BLUE)
		self.player = [[0, 10], [0, 0]]
		self.w_pressed = False
		self.a_pressed = False
		self.d_pressed = False
		self.friction = 0.4
		self.gravity = 0.5
		self.air_resistance_modifier = 3
		self.jump_height = 25
		self.speed = 1

	def on_draw(self):
		arcade.start_render()

		arcade.draw_rectangle_filled(self.player[0][0] + 25, self.player[0][1] + 25, 50, 50, arcade.color.RED)
		arcade.draw_rectangle_filled(500, 5, 1000, 10, arcade.color.GREEN)

	def update(self, deltatime):
		if self.w_pressed and self.player[0][1] == 10:
			self.player[1][1] += self.jump_height
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

		if self.player[1][0] > 10:
			self.player[1][0] = 10
		elif self.player[1][0] < -10:
			self.player[1][0] = -10

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

	def on_key_press(self, key, modifier):
		if key == ord("w") or key == ord(" "):
			self.w_pressed = True

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

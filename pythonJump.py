import arcade


class MyGame(arcade.Window):
	def __init__(self, width, height):
		super().__init__(width, height, "Game")
		arcade.set_background_color(arcade.color.BLACK)
		self.player = [[0, 10], [0, 0]]
		self.w_pressed = False
		self.a_pressed = False
		self.d_pressed = False

	def on_draw(self):
		arcade.start_render()

		arcade.draw_rectangle_filled(self.player[0][0] + 25, self.player[0][1] + 25, 50, 50, arcade.color.RED)

	def update(self, deltatime):
		if self.w_pressed and self.player[0][1] == 10:
			self.player[1][1] += 50
		if self.a_pressed:
			self.player[1][0] += -1
		if self.d_pressed:
			self.player[1][0] += 1

		self.player[0][0] += self.player[1][0]
		self.player[0][1] += self.player[1][1]

		if self.player[1][0] > 10:
			self.player[1][0] = 10
		elif self.player[1][0] < -10:
			self.player[1][0] = -10

		if self.player[1][1] > 10:
			self.player[1][1] = 10

		if self.player[0][1] > 10:
			self.player[1][1] += -1

		if self.player[0][1] < 10:
			self.player[1][1] = 0
			self.player[0][1] = 10

		if self.player[0][1] == 10:
			if self.player[1][0] < 0:
				self.player[1][0] += 0.5
				if self.player[1][0] > 0:
					self.player[1][0] = 0

			elif self.player[1][0] > 0:
				self.player[1][0] += -0.5
				if self.player[1][0] < 0:
					self.player[1][0] = 0

	def on_key_press(self, key, modifier):
		if key == ord("w"):
			self.w_pressed = True

		if key == ord("a"):
			self.a_pressed = True

		if key == ord("d"):
			self.d_pressed = True

	def on_key_release(self, key, modifiers):
		if key == ord("w"):
			self.w_pressed = False
		if key == ord("a"):
			self.a_pressed = False
		if key == ord("d"):
			self.d_pressed = False


game = MyGame(1000, 500)

arcade.run()
